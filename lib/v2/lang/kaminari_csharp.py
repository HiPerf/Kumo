from .. import generator
from .. import gen
from .. import boxes
from .. import semantic

import os
import sys
import itertools as it
import shutil


TYPE_CONVERSION = {
    'uint8':    'byte',
    'uint16':   'ushort',
    'uint32':   'uint',
    'uint64':   'ulong',
    'int8':     'sbyte',
    'int16':    'short',
    'int32':    'int',
    'int64':    'long',
    'float':    'float',
    'double':   'double',
    'bool':     'bool',
    'vector':   'List',
    'optional': 'Optional',
    'string': 'string'
}

def to_camel_case(snake_str, capitalize=True):
    components = snake_str.split('_')
    leading = components[0]
    if capitalize:
        leading = leading.capitalize()
    return leading + ''.join(x.capitalize() for x in components[1:])

class File(object):
    def __init__(self, namespace=None):
        self.sources = []
        self.namespace = namespace

    def add(self, code):
        self.sources.append(code)

    def source(self, prepend=[]):
        if self.namespace is not None:
            return gen.Scope(prepend + [
                gen.Statement(f'namespace {self.namespace}', ending=''),
                gen.Block(self.sources)
            ]).both(0)
        else:
            return gen.Scope(prepend + self.sources).both(0)
    
    def __str__(self):
        return self.source()


