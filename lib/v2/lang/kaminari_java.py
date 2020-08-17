from .. import generator
from .. import gen
from .. import boxes
from .. import semantic



TYPE_CONVERSION = {
    'uint8':    'Byte',
    'uint16':   'Short',
    'uint32':   'Integer',
    'uint64':   'Long',
    'int8':     'Char',
    'int16':    'Short',
    'int32':    'Integer',
    'int64':    'Long',
    'float':    'float',
    'double':   'double',
    'bool':     'boolean',
    'vector':   'ArrayList',
    'optional': 'Optional'
}

def to_camel_case(snake_str, capitalize=True):
    components = snake_str.split('_')
    leading = components[0]
    if capitalize:
        leading = leading.capitalize()
    return leading + ''.join(x.capitalize() for x in components[1:])

class File(object):
    def __init__(self):
        self.sources = []

    def add(self, code):
        self.sources.append(code)

    def source(self, prepend=[]):
        source = gen.Scope(prepend + self.sources).both(0)
        return source
    
    def __str__(self):
        return self.source()


class LangGenerator(generator.Generator):
    def __init__(self, config, role, queues, messages, programs):
        super().__init__(config, role, queues, messages, programs)
        
        # Some helpers
        self.handler_programs = set()

        # Output code
        self.marshal_file = File()
        self.opcodes_file = File()
        self.rpc_file = File()
        self.structs_file = File()
        self.queues_file = File()

        # Flush marshal class already
        self.marshal_cls = gen.Class('Marshal extends IMarshal', csharp_style=True)
        self.marshal_file.add(self.marshal_cls)

        # RPC class
        self.rpc_cls = gen.Class('Rpc', csharp_style=True)
        self.rpc_file.add(self.rpc_cls)


    def __is_trivial(self, message: boxes.MessageBox):
        for decl in self.message_fields_including_base(message):
            # Optional implies we might have variant sizes
            if decl.optional:
                return False

            dtype = decl.dtype.dtype.eval()

            # Vectors are runtime only
            if dtype == 'vector':
                return False

            # Including other messages might include optionals/vectors
            if self.is_message(dtype) and not self.__is_trivial(self.messages[dtype]):
                return False

        return True

    def __write_value(self, dtype, variable):
        # It seems to be a message type
        if self.is_message(dtype):
            return gen.Statement(f'{variable}.pack(marshal, packet)')
        else:
            return gen.Statement(f'packet.write{dtype.capitalize()}({variable})')

    def __write_type(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            inner = decl.dtype.spec.eval()
            ctype = inner
            if not self.is_message(inner):
                ctype = TYPE_CONVERSION[inner]
            else:
                ctype = to_camel_case(ctype)
            
            return gen.Scope([
                gen.Statement(f'packet.writeByte((byte){variable}.size())'),
                gen.Statement(f'for ({ctype} val : {variable})', ending=''),
                gen.Block([
                    self.__write_value(decl.dtype.spec.eval(), 'val')
                ])
            ])
        
        return self.__write_value(dtype, variable)

    def __read_type(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            inner = decl.dtype.spec.eval()

            if not self.is_message(inner):
                return gen.Scope([
                    gen.Statement(f'int size = Byte.toUnsignedInt(packet.readByte())'),
                    gen.Statement(f'if (packet.bytesRead() + size * marshal.sizeof{to_camel_case(inner)}() >= packet.bufferSize())', ending=''),
                    gen.Block([
                        gen.Statement('return false')
                    ]),
                    gen.Statement(f'{variable} = new {TYPE_CONVERSION["vector"]}<{TYPE_CONVERSION[inner]}>()'),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{variable}.add(packet.read{to_camel_case(inner)}())')
                    ])
                ])
            else:
                inner = to_camel_case(inner)

                return gen.Scope([
                    gen.Statement(f'int size = Byte.toUnsignedInt(packet.readByte())'),
                    gen.Statement(f'{variable} = new {TYPE_CONVERSION["vector"]}<{inner}>()'),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{inner} data = new {inner}()'),
                        gen.Statement(f'if (data.unpack(marshal, packet))', ending=''),
                        gen.Block([
                            gen.Statement(f'{variable}.add(data)')
                        ]),
                        gen.Statement(f'else'),
                        gen.Block([
                            gen.Statement('return false')
                        ])
                    ])
                ])

        if self.is_message(dtype):
            dtype = to_camel_case(dtype)

            return gen.Scope([
                gen.Statement(f'{variable} = new {dtype}()'),
                gen.Statement(f'if (!{variable}.unpack(marshal, packet))', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ])
            ])

        return gen.Scope([
            gen.Statement(f'if (packet.bytesRead() + marshal.sizeof{to_camel_case(dtype)}() >= packet.bufferSize())', ending=''),
            gen.Block([
                gen.Statement('return false')
            ]),
            gen.Statement(f'{variable} = packet.read{to_camel_case(dtype)}()')
        ])

    def __write_size(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            # There are two cases
            #  1) Inner type is trivial thus we can do `size() * sizeof(inner)`
            #  2) Inner type is not trivial and we must iterate
            inner = decl.dtype.spec.eval()
            ctype = inner
            if not self.is_message(inner):
                ctype = TYPE_CONVERSION[inner]
            else:
                ctype = to_camel_case(ctype)

            # Case 1
            if not self.is_message(inner) or self.__is_trivial(self.messages[inner]):
                return gen.Statement(f'size += Byte.Bytes + {variable}.size() * marshal.sizeof{to_camel_case(inner)}()')
            # Case 2
            else:
                return gen.Scope([
                    gen.Statement('size += Byte.Bytes'),
                    gen.Statement(f'for ({ctype} val : {variable})', ending=''),
                    gen.Block([
                        gen.Statement(f'size += val.size(marshal)')
                    ])
                ])
            
        elif self.is_message(dtype):
            return gen.Statement(f'size += {variable}.size(marshal)')
        else:
            return gen.Statement(f'size += marshal.sizeof{to_camel_case(dtype)}()')
        
    def _generate_structure(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        base = ' extends IData'
        if message.base.name is not None:
            base = f' extends {message.base.name.eval()}'

        struct = gen.Class(to_camel_case(message_name), decl_name_base=base, csharp_style=True)
        for decl in message.fields.eval():
            dtype = decl.dtype.dtype.eval()
            ctype = '{}'
            if decl.optional:
                ctype = 'Optional<{}>'

            temp = dtype
            if dtype == 'vector':
                ctype = ctype.format('ArrayList<{}>')
                temp = decl.dtype.spec.eval()
            
            if not self.is_message(temp):
                temp = TYPE_CONVERSION[temp]
            else:
                temp = to_camel_case(temp)

            ctype = ctype.format(temp)

            struct.attributes.append(gen.Attribute(
                ctype, 
                decl.name.eval(),
                visibility=gen.Visibility.PUBLIC
            ))

        self.structs_file.add(struct)
        self.__generate_message_packer(message, struct)
        self.__generate_message_unpacker(message, struct)
        self.__generate_message_size(message, struct)

    def __generate_message_packer(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        method = gen.Method('void', f'pack', [
            gen.Variable('IMarshal', 'marshal'),
            gen.Variable('Packet', 'packet')
        ], visibility=gen.Visibility.PUBLIC)

        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'packet.writeBoolean(this.{name}.hasValue)'))
                method.append(gen.Statement(f'if (this.{name}.hasValue)', ending=''))
                method.append(gen.Block([
                    self.__write_type(decl, f'this.{name}.value')
                ]))
            else:
                method.append(self.__write_type(decl, f'this.{name}'))

        struct.methods.append(method)
        
    def __generate_message_unpacker(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        method = gen.Method('boolean', f'unpack', [
            gen.Variable(f'IMarshal', 'marshal'),
            gen.Variable('PacketReader', 'packet')
        ], visibility=gen.Visibility.PUBLIC)

        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'if (packet.bytesRead() + Byte.Bytes >= packet.bufferSize())', ending=''))
                method.append(gen.Block([
                    gen.Statement('return false')
                ]))
                
                method.append(gen.Statement(f'if (packet.readByte() == 1)', ending=''))
                method.append(gen.Block([
                    self.__read_type(decl, f'this.{name}.Value')
                ]))
            else:
                method.append(self.__read_type(decl, f'this.{name}'))
    
        struct.methods.append(method)

    def __generate_message_size(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        # Even if messages are trivial, there is no such thing as sizeof
        # Thus we must always iterate over everything
        if self.__is_trivial(message):
            # This method is registered on the marshal class
            method = gen.Method('int', f'sizeof{to_camel_case(message_name)}', [], visibility=gen.Visibility.PUBLIC)
            self.marshal_cls.methods.append(method)

            method.append(gen.Statement('int size = 0'))    
            # Manually loop all types
            for decl in self.message_fields_including_base(message):
                name = decl.name.eval()
                method.append(self.__write_size(decl, f'this.{name}'))

            method.append(gen.Statement('return size'))    

        # This one is in the struct itself
        method = gen.Method('int', f'size', [
            gen.Variable(f'IMarshal', 'marshal')
        ], visibility=gen.Visibility.PUBLIC)
        struct.methods.append(method)

        method.append(gen.Statement('int size = 0'))    
        # Manually loop all types
        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement('size += Byte.Bytes'))
                method.append(gen.Statement(f'if (this.{name}.hasValue)', ending=''))
                method.append(gen.Block([
                    self.__write_size(decl, f'this.{name}.value')
                ]))
            else:
                method.append(self.__write_size(decl, f'this.{name}'))

        method.append(gen.Statement('return size'))

    # These methods do nothing here, Java interfaces require pack, unpack and size
    # to be implemented upon declaration
    def _generate_message_packer(self, message: boxes.MessageBox):
        pass

    def _generate_message_unpacker(self, message: boxes.MessageBox):
        pass

    def _generate_message_size(self, message: boxes.MessageBox):
        pass

    def _generate_program_send(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        queue = program.queue.eval()
        args = program.args.eval()
        message_name = to_camel_case(args[0])

        # Returned methods
        methods = []

        # Create methods
        if self.can_queue_have_callback(self.queues[queue]):
            method = gen.Method('void', f'send{to_camel_case(program_name)}', [
                gen.Variable(f'ProtocolQueues', 'pq'),
                gen.Variable(f'{message_name}', 'data'),
                gen.Variable('IAckCallback', 'callback')
            ], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'pq.send{to_camel_case(queue)}(Marshal.instance, Opcodes.opcode{to_camel_case(program_name)}, data, callback)'))
            methods.append(method)
        
        # Standard no callback method
        method = gen.Method('void', f'send{to_camel_case(program_name)}', [
            gen.Variable(f'ProtocolQueues', 'pq'),
            gen.Variable(f'{message_name}', 'data')
        ], visibility=gen.Visibility.PUBLIC)
        method.append(gen.Statement(f'pq.send{to_camel_case(queue)}(Marshal.instance, Opcodes.opcode{to_camel_case(program_name)}, data)'))
        methods.append(method)
        
        # There are two types of broadcasts, one that implies neighbouring areas
        # and one that doesn't, generate both
        for suffix in ('', 'Single'):
            if self.has_queue_packed_add(self.queues[queue]):
                
                if self.can_queue_have_callback(self.queues[queue]):
                    method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                        gen.Variable('IBroadcaster', 'broadcaster'),
                        gen.Variable(f'{message_name}', 'data'),
                        gen.Variable('IAckCallback', 'callback')
                    ], visibility=gen.Visibility.PUBLIC)
                    methods.append(method)

                    method.append(gen.Statement(f'Packet packet = Packet.make(Opcodes.opcode{to_camel_case(program_name)}, callback)'))
                    method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                    method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation {', ending=''))
                    method.append(gen.Scope([
                        gen.Statement('void onCandidate(ProtocolQueue pq) {'),
                        gen.Scope([
                            gen.Statement(f'pq.send{to_camel_case(queue)}(packet)')
                        ], indent=True),
                        gen.Statement('})')
                    ], indent=True)),
                    method.append(gen.Statement('})'))
                
                # No callback
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('IBroadcaster', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC)
                methods.append(method)

                method.append(gen.Statement(f'Packet packet = Packet.make(Opcodes.opcode{to_camel_case(program_name)})'))
                method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation {', ending=''))
                method.append(gen.Scope([
                    gen.Statement('void onCandidate(ProtocolQueue pq) {'),
                    gen.Scope([
                        gen.Statement(f'pq.send{to_camel_case(queue)}(packet)')
                    ], indent=True),
                    gen.Statement('})')
                ], indent=True)),
                method.append(gen.Statement('})'))

            else:
                # Adding by bare data is always available
                # But we can not have callbacks YET
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('IBroadcaster', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC)
                methods.append(method)

                method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation {', ending=''))
                method.append(gen.Scope([
                    gen.Statement('void onCandidate(ProtocolQueue pq) {'),
                    gen.Scope([
                        gen.Statement(f'pq.send{to_camel_case(queue)}(Marshal.instance, Opcodes.opcode{to_camel_case(program_name)}, data)')
                    ], indent=True),
                    gen.Statement('})')
                ], indent=True)),
                method.append(gen.Statement('})'))
            
        for method in methods:
            self.rpc_cls.methods.append(method)

        return methods
    
    def _generate_program_recv(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        args = program.args.eval()
        message_name = args[0]

        method = gen.Method('boolean', f'handle{to_camel_case(program_name)}', [
            gen.Variable('IMarshal', 'marshal'),
            gen.Variable('PacketReader', 'packet'),
            gen.Variable('IClient', 'client')
        ], visibility=gen.Visibility.PRIVATE)

        if program.cond.attr is not None:
            attr = program.cond.attr.eval()
            value = program.cond.value.eval()
            false_case = program.cond.false_case
            if false_case.action is not None:
                false_case = false_case.action.eval()
            else:
                false_case = 'client.handleClientError'

            #method.append(gen.Statement(f'if (client->{attr}() != {attr}::{value})', ending=''))
            method.append(gen.Statement(f'if (!clint.check(client, "{attr}", {value}))', ending=''))
            method.append(gen.Block([
                gen.Statement(f'return {false_case}(client, packet.opcode())')
            ]))
        
        method.append(gen.Statement(f'{to_camel_case(message_name)} data = new {to_camel_case(message_name)}()'))
        method.append(gen.Statement(f'if (!data.unpack(marshal, packet))', ending=''))
        method.append(gen.Block([
            gen.Statement('return false')
        ]))

        method.append(gen.Statement(f'return client.on{to_camel_case(program_name)}(client, data, packet.timestamp())'))

        self.handler_programs.add(program_name)
        self.marshal_cls.methods.append(method)

        return [method]

    def _generate_internals(self):
        # Trivial types size
        for dtype in semantic.TRIVIAL_TYPES:
            ctype = TYPE_CONVERSION[dtype]
            method = gen.Method('int', f'sizeof{to_camel_case(dtype)}', visibility=gen.Visibility.PUBLIC)
            if dtype == 'bool':
                # Java booleans are kinda special
                method.append(gen.Statement(f'return Byte.Bytes'))
            else:
                method.append(gen.Statement(f'return {ctype.capitalize()}.Bytes'))
            self.marshal_cls.methods.append(method)

        # General packet handler
        method = gen.Method('boolean', 'handlePacket', [
            gen.Variable('Packet', 'packet'),
            gen.Variable('IClient', 'client')
        ], visibility=gen.Visibility.PUBLIC)

        method.append(gen.Statement('switch (packet.opcode())', ending=''))
        method.append(gen.Block([
            gen.Scope([
                gen.Statement(f'case Opcodes.opcode{to_camel_case(program)}:', ending=''),
                gen.Scope([
                    gen.Statement(f'return handle{to_camel_case(program)}(this, packet, client)') 
                ], indent=True)
            ]) for program in self.handler_programs
        ] + [gen.Scope([
            gen.Statement(f'default:', ending=''),
            gen.Scope([
                gen.Statement(f'return false') 
            ], indent=True)
        ])]))

        self.marshal_cls.methods.append(method)

        # Opcodes enum
        opcodes = gen.Class('Opcodes', csharp_style=True)
        for program in self.programs.values():
            program_name = program.name.eval()
            name = f'opcode{to_camel_case(program_name)}'

            opcodes.attributes.append(
                gen.Attribute(
                    'Short', 
                    f'{name: <24}', 
                    f'0x{self.opcodes[program_name]}',
                    ['static', 'const'],
                    visibility=gen.Visibility.PUBLIC,
                )
            )
            
        self.opcodes_file.add(opcodes)

        # Protocol queues
        queues = gen.Class('ProtocolQueues', csharp_style=True)
        self.queues_file.add(queues)
        
        constructor = gen.Method('', 'ProtocolQueues', [
            gen.Variable('int', 'resendThreshold')
        ], visibility=gen.Visibility.PUBLIC)
        queues.methods.append(constructor)

        reset = gen.Method('void', 'reset', visibility=gen.Visibility.PUBLIC)
        reset.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.reset()') for queue in self.queues.keys()
        ]))
        queues.methods.append(reset)

        ack = gen.Method('void', 'ack', [gen.Variable('Short', 'blockId')], visibility=gen.Visibility.PUBLIC)
        ack.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.ack(blockId)') for queue in self.queues.keys()
        ]))
        queues.methods.append(ack)

        process = gen.Method('void', 'process', [
            gen.Variable('Short', 'blockId'),
            gen.Variable('Ref<Short>', 'remaining'),
            gen.Variable('TreeMap<Integer, ArrayList<Packet>>', 'byBlock')
        ], visibility=gen.Visibility.PUBLIC)
        process.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.process(blockId, remaining, byBlock)') for queue in self.queues.keys()
        ]))
        queues.methods.append(process)

        for queue_name, queue in self.queues.items():
            # Attribute
            queue_base = queue.base.subtype.eval()
            queue_packer = 'ImmediatePacker'
            queue_packer_template = f''

            if queue.specifier.queue_type == boxes.QueueSpecifierType.SPECIALIZED:
                queue_packer = to_camel_case(queue.specifier.args.eval())

            elif queue.specifier.queue_type == boxes.QueueSpecifierType.TEMPLATED:
                queue_packer = 'UniqueMergePacker'
                args = queue.specifier.args
                queue_packer_template = f'<{args[0].eval()}, {args[1].eval()}, {args[2].eval()}>'

            queue_packer = queue_packer + queue_packer_template
            # TODO(gpascualg): Forward queue arguments
            # if queue.base.argument is not None:
            #     queue_packer = f'{queue_packer}, {queue.base.argument.eval()}'

            queue_qualified_name = f'{to_camel_case(queue_base)}<{queue_packer}>'

            constructor.append(
                gen.Statement(f'{to_camel_case(queue_name, False)} = new {queue_qualified_name}({queue_packer}.class)')
            )

            queues.attributes.append(gen.Attribute(
                queue_qualified_name,
                f'{to_camel_case(queue_name, False)}'
            ))

            # # General send with data
            # if self.can_queue_have_callback(queue):
            #     send = gen.Method('void', f'send_{queue_name}', [
            #         gen.Variable('::kumo::opcode', 'opcode'),
            #         gen.Variable(f'D&&', 'data'),
            #         gen.Variable('T&&', 'callback')
            #     ], template=gen.Statement('template <typename D, typename T>', ending=''), visibility=gen.Visibility.PUBLIC)
            #     send.append(gen.Statement(f'_{queue_name}.add(opcode, std::forward<D>(data), std::forward<T>(callback))'))
            # else:
            #     send = gen.Method('void', f'send_{queue_name}', [
            #         gen.Variable('::kumo::opcode', 'opcode'),
            #         gen.Variable(f'D&&', 'data')
            #     ], template=gen.Statement('template <typename D>', ending=''), visibility=gen.Visibility.PUBLIC)
            #     send.append(gen.Statement(f'_{queue_name}.add(opcode, std::forward<D>(data))'))

            # queues.methods.append(send)

            # if self.has_queue_packed_add(queue):
            #     send = gen.Method('void', f'send_{queue_name}', [
            #         gen.Variable('const boost::intrusive_ptr<::kaminari::packet>&', 'packet')
            #     ], visibility=gen.Visibility.PUBLIC)
            #     send.append(gen.Statement(f'_{queue_name}.add(packet)'))
            #     queues.methods.append(send)

    def dump(self, path):
        package = self.config.get('package', 'kumo')

        # Do we need to include marshal base class?
        marshal_include = []

        with open(f'{path}/Marshal.java', 'w') as fp:
            fp.write(self.marshal_file.source())

        with open(f'{path}/Rpc.java', 'w') as fp:
            fp.write(self.rpc_file.source())

        with open(f'{path}/Structs.java', 'w') as fp:
            fp.write(self.structs_file.source())

        with open(f'{path}/Opcodes.java', 'w') as fp:
            fp.write(self.opcodes_file.source())

        with open(f'{path}/ProtocolQueues.java', 'w') as fp:
            fp.write(self.queues_file.source())


        