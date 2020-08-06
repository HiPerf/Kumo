from .. import generator
from .. import gen
from .. import boxes


def if_template(x):
    try:
        return x.template is not None
    except:
        return None


class File(object):
    def __init__(self, namespace=None):
        self.sources = []
        self.namespace = namespace

    def add(self, code):
        self.sources.append(code)
            
    def __str__(self):
        if self.namespace is not None:
            code_root = gen.Scope([
                gen.Statement(f'namespace {self.namespace}', ending=''),
                gen.Block(self.sources)
            ])
        else:
            code_root = gen.Scope(self.sources)
        
        header_decl = code_root.decl(0)
        header_inst = code_root.instance(0, eval_fn=lambda x: if_template(x) in (None, True))
        source = code_root.instance(0, eval_fn=lambda x: if_template(x) in (None, False))

        return header_decl + header_inst + '\n---------------------\n' + source + '\n---------------------\n' 


class LangGenerator(generator.Generator):
    def __init__(self, role, queues, messages, programs):
        super().__init__(role, queues, messages, programs)
        
        # Some helpers
        self.handler_programs = set()

        # Output code
        self.marshall_file = File(namespace='kaminari')
        self.opcodes_file = File(namespace='kaminari')
        self.rpc_file = File(namespace='kaminari')
        self.rpc_detail_file = File(namespace='kaminari')

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

        self.marshall_file.add(method)
        return [method]

    def _generate_message_unpacker(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        method = gen.Method('bool', f'unpack_{message_name}', [
            gen.Variable('packet_reader*', 'packet'),
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

        self.marshall_file.add(method)
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

        for method in methods:
            self.marshall_file.add(method)

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
        method.append(gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)'))

        # Individual with callback
        method = gen.Method('void', f'send_{program_name}', [
            gen.Variable('Client*', 'client'),
            gen.Variable(f'{message_name}&&', 'data'),
            gen.Variable('T&&', 'callback')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename T>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name}, std::forward<T>(callback))'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)'))

        # Global broadcast send without callback
        method = gen.Method('void', f'broadcast_{program_name}', [
            gen.Variable('broadcaster<B>*', 'broadcaster'),
            gen.Variable(f'{message_name}&&', 'data')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name})'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'broadcaster->broadcast([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)')], True))
        method.append(gen.Statement(f'}})'))

        # Global broadcast with callback
        method = gen.Method('void', f'broadcast_{program_name}', [
            gen.Variable('broadcaster<B>*', 'broadcaster'),
            gen.Variable(f'{message_name}&&', 'data'),
            gen.Variable('T&&', 'callback')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B, typename T>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name}, std::forward<T>(callback))'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'broadcaster->broadcast([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)')], True))
        method.append(gen.Statement(f'}})'))

        # Global broadcast send without callback
        method = gen.Method('void', f'broadcast_single_{program_name}', [
            gen.Variable('broadcaster<B>*', 'broadcaster'),
            gen.Variable(f'{message_name}&&', 'data')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name})'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'broadcaster->broadcast_single([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)')], True))
        method.append(gen.Statement(f'}})'))

        # Global broadcast with callback
        method = gen.Method('void', f'broadcast_single_{program_name}', [
            gen.Variable('broadcaster<B>*', 'broadcaster'),
            gen.Variable(f'{message_name}&&', 'data'),
            gen.Variable('T&&', 'callback')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B, typename T>', ending=''))
        methods.append(method)

        method.append(gen.Statement(f'Packet::Ptr packet = Packet::make(opcode::{program_name}, std::forward<T>(callback))'))
        method.append(gen.Statement(f'pack_{message_name}(packet, data)'))
        method.append(gen.Statement(f'broadcaster->broadcast_single([packet](auto client) {{', ending=''))
        method.append(gen.Scope([gen.Statement(f'::kaminari::detail::send_{queue}(client, packet)')], True))
        method.append(gen.Statement(f'}})'))
        
        for method in methods:
            self.rpc_file.add(method)

        return methods

    def _generate_program_recv(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        args = program.args.eval()
        message_name = args[0]

        method = gen.Method('bool', f'handle_{program_name}', [
            gen.Variable('packet_reader*', 'packet'),
            gen.Variable('client*', 'client')
        ])

        if program.cond.attr is not None:
            attr = program.cond.attr.eval()
            value = program.cond.value.eval()
            false_case = program.cond.false_case
            if false_case.action is not None:
                false_case = false_case.action.eval()
            else:
                false_case = 'handle_client_status_error'

            method.append(gen.Statement(f'if (client->{attr}() != {attr}::{value})', ending=''))
            method.append(gen.Block([
                gen.Statement(f'return {false_case}(packet->opcode(), client->{attr}(), {attr}::{value})')
            ]))
        
        method.append(gen.Statement(f'const {message_name} data'))
        method.append(gen.Statement(f'if (!unpack_{message_name}(packet, data)', ending=''))
        method.append(gen.Block([
            gen.Statement('return false')
        ]))

        method.append(gen.Statement(f'client->on_{program_name}(packet)'))

        self.handler_programs.add(program)

        return [method]

    def _generate_internals(self):
        # Per queue internal send to hide implementation details
        details_methods = []

        for queue in self.queues.keys():
            method = gen.Method('void', f'send_{queue}', [
                gen.Variable('client*', 'client'),
                gen.Variable('const packet::ptr&', 'packet')
            ], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'client->send_{queue}(packet)'))
            details_methods.append(method)

        self.rpc_detail_file.add(gen.Scope([
            gen.Statement('namespace detail', ending=''),
            gen.Block(details_methods)
        ]))

        # General packet handler
        method = gen.Method('bool', 'handle_packet', [
            gen.Variable('packet_reader*', 'packet'),
            gen.Variable('client*', 'client')
        ])

        method.append(gen.Statement('switch (packet->opcode())', ending=''))
        method.append(gen.Block([
            gen.Scope([
                gen.Statement(f'case opcode::{program.name.eval()}:', ending=''),
                gen.Scope([
                    gen.Statement(f'return handle_{program.name.eval()}(packet, client)') 
                ], indent=True)
            ]) for program in self.handler_programs
        ]))

        self.marshall_file.add(method)


        print(self.rpc_file)
        