class LangGenerator(generator.Generator):
    def __init__(self, config, role, queues, messages, programs):
        super().__init__(config, role, queues, messages, programs)
        
        # Some helpers
        self.handler_programs = set()

        # Output code
        self.marshal_file = File(namespace='Kumo')
        self.client_file = File(namespace='Kumo')
        self.opcodes_file = File(namespace='Kumo')
        self.unsafe_rpc_file = File(namespace='Kumo')
        self.rpc_file = File(namespace='Kumo')
        self.queues_file = File(namespace='Kumo')
        self.config_file = File(namespace='Kumo')

        # Needs processing at the end
        self.trivial_messages = {}
        self.all_structs = {}

        # Flush marshal class already
        self.marshal_cls = gen.Class('Marshal : Kaminari.IMarshal, Kaminari.IHandlePacket', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.marshal_cls.attributes.append(
            gen.Attribute('Marshal', 'instance', decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)
        )
        self.marshal_file.add(self.marshal_cls)

        data_struct = gen.Class('DataBuffer<T>', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value], postfix=' where T : new()')
        data_struct.attributes.append(gen.Attribute('T', 'Data', visibility=gen.Visibility.PUBLIC))
        data_struct.attributes.append(gen.Attribute('ushort', 'BlockId', visibility=gen.Visibility.PUBLIC))
        data_struct.attributes.append(gen.Attribute('ulong', 'Timestamp', visibility=gen.Visibility.PUBLIC))
        self.marshal_file.add(data_struct)

        # Helper method for marhsal
        method = gen.Method('T', f'emplaceData<T>', [
            gen.Variable('SortedList<ushort, DataBuffer<T>>', 'buffer'),
            gen.Variable('ushort', 'blockId'),
            gen.Variable('ulong', 'timestamp')
        ], visibility=gen.Visibility.PROTECTED, postfix=' where T : new()')
        self.marshal_cls.methods.append(method)

        method.append(gen.Statement('var data = new DataBuffer<T>', ending=''))
        method.append(gen.Block([
            gen.Statement('BlockId = blockId', ending=','),
            gen.Statement('Timestamp = timestamp', ending=','),
            gen.Statement('Data = new T()', ending='')
        ], ending=';'))
        method.append(gen.Statement('buffer.Add(blockId, data)'))
        method.append(gen.Statement('return data.Data'))

        # Helper method for marhsal
        method = gen.Method('bool', f'checkBuffer<T>', [
            gen.Variable('SortedList<ushort, DataBuffer<T>>', 'buffer'),
            gen.Variable('ushort', 'blockId'),
            gen.Variable('byte', 'bufferSize')
        ], visibility=gen.Visibility.PROTECTED, postfix=' where T : new()')
        self.marshal_cls.methods.append(method)

        method.append(gen.Statement('return buffer.Count > 0 && Kaminari.Overflow.le(buffer.Values[0].BlockId, Kaminari.Overflow.sub(blockId, (ushort)bufferSize))'))

        # Flush IClient 
        self.client_itf = gen.Class('IClient : Kaminari.IBaseClient', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value], keyword='interface')
        self.client_file.add(self.client_itf)

        # RPC class
        self.unsafe_rpc_cls = gen.Class('Unsafe', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.unsafe_rpc_file.add(self.unsafe_rpc_cls)
        
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
                gen.Statement(f'packet.getData().write((byte){variable}.Count)'),
                gen.Statement(f'foreach ({ctype} val in {variable})', ending=''),
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
                    gen.Statement(f'int size_{varname} = packet.getData().readByte()'),
                    gen.Statement(f'if (packet.bytesRead() + size_{varname} * marshal.size<{ctype}>() > packet.bufferSize())', ending=''),
                    gen.Block([
                        gen.Statement('return false')
                    ]),
                    gen.Statement(set_value),
                    gen.Statement(f'for (int i = 0; i < size_{varname}; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{get_value}.Add(packet.getData().read{TYPE_CONVERSION[inner].capitalize()}())')
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
                    gen.Statement(f'int size_{varname} = packet.getData().readByte()'),
                    gen.Statement(set_value),
                    gen.Statement(f'for (int i = 0; i < size_{varname}; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{inner} data = new {inner}()'),
                        gen.Statement(f'if (data.unpack(marshal, packet))', ending=''),
                        gen.Block([
                            gen.Statement(f'{get_value}.Add(data)')
                        ]),
                        gen.Statement(f'else', ending=''),
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
            set_value = f'packet.getData().read{ctype.capitalize()}()'
            if is_optional:
                set_value = f'{variable}.setValue({set_value})'
            else:
                set_value = f'{variable} = {set_value}'
            
            return gen.Scope([
                gen.Statement(f'if (packet.bytesRead() + marshal.size<byte>() > packet.bufferSize())', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ]),
                gen.Statement(f'if (packet.bytesRead() + marshal.size<byte>() + packet.getData().peekByte() > packet.bufferSize())', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ]),
                gen.Statement(set_value)
            ])


        set_value = f'packet.getData().read{ctype.capitalize()}()'
        if is_optional:
            set_value = f'{variable}.setValue({set_value})'
        else:
            set_value = f'{variable} = {set_value}'
            
        return gen.Scope([
            gen.Statement(f'if (packet.bytesRead() + marshal.size<{ctype}>() > packet.bufferSize())', ending=''),
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
        set_value = f'packet.getData().read{ctype.capitalize()}()'
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
                return gen.Statement(f'size += sizeof(byte) + {variable}.Count * {this}.size<{ctype}>()')
            # Case 2
            else:
                return gen.Scope([
                    gen.Statement('size += sizeof(byte)'),
                    gen.Statement(f'foreach ({ctype} val in {variable})', ending=''),
                    gen.Block([
                        gen.Statement(f'size += val.size({this})')
                    ])
                ])
            
        elif self.is_message(dtype):
            return gen.Statement(f'size += {variable}.size({this})')
        elif dtype == 'string':
            return gen.Statement(f'size += {this}.size<byte>() + {variable}.Length')
        else:
            ctype = TYPE_CONVERSION[dtype]
            return gen.Statement(f'size += {this}.size<{ctype}>()')
        
    def _generate_structure(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        base_name = None
        base = ' : Kaminari.IData'
        if message.base.name is not None:
            base_name = message.base.name.eval()

            # TODO(gpascualg): This is not really elegant
            if base_name == 'has_id':
                base = f' : Kaminari.IHasId'
            elif base_name == 'has_data_vector':
                base = f' : Kaminari.IHasDataVector<Kumo.{to_camel_case(message.base.template.eval())}>'
            else:
                base = f' : {to_camel_case(base_name)}'

        struct = gen.Class(to_camel_case(message_name), decl_name_base=base, csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        for decl in self.message_fields_including_base_and_ignored(message):
            dtype = decl.dtype.dtype.eval()
            ctype = '{}'
            if decl.optional:
                ctype = 'Kaminari.Optional<{}>'

            temp = dtype
            if dtype == 'vector':
                ctype = ctype.format('List<{}>')
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
        self.__generate_base_methods(struct, base_name, message.base)
        self.__generate_message_packer(message, struct)
        self.__generate_message_unpacker(message, struct)
        self.__generate_message_size(message, struct)

    # Java doesn't generate base structures but implements them in the same struct
    def _generate_base_structure(self, base):
        pass

    def __generate_base_methods(self, struct: gen.Class, base_name: str, base: boxes.MessageBaseBox):
        if base_name == 'has_id':
            method = gen.Method('ulong', f'getId', [], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement('return id'))
            struct.methods.append(method)

            method = gen.Method('void', f'setId', [
                gen.Variable('ulong', 'id')
            ], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement('this.id = id'))
            struct.methods.append(method)

        elif base_name == 'has_data_vector':
            method = gen.Method('void', f'initialize', [], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'data = new List<Kumo.{to_camel_case(base.template.eval())}>()'))
            struct.methods.append(method)

            method = gen.Method(f'List<Kumo.{to_camel_case(base.template.eval())}>', f'getData', [], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement('return data'))
            struct.methods.append(method)

    def __generate_message_packer(self, message: boxes.MessageBox, struct: gen.Class):
        message_name = message.name.eval()

        method = gen.Method('void', f'pack', [
            gen.Variable('Kaminari.IMarshal', 'marshal'),
            gen.Variable('Kaminari.Packet', 'packet')
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

        method = gen.Method('bool', f'unpack', [
            gen.Variable(f'Kaminari.IMarshal', 'marshal'),
            gen.Variable('Kaminari.PacketReader', 'packet')
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
                    method.append(gen.Statement(f'if (packet.bytesRead() + sizeof(byte) > packet.bufferSize())', ending=''))
                    method.append(gen.Block([
                        gen.Statement('return false')
                    ]))

                    dtype = decl.dtype.dtype.eval()
                    if dtype == 'vector':
                        inner = decl.dtype.spec.eval()                        
                        if not self.is_message(inner):
                            inner = TYPE_CONVERSION[inner]

                        dtype = f'{TYPE_CONVERSION["vector"]}<{inner}>'
                    elif not self.is_message(dtype):
                        dtype = TYPE_CONVERSION[dtype]
                    
                    method.append(gen.Statement(f'this.{name} = new Kaminari.Optional<{dtype}>()'))
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
            gen.Variable(f'Kaminari.IMarshal', 'marshal')
        ], visibility=gen.Visibility.PUBLIC)
        struct.methods.append(method)

        method.append(gen.Statement('int size = 0'))    
        # Manually loop all types
        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement('size += sizeof(byte)'))
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
        return self._generate_unsafe_send(program) + self._generate_safe_send(program)

    def _generate_unsafe_send(self, program: boxes.ProgramBox):
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
                gen.Variable('Action', 'callback')
            ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
            method.append(gen.Statement(f'pq.send{to_camel_case(queue)}((ushort)Opcodes.opcode{to_camel_case(program_name)}, data, callback)'))
            methods.append(method)
        
        # Standard no callback method
        method = gen.Method('void', f'send{to_camel_case(program_name)}', [
            gen.Variable(f'ProtocolQueues', 'pq'),
            gen.Variable(f'{message_name}', 'data')
        ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
        method.append(gen.Statement(f'pq.send{to_camel_case(queue)}((ushort)Opcodes.opcode{to_camel_case(program_name)}, data)'))
        methods.append(method)
        
        # There are two types of broadcasts, one that implies neighbouring areas
        # and one that doesn't, generate both
        for suffix in ('', 'Single'):
            if self.has_queue_packed_add(self.queues[queue]):
                
                if self.can_queue_have_callback(self.queues[queue]):
                    method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                        gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                        gen.Variable(f'{message_name}', 'data'),
                        gen.Variable('Action', 'callback')
                    ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                    methods.append(method)

                    method.append(gen.Statement(f'Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcode{to_camel_case(program_name)}, callback)'))
                    method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                    method.append(gen.Statement(f'broadcaster.broadcast((ProtocolQueues pq) => pq.send{to_camel_case(queue)}(packet))'))
                
                # No callback
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement(f'Kaminari.Packet packet = Kaminari.Packet.make((ushort)Opcodes.opcode{to_camel_case(program_name)})'))
                method.append(gen.Statement(f'data.pack(Marshal.instance, packet)'))
                method.append(gen.Statement(f'broadcaster.broadcast((ProtocolQueues pq) => pq.send{to_camel_case(queue)}(packet))'))

            else:
                # Adding by bare data is always available
                # But we can not have callbacks YET
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement(f'broadcaster.broadcast((ProtocolQueues pq) => pq.send{to_camel_case(queue)}((ushort)Opcodes.opcode{to_camel_case(program_name)}, data))'))
            
        for method in methods:
            self.unsafe_rpc_cls.methods.append(method)

        return methods

    def _generate_safe_send(self, program: boxes.ProgramBox):
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
                gen.Variable(f'Kaminari.Client<ProtocolQueues>', 'client'),
                gen.Variable(f'{message_name}', 'data'),
                gen.Variable('Action', 'callback')
            ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
            method.append(gen.Statement(f'client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.send{to_camel_case(program_name)}(client.getSuperPacket().getQueues(), data, callback))'))
            methods.append(method)
        
        # Standard no callback method
        method = gen.Method('void', f'send{to_camel_case(program_name)}', [
            gen.Variable(f'Kaminari.Client<ProtocolQueues>', 'client'),
            gen.Variable(f'{message_name}', 'data')
        ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
        method.append(gen.Statement(f'client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.send{to_camel_case(program_name)}(client.getSuperPacket().getQueues(), data))'))
        methods.append(method)
        
        # There are two types of broadcasts, one that implies neighbouring areas
        # and one that doesn't, generate both
        for suffix in ('', 'Single'):
            if self.has_queue_packed_add(self.queues[queue]):
                
                if self.can_queue_have_callback(self.queues[queue]):
                    method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                        gen.Variable(f'Kaminari.Client<ProtocolQueues>', 'client'),
                        gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                        gen.Variable(f'{message_name}', 'data'),
                        gen.Variable('Action', 'callback')
                    ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                    methods.append(method)

                    method.append(gen.Statement(f'client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcast{to_camel_case(program_name)}{suffix}(broadcaster, data, callback))'))
                
                # No callback
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable(f'Kaminari.Client<ProtocolQueues>', 'client'),
                    gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement(f'client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcast{to_camel_case(program_name)}{suffix}(broadcaster, data))'))

            else:
                # Adding by bare data is always available
                # But we can not have callbacks YET
                method = gen.Method('void', f'broadcast{to_camel_case(program_name)}{suffix}', [
                    gen.Variable(f'Kaminari.Client<ProtocolQueues>', 'client'),
                    gen.Variable('Kaminari.IBroadcaster<ProtocolQueues>', 'broadcaster'),
                    gen.Variable(f'{message_name}', 'data')
                ], visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])
                methods.append(method)

                method.append(gen.Statement(f'client.getProtocol().getPhaseSync().OneShot(() => Kumo.Unsafe.broadcast{to_camel_case(program_name)}{suffix}(broadcaster, data))'))
            
        for method in methods:
            self.rpc_cls.methods.append(method)

        return methods
    
    def _generate_program_recv(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        message_name = self.get_program_message(program)

        method = gen.Method('bool', f'handle{to_camel_case(program_name)}', [
            gen.Variable('Kaminari.IMarshal', 'marshal'),
            gen.Variable('Kaminari.PacketReader', 'packet'),
            gen.Variable('IClient', 'client'),
            gen.Variable('ushort', 'blockId')
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
        
        method.append(gen.Statement(f'if ({to_camel_case(program_name, capitalize=False)}SinceLastCalled < 100 && Kaminari.Overflow.le(blockId, {to_camel_case(program_name, capitalize=False)}LastCalled))', ending=''))
        method.append(gen.Block([
            gen.Statement('// TODO: Returning true here means the packet is understood as correctly parsed, while we are ignoring it', ending=''),
            gen.Statement('return true')
        ]))

        method.append(gen.Statement(f'var data = emplaceData({to_camel_case(program_name, capitalize=False)}, blockId, packet.timestamp())'))
        method.append(gen.Statement(f'if (!data.unpack(marshal, packet))', ending=''))
        method.append(gen.Block([
            gen.Statement('return false')
        ]))

        method.append(gen.Statement('// The user is assumed to provide all peek methods in C#', ending=''))
        method.append(gen.Statement('// TODO: Test if the method exists in the class', ending=''))
        method.append(gen.Statement(f'{to_camel_case(program_name, capitalize=False)}SinceLastCalled = Math.Max({to_camel_case(program_name, capitalize=False)}SinceLastCalled, Kaminari.Overflow.inc({to_camel_case(program_name, capitalize=False)}SinceLastCalled))'))
        method.append(gen.Statement(f'if ({to_camel_case(program_name, capitalize=False)}SinceLastPeeked > 100 || Kaminari.Overflow.ge(blockId, {to_camel_case(program_name, capitalize=False)}LastPeeked))', ending=''))
        method.append(gen.Block([
            gen.Statement(f'{to_camel_case(program_name, capitalize=False)}SinceLastPeeked = 0'),
            gen.Statement(f'{to_camel_case(program_name, capitalize=False)}LastPeeked = blockId'),
            gen.Statement(f'return client.peek{to_camel_case(program_name)}(data, packet.timestamp())')
        ]))

        method.append(gen.Statement(f'return true'))

        self.handler_programs.add(program_name)
        self.marshal_cls.methods.append(method)

        self.marshal_cls.attributes.append(gen.Attribute(f'SortedList<ushort, DataBuffer<{to_camel_case(message_name)}>>', f'{to_camel_case(program_name, capitalize=False)}'))
        self.marshal_cls.attributes.append(gen.Proppertie(f'byte', f'{to_camel_case(program_name, capitalize=False)}BufferSize', True, True))
        self.marshal_cls.attributes.append(gen.Attribute(f'ushort', f'{to_camel_case(program_name, capitalize=False)}LastPeeked'))
        self.marshal_cls.attributes.append(gen.Attribute(f'ushort', f'{to_camel_case(program_name, capitalize=False)}SinceLastPeeked'))
        self.marshal_cls.attributes.append(gen.Attribute(f'ushort', f'{to_camel_case(program_name, capitalize=False)}LastCalled'))
        self.marshal_cls.attributes.append(gen.Attribute(f'byte', f'{to_camel_case(program_name, capitalize=False)}SinceLastCalled'))

        return [method]

    def _generate_internals(self):
        # Marshal size method
        method = gen.Method('int', f'size<T>', [], visibility=gen.Visibility.PUBLIC)
        self.marshal_cls.methods.append(method)

        # TODO(gpascualg): Use one method per type
        for message_name, message in self.trivial_messages.items():
            method.append(gen.Statement(f'if (typeof(T) == typeof({to_camel_case(message_name)}))', ending=''))
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
            method.append(gen.Statement(f'if (typeof(T) == typeof({ctype}))', ending=''))
            method.append(gen.Block([
                gen.Statement(f'return sizeof({ctype})')
            ]))

        method.append(gen.Statement('return 0'))

        # General packet handler
        method = gen.Method('bool', 'handlePacket<T>', [
            gen.Variable('Kaminari.PacketReader', 'packet'),
            gen.Variable('T', 'client'),
            gen.Variable('ushort', 'blockId')
        ], visibility=gen.Visibility.PUBLIC, postfix=' where T : Kaminari.IBaseClient')

        method.append(gen.Statement('switch (packet.getOpcode())', ending=''))
        method.append(gen.Block([
            gen.Scope([
                gen.Statement(f'case (ushort)Opcodes.opcode{to_camel_case(program)}:', ending=''),
                gen.Scope([
                    gen.Statement(f'return handle{to_camel_case(program)}(this, packet, (IClient)client, blockId)') 
                ], indent=True)
            ]) for program in self.handler_programs
        ] + [gen.Scope([
            gen.Statement(f'default:', ending=''),
            gen.Scope([
                gen.Statement(f'return false') 
            ], indent=True)
        ])]))

        self.marshal_cls.methods.append(method)

        # Generated constructor and update methods
        marshal_constructor = gen.Method('', 'Marshal', visibility=gen.Visibility.PUBLIC)
        marshal_update = gen.Method('void', 'Update<T>', [
            gen.Variable('T', 'client'),
            gen.Variable('ushort', 'blockId')
        ], visibility=gen.Visibility.PUBLIC, postfix=' where T : Kaminari.IBaseClient')

        self.marshal_cls.methods.append(marshal_constructor)
        self.marshal_cls.methods.append(marshal_update)

        buffer_size = self.config.get("buffer_size", 2)
        for program_name in self.recv_list:
            # Constructor initializer
            message_name = to_camel_case(self.get_program_message(self.programs[program_name]))
            x = to_camel_case(program_name, capitalize=False)
            marshal_constructor.append(gen.Statement(f'{x} = new SortedList<ushort, DataBuffer<{message_name}>>(new Kaminari.DuplicateKeyComparer())'))
            marshal_constructor.append(gen.Statement(f'{x}BufferSize = {buffer_size}'))
            marshal_constructor.append(gen.Statement(f'{x}LastPeeked = 0'))
            marshal_constructor.append(gen.Statement(f'{x}SinceLastPeeked = 0'))
            marshal_constructor.append(gen.Statement(f'{x}LastCalled = 0'))
            marshal_constructor.append(gen.Statement(f'{x}SinceLastCalled = 0'))

            # Update method
            marshal_update.append(gen.Statement(f'{x}SinceLastCalled = Math.Max({x}SinceLastCalled, Kaminari.Overflow.inc({x}SinceLastCalled))'))
            marshal_update.append(gen.Statement(f'while (checkBuffer({x}, blockId, {x}BufferSize))', ending=''))
            marshal_update.append(gen.Block([
                gen.Statement(f'var data = {x}.Values[0]'),
                gen.Statement(f'if (!((IClient)client).on{to_camel_case(program_name)}(data.Data, data.Timestamp))', ending=''),
                gen.Block([
                    gen.Statement('break')
                ]),
                gen.Statement(f'{x}LastCalled = data.BlockId'),
                gen.Statement(f'{x}SinceLastCalled = 0'),
                gen.Statement(f'{x}.RemoveAt(0)')
            ]))
        
        # IClient
        for program_name in self.handler_programs:
            program = self.programs[program_name]
            message = self.get_program_message(program)
            
            # Templated queues work by filling vectors
            queue = self.queues[program.queue.eval()]
            if queue.specifier.queue_type == boxes.QueueSpecifierType.TEMPLATED:
                args = queue.specifier.args
                message = args[1].eval()
                
            self.client_itf.methods.append(gen.Method(
                'bool', 
                f'on{to_camel_case(program_name)}',
                [
                    gen.Variable(to_camel_case(message), 'data'), 
                    gen.Variable('ulong', 'timestamp')
                ],
                visibility=gen.Visibility.PUBLIC,
                interface=True,
                hide_visibility=True
            ))
                
            self.client_itf.methods.append(gen.Method(
                'bool', 
                f'peek{to_camel_case(program_name)}',
                [
                    gen.Variable(to_camel_case(message), 'data'), 
                    gen.Variable('ulong', 'timestamp')
                ],
                visibility=gen.Visibility.PUBLIC,
                interface=True,
                hide_visibility=True
            ))

        # Opcodes enum
        opcodes = gen.Block([])
        for program in self.programs.values():
            program_name = program.name.eval()
            name = f'opcode{to_camel_case(program_name)}'

            opcodes.append(
                gen.Statement(f'{name: <24} = 0x{self.opcodes[program_name]},', ending='')
            )
            
        
        self.opcodes_file.add(gen.Scope([
            gen.Statement('public enum Opcodes', ending=''),
            opcodes
        ]))

        # Protocol queues
        queues = gen.Class('ProtocolQueues : Kaminari.IProtocolQueues', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        self.queues_file.add(queues)
        
        constructor = gen.Method('', 'ProtocolQueues', [
            gen.Variable('int', 'resendThreshold')
        ], visibility=gen.Visibility.PUBLIC)
        queues.methods.append(constructor)

        reset = gen.Method('void', 'reset', visibility=gen.Visibility.PUBLIC)
        reset.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.clear()') for queue in self.queues.keys() if self.queue_usage[queue]
        ]))
        queues.methods.append(reset)

        ack = gen.Method('void', 'ack', [gen.Variable('ushort', 'blockId')], visibility=gen.Visibility.PUBLIC)
        ack.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.ack(blockId)') for queue in self.queues.keys() if self.queue_usage[queue]
        ]))
        queues.methods.append(ack)

        process = gen.Method('void', 'process', [
            gen.Variable('ushort', 'blockId'),
            gen.Variable('ref ushort', 'remaining'),
            gen.Variable('SortedDictionary<uint, List<Kaminari.Packet>>', 'byBlock')
        ], visibility=gen.Visibility.PUBLIC)
        process.append(gen.Scope([
            gen.Statement(f'{to_camel_case(queue, False)}.process(Marshal.instance, blockId, ref remaining, byBlock)') for queue in self.queues.keys() if self.queue_usage[queue]
        ]))
        queues.methods.append(process)

        for queue_name, queue in self.queues.items():
            if not self.queue_usage[queue_name]:
                continue

            # Attribute
            queue_base = queue.base.subtype.eval()
            queue_packer = 'Kaminari.ImmediatePacker'
            queue_packer_template = 'Kaminari.ImmediatePacker, Kaminari.Packet'
            queue_packer_args = ''

            if queue.specifier.queue_type == boxes.QueueSpecifierType.SPECIALIZED:
                queue_packer_base = queue.specifier.args.eval()
                queue_packer = f'Kaminari.{to_camel_case(queue_packer_base)}'

                if queue_packer_base == 'most_recent_packer_by_opcode':
                    queue_base = queue_base + '_by_opcode'
                    queue_packer_template = queue_packer
                elif queue_packer_base == 'most_recent_packer_with_id':
                    queue_base = queue_base + '_with_id'
                    queue_packer_template = queue_packer
                else:
                    queue_packer_template = f'{queue_packer}, Kaminari.Packet'

            elif queue.specifier.queue_type == boxes.QueueSpecifierType.TEMPLATED:
                num_programs = len(self.queue_usage[queue_name])
                if num_programs > 1:
                    raise RuntimeError('Eventually synced queues can be used only in one program')
                
                args = queue.specifier.args
                queue_packer = to_camel_case(args[0].eval())
                global_dtype = to_camel_case(args[1].eval())
                data_dtype = to_camel_case(args[2].eval())
                program_name = self.queue_usage[queue_name][0]

                queue_packer_template = f'Kaminari.{queue_packer}<{global_dtype}, {data_dtype}>, {data_dtype}'
                queue_packer_args = f'{global_dtype}.class, Opcodes.opcode{to_camel_case(program_name)}'

            if queue.base.argument is not None:
                queue_packer_args = queue.base.argument.eval()

            queue_qualified_name = f'Kaminari.{to_camel_case(queue_base)}<{queue_packer_template}>'

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
                    gen.Variable('ushort', 'opcode'),
                    gen.Variable(f'Kaminari.IData', 'data'),
                    gen.Variable('Action', 'callback')
                ], visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(Marshal.instance, opcode, data, callback)'))
                queues.methods.append(send)
            
            send = gen.Method('void', f'send{to_camel_case(queue_name)}', [
                gen.Variable('ushort', 'opcode'),
                gen.Variable(f'Kaminari.IData', 'data')
            ], visibility=gen.Visibility.PUBLIC)
            send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(Marshal.instance, opcode, data, null)'))
            queues.methods.append(send)

            if self.has_queue_packed_add(queue):
                send = gen.Method('void', f'send{to_camel_case(queue_name)}', [
                    gen.Variable('Kaminari.Packet', 'packet')
                ], visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'{to_camel_case(queue_name, False)}.add(packet)'))
                queues.methods.append(send)
    
    def _generate_version(self, version):
        config = gen.Class('Config', csharp_style=True, decl_modifiers=[gen.Visibility.PUBLIC.value])
        config.attributes.append(gen.Attribute('uint', 'VERSION', f'0x{version}', decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC))
        self.config_file.add(config)

    def dump(self, path):
        package = self.config['package'] + '.kumo'
        kaminari = self.config['kaminari']

        try:
            shutil.rmtree(path)
        except:
            pass

        os.mkdir(path)
        os.mkdir(os.path.join(path, 'structs'))

        with open(f'{path}/IClient.cs', 'w') as fp:
            fp.write(self.client_file.source())

        with open(f'{path}/Marshal.cs', 'w') as fp:
            fp.write(self.marshal_file.source([
                gen.Statement('using System'),
                gen.Statement('using System.Collections'),
                gen.Statement('using System.Collections.Generic')
            ]))

        with open(f'{path}/Unsafe.cs', 'w') as fp:
            fp.write(self.unsafe_rpc_file.source([
                gen.Statement('using System')
            ]))

        with open(f'{path}/Rpc.cs', 'w') as fp:
            fp.write(self.rpc_file.source([
                gen.Statement('using System')
            ]))

        for struct_name, struct in self.all_structs.items():
            with open(f'{path}/structs/{struct_name}.cs', 'w') as fp:
                structs_file = File(namespace='Kumo')
                structs_file.add(struct)

                fp.write(structs_file.source([
                    gen.Statement('using System.Collections'),
                    gen.Statement('using System.Collections.Generic')
                ]))

        with open(f'{path}/Opcodes.cs', 'w') as fp:
            fp.write(self.opcodes_file.source())

        with open(f'{path}/ProtocolQueues.cs', 'w') as fp:
            fp.write(self.queues_file.source([
                gen.Statement('using System'),
                gen.Statement('using System.Collections'),
                gen.Statement('using System.Collections.Generic')
            ]))

        with open(f'{path}/Config.cs', 'w') as fp:
            fp.write(self.config_file.source())
        