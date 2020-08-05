from .. import generator
from .. import gen
from .. import boxes


class LangGenerator(generator.Generator):
    def __init__(self, role, queues, messages, programs):
        super().__init__(role, queues, messages, programs)

    def __is_trivial(self, message: boxes.MessageBox):
        for decl in message.fields.eval():
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
            return gen.Statement(f'pack_{dtype}(packet, {variable})')
        else:
            return gen.Statement(f'*packet << {variable}')

    def __write_type(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            return gen.Scope([
                gen.Statement(f'*packet << static_cast<uint8_t>(({variable}).size())'),
                gen.Statement(f'for (const auto& val : {variable})', ending=''),
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
                    gen.Statement(f'uint8_t size = packet->read<uint8_t>()'),
                    gen.Statement(f'if (packet->bytes_read() + size * sizeof_{inner}() > packet->buffer_size())', ending=''),
                    gen.Block([
                        gen.Statement('return false;')
                    ]),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'({variable}).push_back(packet->read<{inner}>())')
                    ])
                ])
            else:
                return gen.Scope([
                    gen.Statement(f'uint8_t size = packet->read<uint8_t>()'),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{inner} data'),
                        gen.Statement(f'if (unpack_{inner}(packet, data)', ending=''),
                        gen.Block([
                            gen.Statement(f'({variable}).push_back(std::move(data))')
                        ])
                    ])
                ])

        if self.is_message(dtype):
            return gen.Statement(f'unpack_{dtype}(packet, data)')

        return gen.Statement(f'{variable} = packet->read<{dtype}>()')

    def __write_size(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            # There are two cases
            #  1) Inner type is trivial thus we can do `size() * sizeof(inner)`
            #  2) Inner type is not trivial and we must iterate
            inner = decl.dtype.spec.eval()

            # Case 1
            if not self.is_message(inner) or self.__is_trivial(self.messages[inner]):
                return gen.Statement(f'size += sizeof(uint8_t) + ({variable}).size() * sizeof_{inner}()')
            # Case 2
            else:
                return gen.Scope([
                    gen.Statement('size += sizeof(uint8_t)'),
                    gen.Statement(f'for (const auto& val : {variable})', ending=''),
                    gen.Block([
                        gen.Statement(f'size += packet_size(val)')
                    ])
                ])
            
        elif self.is_message(dtype):
            return gen.Statement(f'size += packet_size({variable})')
        else:
            return gen.Statement(f'size += sizeof({dtype})')

    def _generate_message_packer(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        method = gen.Method('void', f'pack_{message_name}', [
            gen.Variable('const Packet::Ptr&', 'packet'),
            gen.Variable(f'const {message_name}&', 'data')
        ], visibility=gen.Visibility.PUBLIC)

        for decl in message.fields.eval():
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'*packet << static_cast<bool>(data.{name})'))
                method.append(gen.Statement(f'if (static_cast<bool>(data.{name}))', ending=''))
                method.append(gen.Block([
                    self.__write_type(decl, f'*data.{name}')
                ]))
            else:
                method.append(self.__write_type(decl, f'data.{name}'))

        print(method.both(0))
        return method

    def _generate_message_unpacker(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        method = gen.Method('bool', f'unpack_{message_name}', [
            gen.Variable('PacketReader*', 'packet'),
            gen.Variable(f'{message_name}&', 'data')
        ], visibility=gen.Visibility.PUBLIC)

        for decl in message.fields.eval():
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'if (packet->bytes_read() + sizeof(bool) > packet->buffer_size())', ending=''))
                method.append(gen.Block([
                    gen.Statement('return false')
                ]))
                
                method.append(gen.Statement(f'if (packet->read<uint8_t>() == 1)', ending=''))
                method.append(gen.Block([
                    self.__read_type(decl, f'*data.{name}')
                ]))
            else:
                method.append(self.__read_type(decl, f'data.{name}'))

        print(method.both(0))
        return method

    def _generate_message_size(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        methods = []
        method = gen.Method('uint8_t', f'packet_size', [
            gen.Variable(f'const {message_name}&', 'data')
        ], visibility=gen.Visibility.PUBLIC)
        methods.append(method)

        if self.__is_trivial(message):
            method.append(gen.Statement('(void)data'))
            method.append(gen.Statement(f'return sizeof({message_name})'))

            # Method without parameter
            method = gen.Method('uint8_t', f'sizeof_{message_name}', visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'return sizeof({message_name})'))
            methods.append(method)
        else:
            method.append(gen.Statement('uint8_t size = 0'))    
            # Manually loop all types
            for decl in message.fields.eval():
                name = decl.name.eval()

                if decl.optional:
                    method.append(gen.Statement('size += sizeof(bool)'))
                    method.append(gen.Statement(f'if (static_cast<bool>(data.{name}))'))
                    method.append(gen.Block([
                        self.__write_size(decl, f'*data.{name}')
                    ]))
                else:
                    method.append(self.__write_size(decl, f'data.{name}'))

        print(method.both(0))
        return methods

    def _generate_program_send(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        queue = program.queue.eval()
        args = program.args.eval()
        message_name = args[0]

        # Returned methods
        methods = []
        
        # Individual send without callback
        method = gen.Method('void', f'send_{program_name}', [
            gen.Variable('Client*', 'client'),
            gen.Variable(f'{message_name}&&', 'data')
        ], visibility=gen.Visibility.PUBLIC)
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name})'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'client->send_{queue}(packet)'))
        print(method.both(0))

        # Individual with callback
        method = gen.Method('void', f'send_{program_name}', [
            gen.Variable('Client*', 'client'),
            gen.Variable(f'{message_name}&&', 'data'),
            gen.Variable('T&&', 'callback')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename T>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name}, std::forward<T>(callback))'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'client->send_{queue}(packet)'))
        print(method.both(0))

        # Individual send without callback
        method = gen.Method('void', f'broadcast_{program_name}', [
            gen.Variable('Cell*', 'cell'),
            gen.Variable(f'{message_name}&&', 'data')
        ], visibility=gen.Visibility.PUBLIC)
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name})'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'cell->broadcast([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'client->send_{queue}(packet)')], True))
        method.append(gen.Statement(f'}})'))
        print(method.both(0))

        # Individual with callback
        method = gen.Method('void', f'broadcast_{program_name}', [
            gen.Variable('Cell*', 'cell'),
            gen.Variable(f'{message_name}&&', 'data'),
            gen.Variable('T&&', 'callback')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename T>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name}, std::forward<T>(callback))'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'cell->broadcast([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'client->send_{queue}(packet)')], True))
        method.append(gen.Statement(f'}})'))
        print(method.both(0))

        return methods
