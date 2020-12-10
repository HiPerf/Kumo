from .. import generator
from .. import gen
from .. import boxes
from .. import semantic

import os
import sys
import itertools as it
import shutil


TYPE_CONVERSION = {
    'uint8':    'Byte',
    'uint16':   'Short',
    'uint32':   'Integer',
    'uint64':   'Long',
    'int8':     'Byte',
    'int16':    'Short',
    'int32':    'Integer',
    'int64':    'Long',
    'float':    'Float',
    'double':   'Double',
    'bool':     'Boolean',
    'vector':   'ArrayList',
    'optional': 'Optional',
    'string': 'String'
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
        self.client_file = File()
        self.opcodes_file = File()
        self.rpc_file = File()
        self.queues_file = File()
        self.config_file = File()

        # Needs processing at the end
        self.trivial_messages = {}
        self.all_structs = {}

        # Flush marshal class already
        self.marshal_cls = gen.Class('Marshal implements IMarshal, IHandlePacket', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.marshal_cls.attributes.append(
            gen.Attribute('Marshal', 'instance', decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)
        )
        self.marshal_file.add(self.marshal_cls)

        # Flush IClient 
        self.client_itf = gen.Class('IClient extends IBaseClient', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value], keyword='interface')
        self.client_file.add(self.client_itf)

        # RPC class
        self.rpc_cls = gen.Class('Rpc', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.rpc_file.add(self.rpc_cls)

    def _base_message_fields(self, base):
        if base == 'has_id':
            return [
                boxes.DeclarationBox(boxes.TypeBox(boxes.IdentifierBox('uint64')), boxes.IdentifierBox('id'), False)
            ]
        return []

    def __is_trivial(self, message: boxes.MessageBox):
        for decl in self.message_fields_including_base(message):
            # Optional implies we might have variant sizes
            if decl.optional:
                return False

            dtype = decl.dtype.dtype.eval()

            # Vectors are runtime only
            if dtype in ('vector', 'string'):
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
            ctype = TYPE_CONVERSION[dtype]
            return gen.Statement(f'packet.getData().write(({ctype}){variable})')

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
                gen.Statement(f'packet.getData().write((byte){variable}.size())'),
                gen.Statement(f'for ({ctype} val : {variable})', ending=''),
                gen.Block([
                    self.__write_value(decl.dtype.spec.eval(), 'val')
                ])
            ])
        
        return self.__write_value(dtype, variable)

    def __read_type(self, decl, variable, is_optional=False):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            varname = decl.name.eval()
            inner = decl.dtype.spec.eval()

            if not self.is_message(inner):
                ctype = TYPE_CONVERSION[inner]
                set_value = f'new {TYPE_CONVERSION["vector"]}<{TYPE_CONVERSION[inner]}>()'
                if is_optional:
                    set_value = f'{variable}.setValue({set_value})'
                    get_value = f'{variable}.getValue()'
                else:
                    set_value = f'{variable} = {set_value}'
                    get_value = variable

                return gen.Scope([
                    gen.Statement(f'int size_{varname} = Byte.toUnsignedInt(packet.getData().readByte())'),
                    gen.Statement(f'if (packet.bytesRead() + size_{varname} * marshal.size({ctype}.class) > packet.bufferSize())', ending=''),
                    gen.Block([
                        gen.Statement('return false')
                    ]),
                    gen.Statement(set_value),
                    gen.Statement(f'for (int i = 0; i < size_{varname}; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{get_value}.add(packet.getData().read{TYPE_CONVERSION[inner]}())')
                    ])
                ])
            else:
                inner = to_camel_case(inner)

                set_value = f'new {TYPE_CONVERSION["vector"]}<{inner}>()'
                if is_optional:
                    set_value = f'{variable}.setValue({set_value})'
                    get_value = f'{variable}.getValue()'
                else:
                    set_value = f'{variable} = {set_value}'
                    get_value = variable
                
                return gen.Scope([
                    gen.Statement(f'int size_{varname} = Byte.toUnsignedInt(packet.getData().readByte())'),
                    gen.Statement(set_value),
                    gen.Statement(f'for (int i = 0; i < size_{varname}; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{inner} data = new {inner}()'),
                        gen.Statement(f'if (data.unpack(marshal, packet))', ending=''),
                        gen.Block([
                            gen.Statement(f'{get_value}.add(data)')
                        ]),
                        gen.Statement(f'else'),
                        gen.Block([
                            gen.Statement('return false')
                        ])
                    ])
                ])

        if self.is_message(dtype):
            dtype = to_camel_case(dtype)

            set_value = f'new {dtype}()'
            if is_optional:
                set_value = f'{variable}.setValue({set_value})'
            else:
                set_value = f'{variable} = {set_value}'

            return gen.Scope([
                gen.Statement(set_value),
                gen.Statement(f'if (!{variable}.unpack(marshal, packet))', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ])
            ])

        ctype = TYPE_CONVERSION[dtype]

        if dtype == 'string':
            set_value = f'packet.getData().read{ctype}()'
            if is_optional:
                set_value = f'{variable}.setValue({set_value})'
            else:
                set_value = f'{variable} = {set_value}'
            
            return gen.Scope([
                gen.Statement(f'if (packet.bytesRead() + marshal.size(Byte.class) > packet.bufferSize())', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ]),
                gen.Statement(f'if (packet.bytesRead() + marshal.size(Byte.class) + packet.getData().peekByte() > packet.bufferSize())', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ]),
                gen.Statement(set_value)
            ])


        set_value = f'packet.getData().read{ctype}()'
        if is_optional:
            set_value = f'{variable}.setValue({set_value})'
        else:
            set_value = f'{variable} = {set_value}'
            
        return gen.Scope([
            gen.Statement(f'if (packet.bytesRead() + marshal.size({ctype}.class) > packet.bufferSize())', ending=''),
            gen.Block([
                gen.Statement('return false')
            ]),
            gen.Statement(set_value)
        ])

    def __read_type_unsafe(self, decl, variable, is_optional=False):
        dtype = decl.dtype.dtype.eval()
        if dtype in ('vector', 'string'):
            raise NotImplementedError('Unsafe reading cannot read vectors')

        if self.is_message(dtype):
            dtype = to_camel_case(dtype)

            set_value = f'new {dtype}()'
            if is_optional:
                set_value = f'{variable}.setValue({set_value})'
            else:
                set_value = f'{variable} = {set_value}'

            return gen.Scope([
                gen.Statement(set_value),
                gen.Statement(f'{variable}.unpack(marshal, packet)', ending='')
            ])


        ctype = TYPE_CONVERSION[dtype]
        set_value = f'packet.getData().read{ctype}()'
        if is_optional:
            set_value = f'{variable}.setValue({set_value})'
        else:
            set_value = f'{variable} = {set_value}'
            
        return gen.Scope([
            gen.Statement(set_value)
        ])
    
    def __write_size(self, this, decl, variable):
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
                return gen.Statement(f'size += Byte.BYTES + {variable}.size() * {this}.size({ctype}.class)')
            # Case 2
            else:
                return gen.Scope([
                    gen.Statement('size += Byte.BYTES'),
                    gen.Statement(f'for ({ctype} val : {variable})', ending=''),
                    gen.Block([
                        gen.Statement(f'size += val.size({this})')
                    ])
                ])
            
        elif self.is_message(dtype):
            return gen.Statement(f'size += {variable}.size({this})')
        elif dtype == 'string':
            return gen.Statement(f'size += {this}.size(Byte.class) + {variable}.length()')
        else:
            ctype = TYPE_CONVERSION[dtype]
            return gen.Statement(f'size += {this}.size({ctype}.class)')
        
    def _generate_structure(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        base_name = None
        base = ' implements IData'
        if message.base.name is not None:
            base_name = message.base.name.eval()

            # TODO(gpascualg): This is not really elegant
            if base_name == 'has_id':
                base = f' implements IHasId'
            else:
                base = f' extends {to_camel_case(base_name)}'

        struct = gen.Class(to_camel_case(message_name), decl_name_base=base, csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        for decl in it.chain(self._base_message_fields(base_name), message.fields.eval()) :
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

        self.all_structs[to_camel_case(message_name)] = struct
        self.__generate_base_methods(struct, base_name)
        self.__generate_message_packer(message, struct)
        self.__generate_message_unpacker(message, struct)
        self.__generate_message_size(message, struct)

    # Java doesn't generate base structures but implements them in the same struct
    def _generate_base_structure(self, base):
        pass

    def __generate_base_methods(self, struct: gen.Class, base_name: str):
        if base_name != 'has_id':
            return

        method = gen.Method('Long', f'getId', [], visibility=gen.Visibility.PUBLIC)
        method.append(gen.Statement('return id'))
        struct.methods.append(method)

        method = gen.Method('void', f'setId', [
            gen.Variable('Long', 'id')
        ], visibility=gen.Visibility.PUBLIC)
        method.append(gen.Statement('this.id = id'))
        struct.methods.append(method)

    def __generate_message_packer(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        method = gen.Method('void', f'pack', [
            gen.Variable('IMarshal', 'marshal'),
            gen.Variable('Packet', 'packet')
        ], visibility=gen.Visibility.PUBLIC)

        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'packet.getData().write(this.{name}.hasValue())'))
                method.append(gen.Statement(f'if (this.{name}.hasValue())', ending=''))
                method.append(gen.Block([
                    self.__write_type(decl, f'this.{name}.getValue()')
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

        if self.__is_trivial(message):
            method.append(gen.Statement(f'if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())', ending=''))
            method.append(gen.Block([
                gen.Statement('return false')
            ]))

            for decl in self.message_fields_including_base(message):
                name = decl.name.eval()
                method.append(self.__read_type_unsafe(decl, f'this.{name}'))
        else:
            for decl in self.message_fields_including_base(message):
                name = decl.name.eval()

                if decl.optional:
                    method.append(gen.Statement(f'if (packet.bytesRead() + Byte.BYTES > packet.bufferSize())', ending=''))
                    method.append(gen.Block([
                        gen.Statement('return false')
                    ]))
                    
                    method.append(gen.Statement(f'if (packet.getData().readByte() == 1)', ending=''))
                    method.append(gen.Block([
                        self.__read_type(decl, f'this.{name}', True)
                    ]))
                else:
                    method.append(self.__read_type(decl, f'this.{name}'))
    
        method.append(gen.Statement('return true'))
        struct.methods.append(method)

    def __generate_message_size(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        # Even if messages are trivial, there is no such thing as sizeof
        # Thus we must always iterate over everything
        if self.__is_trivial(message):
            self.trivial_messages[message_name] = message

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
                method.append(gen.Statement('size += Byte.BYTES'))
                method.append(gen.Statement(f'if (this.{name}.hasValue())', ending=''))
                method.append(gen.Block([
                    self.__write_size('marshal', decl, f'this.{name}.getValue()')
                ]))
            else:
                method.append(self.__write_size('marshal', decl, f'this.{name}'))

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
            ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
            method.append(gen.Statement(f'pq.send{to_camel_case(queue)}(Opcodes.opcode{to_camel_case(program_name)}, data, callback)'))
            methods.append(method)
        
        # Standard no callback method
        method = gen.Method('void', f'send{to_camel_case(program_name)}', [
            gen.Variable(f'ProtocolQueues', 'pq'),
            gen.Variable(f'{message_name}', 'data')
        ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
        method.append(gen.Statement(f'pq.send{to_camel_case(queue)}(Opcodes.opcode{to_camel_case(program_name)}, data)'))
        methods.append(method)
        
        # There are two types of broadcasts, one that implies neighbouring areas
        # and one that doesn't, generate both
        for suffix in ('', 'Single'):
            if self.has_queue_packed_add(self.queues[queue]):
                
                if self.can_queue_have_callback(self.queues[queue]):
                    method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                        gen.Variable('IBroadcaster<ProtocolQueues>', 'broadcaster'),
                        gen.Variable(f'{message_name}', 'data'),
                        gen.Variable('IAckCallback', 'callback')
                    ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                    methods.append(method)

                    method.append(gen.Statement(f'Packet packet = Packet.make(Opcodes.opcode{to_camel_case(program_name)}, callback)'))
                    method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                    method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {', ending=''))
                    method.append(gen.Scope([
                        gen.Statement('public void onCandidate(ProtocolQueues pq) {', ending=''),
                        gen.Scope([
                            gen.Statement(f'pq.send{to_camel_case(queue)}(packet)')
                        ], indent=True),
                        gen.Statement('}', ending='')
                    ], indent=True)),
                    method.append(gen.Statement('})'))
                
                # No callback
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement(f'Packet packet = Packet.make(Opcodes.opcode{to_camel_case(program_name)})'))
                method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {', ending=''))
                method.append(gen.Scope([
                    gen.Statement('public void onCandidate(ProtocolQueues pq) {', ending=''),
                    gen.Scope([
                        gen.Statement(f'pq.send{to_camel_case(queue)}(packet)')
                    ], indent=True),
                    gen.Statement('}', ending='')
                ], indent=True)),
                method.append(gen.Statement('})'))

            else:
                # Adding by bare data is always available
                # But we can not have callbacks YET
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement('broadcaster.broadcast(new IBroadcastOperation<ProtocolQueues>() {', ending=''))
                method.append(gen.Scope([
                    gen.Statement('void onCandidate(ProtocolQueues pq) {', ending=''),
                    gen.Scope([
                        gen.Statement(f'pq.send{to_camel_case(queue)}(Opcodes.opcode{to_camel_case(program_name)}, data)')
                    ], indent=True),
                    gen.Statement('}', ending='')
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
            method.append(gen.Statement(f'if (!client.check(client, "{attr}", {value}))', ending=''))
            method.append(gen.Block([
                gen.Statement(f'return {false_case}(client, packet.getOpcode())')
            ]))
        
        method.append(gen.Statement(f'{to_camel_case(message_name)} data = new {to_camel_case(message_name)}()'))
        method.append(gen.Statement(f'if (!data.unpack(marshal, packet))', ending=''))
        method.append(gen.Block([
            gen.Statement('return false')
        ]))

        method.append(gen.Statement(f'return client.on{to_camel_case(program_name)}(data, packet.timestamp())'))

        self.handler_programs.add(program_name)
        self.marshal_cls.methods.append(method)

        return [method]

    def _generate_internals(self):
        # Marshal size method
        method = gen.Method('<T> int', f'size', [
            gen.Variable('Class<T>', 'cls')
        ], visibility=gen.Visibility.PUBLIC)
        self.marshal_cls.methods.append(method)

        for message_name, message in self.trivial_messages.items():
            method.append(gen.Statement(f'if (cls == {to_camel_case(message_name)}.class)', ending=''))
            method.append(gen.Block([
                gen.Statement('int size = 0'),
                *[
                    self.__write_size('this', decl, f'this.{name}') for decl, name in \
                        ((decl, decl.name.eval()) for decl in self.message_fields_including_base(message))
                ],
                gen.Statement('return size')
            ]))

        # Trivial types size
        for dtype in semantic.TRIVIAL_TYPES:
            ctype = TYPE_CONVERSION[dtype]
            method.append(gen.Statement(f'if (cls == {ctype}.class)', ending=''))
            method.append(gen.Block([
                gen.Statement('return Byte.BYTES') if dtype == 'bool' else gen.Statement(f'return {ctype.capitalize()}.BYTES')
            ]))

        method.append(gen.Statement('return 0'))

        # General packet handler
        method = gen.Method('<T extends IBaseClient> boolean', 'handlePacket', [
            gen.Variable('PacketReader', 'packet'),
            gen.Variable('T', 'client')
        ], visibility=gen.Visibility.PUBLIC)

        method.append(gen.Statement('switch (packet.getOpcode())', ending=''))
        method.append(gen.Block([
            gen.Scope([
                gen.Statement(f'case Opcodes.opcode{to_camel_case(program)}:', ending=''),
                gen.Scope([
                    gen.Statement(f'return handle{to_camel_case(program)}(this, packet, (IClient)client)') 
                ], indent=True)
            ]) for program in self.handler_programs
        ] + [gen.Scope([
            gen.Statement(f'default:', ending=''),
            gen.Scope([
                gen.Statement(f'return false') 
            ], indent=True)
        ])]))

        self.marshal_cls.methods.append(method)

        # IClient
        for program_name in self.handler_programs:
            program = self.programs[program_name]
            message = self.get_program_message(program)
            self.client_itf.methods.append(gen.Method(
                'boolean', 
                f'on{to_camel_case(program_name)}',
                [
                    gen.Variable(to_camel_case(message), 'data'), 
                    gen.Variable('long', 'timestamp')
                ],
                visibility=gen.Visibility.PUBLIC,
                interface=True
            ))

        # Opcodes enum
        opcodes = gen.Class('Opcodes', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        for program in self.programs.values():
            program_name = program.name.eval()
            name = f'opcode{to_camel_case(program_name)}'

            opcodes.attributes.append(
                gen.Attribute(
                    'short', 
                    f'{name: <24}', 
                    f'0x{self.opcodes[program_name]}',
                    ['static', 'final'],
                    visibility=gen.Visibility.PUBLIC,
                )
            )
            
        self.opcodes_file.add(opcodes)

        # Protocol queues
        queues = gen.Class('ProtocolQueues implements IProtocolQueues', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.queues_file.add(queues)
        
        constructor = gen.Method('', 'ProtocolQueues', [
            gen.Variable('int', 'resendThreshold')
        ], visibility=gen.Visibility.PUBLIC)
        queues.methods.append(constructor)

        reset = gen.Method('void', 'reset', visibility=gen.Visibility.PUBLIC)
        reset.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.clear()') for queue in self.queues.keys()
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
            gen.Statement(f'{to_camel_case(queue, False)}.process(Marshal.instance, blockId, remaining, byBlock)') for queue in self.queues.keys()
        ]))
        queues.methods.append(process)

        for queue_name, queue in self.queues.items():
            # Attribute
            queue_base = queue.base.subtype.eval()
            queue_packer = 'ImmediatePacker'
            queue_packer_template = 'ImmediatePacker, Packet'
            queue_packer_args = ''

            if queue.specifier.queue_type == boxes.QueueSpecifierType.SPECIALIZED:
                queue_packer = to_camel_case(queue.specifier.args.eval())
                queue_packer_template = f'{queue_packer}, Packet'

            elif queue.specifier.queue_type == boxes.QueueSpecifierType.TEMPLATED:
                queue_packer = 'UniqueMergePacker'
                args = queue.specifier.args
                global_dtype = to_camel_case(args[0].eval())
                program_name = args[2].eval()
                data_dtype = to_camel_case(args[1].eval())

                queue_packer_template = f'{queue_packer}<{global_dtype}, {data_dtype}>, {data_dtype}'
                queue_packer_args = f'{global_dtype}.class, Opcodes.opcode{to_camel_case(progam_name)}'

            if queue.base.argument is not None:
                queue_packer_args = queue.base.argument.eval()

            queue_qualified_name = f'{to_camel_case(queue_base)}<{queue_packer_template}>'

            constructor.append(
                gen.Statement(f'{to_camel_case(queue_name, False)} = new {queue_qualified_name}(new {queue_packer}({queue_packer_args}))')
            )

            queues.attributes.append(gen.Attribute(
                queue_qualified_name,
                f'{to_camel_case(queue_name, False)}'
            ))

            # General send with data
            if self.can_queue_have_callback(queue):
                send = gen.Method('void', f'send{to_camel_case(queue_name)}', [
                    gen.Variable('Short', 'opcode'),
                    gen.Variable(f'IData', 'data'),
                    gen.Variable('IAckCallback', 'callback')
                ], visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(Marshal.instance, opcode, data, callback)'))
                queues.methods.append(send)
            
            send = gen.Method('void', f'send{to_camel_case(queue_name)}', [
                gen.Variable('Short', 'opcode'),
                gen.Variable(f'IData', 'data')
            ], visibility=gen.Visibility.PUBLIC)
            send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(Marshal.instance, opcode, data, new NoCallback())'))
            queues.methods.append(send)

            if self.has_queue_packed_add(queue):
                send = gen.Method('void', f'send{to_camel_case(queue_name)}', [
                    gen.Variable('Packet', 'packet')
                ], visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(packet)'))
                queues.methods.append(send)
    
    def _generate_version(self, version):
        config = gen.Class('Config', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        config.attributes.append(gen.Attribute('Integer', 'VERSION', f'0x{version}', decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC))
        self.config_file.add(config)

    def dump(self, path):
        package = self.config['package'] + '.kumo'
        kaminari = self.config['kaminari']
        path = os.path.join(path.replace('\\', '/'), package.replace('.', '/'))

        try:
            shutil.rmtree(path)
        except:
            pass

        os.mkdir(path)
        os.mkdir(os.path.join(path, 'structs'))

        with open(f'{path}/IClient.java', 'w') as fp:
            fp.write(self.client_file.source([
                gen.Statement(f'package {package}'),
                *[
                    gen.Statement(f'import {package}.structs.{name}') for name in self.all_structs.keys()
                ],
                gen.Statement(f'import {kaminari}.IBaseClient')
            ]))

        with open(f'{path}/Marshal.java', 'w') as fp:
            fp.write(self.marshal_file.source([
                gen.Statement(f'package {package}'),
                *[
                    gen.Statement(f'import {package}.structs.{name}') for name in self.all_structs.keys()
                ],
                gen.Statement(f'import {package}.IClient'),
                gen.Statement(f'import {kaminari}.Packet'),
                gen.Statement(f'import {kaminari}.PacketReader'),
                gen.Statement(f'import {kaminari}.IMarshal'),
                gen.Statement(f'import {kaminari}.IBaseClient'),
                gen.Statement(f'import {kaminari}.IHandlePacket')
            ]))

        with open(f'{path}/Rpc.java', 'w') as fp:
            fp.write(self.rpc_file.source([
                gen.Statement(f'package {package}'),
                *[
                    gen.Statement(f'import {package}.structs.{name}') for name in self.all_structs.keys()
                ],
                gen.Statement(f'import {kaminari}.IAckCallback'),
                gen.Statement(f'import {kaminari}.IBroadcaster'),
                gen.Statement(f'import {kaminari}.IBroadcastOperation'),
                gen.Statement(f'import {kaminari}.Packet')
            ]))

        for struct_name, struct in self.all_structs.items():
            with open(f'{path}/structs/{struct_name}.java', 'w') as fp:
                structs_file = File()
                structs_file.add(struct)

                fp.write(structs_file.source([
                    gen.Statement(f'package {package}.structs'),
                    gen.Statement(f'import java.util.ArrayList'),
                    gen.Statement(f'import java.util.TreeMap'),
                    gen.Statement(f'import {kaminari}.Packet'),
                    gen.Statement(f'import {kaminari}.PacketReader'),
                    gen.Statement(f'import {kaminari}.Optional'),
                    gen.Statement(f'import {kaminari}.IMarshal'),
                    gen.Statement(f'import {kaminari}.packers.IData'),
                    gen.Statement(f'import {kaminari}.packers.IHasId'),
                    gen.Statement(f'import {kaminari}.packers.IHasDataVector')
                ]))

        with open(f'{path}/Opcodes.java', 'w') as fp:
            fp.write(self.opcodes_file.source([
                gen.Statement(f'package {package}')
            ]))

        with open(f'{path}/ProtocolQueues.java', 'w') as fp:
            fp.write(self.queues_file.source([
                gen.Statement(f'package {package}'),
                gen.Statement(f'import java.util.ArrayList'),
                gen.Statement(f'import java.util.TreeMap'),
                gen.Statement(f'import {kaminari}.Constants'),
                gen.Statement(f'import {kaminari}.IAckCallback'),
                gen.Statement(f'import {kaminari}.NoCallback'),
                gen.Statement(f'import {kaminari}.IMarshal'),
                gen.Statement(f'import {kaminari}.IProtocolQueues'),
                gen.Statement(f'import {kaminari}.packers.IData'),
                gen.Statement(f'import {kaminari}.Overflow'),
                gen.Statement(f'import {kaminari}.Packet'),
                gen.Statement(f'import {kaminari}.Ref'),
                gen.Statement(f'import {kaminari}.queues.ReliableQueue'),
                gen.Statement(f'import {kaminari}.queues.UnreliableQueue'),
                gen.Statement(f'import {kaminari}.queues.EventuallySyncedQueue'),
                gen.Statement(f'import {kaminari}.packers.ImmediatePacker'),
                gen.Statement(f'import {kaminari}.packers.OrderedPacker'),
                gen.Statement(f'import {kaminari}.packers.MergePacker'),
                gen.Statement(f'import {kaminari}.packers.MostRecentPackerWithId')
            ]))

        with open(f'{path}/Config.java', 'w') as fp:
            fp.write(self.config_file.source([
                gen.Statement(f'package {package}')
            ]))
        