import hashlib
import cgen as c

from . import boxes


def memo(argnum):
    def memoize(f):
        memo = {}
        def helper(*args, **kwargs):
            x = args[argnum]
            if x not in memo:     
                memo[x] = f(*args, **kwargs)
            return memo[x]
        return helper
    return memoize


class Generator(object):
    def __init__(self, user_defined_messages):
        self.user_defined_messages = user_defined_messages
        self.queues_table = {}
        self.jump_table = {}
        self.map_program = {}
        self.packet_makers = set()

        self.TRIVIAL_TYPES = {
            'int8': None,
            'int16': None,
            'int32': None,
            'int64': None,
            'uint8': None,
            'uint16': None,
            'uint32': None,
            'uint64': None,
            'float': None,
            'double': None,
            'bool': None
        }

        self.VALID_TYPES = {
            'string': None,
            'vector': None
        }

        self.USED_OPCODES = {}

    def _packet_type(self):
        raise NotImplementedError()

    def _data_cref(self, dtype, name):
        raise NotImplementedError()

    def _pointer_type(self, dtype, name):
        raise NotImplementedError()

    def _data_object_ref(self, dtype, name):
        raise NotImplementedError()

    def _data_value_ref(self, dtype, name):
        raise NotImplementedError()

    def _template_call(self, name, args):
        raise NotImplementedError()

    def _template_function_declaration(self, template, body):
        raise NotImplementedError()

    def _template_function_name(self, template, name):
        raise NotImplementedError()

    def _template_function_arg(self, dtype, name, default=''):
        raise NotImplementedError()

    def _template_forward(self, template, name):
        raise NotImplementedError()

    def _call_queue(self, name, args):
        raise NotImplementedError()

    def _pointer_call(self, obj, call):
        raise NotImplementedError()

    def _ns_call(self, ns, call):
        raise NotImplementedError()

    def _enum_class(self):
        raise NotImplementedError()

    def _queue_decl(self, queue, param):
        raise NotImplementedError()

    def _additional_queue_methods(self, queues):
        return []

    def _packets_by_block(self):
        raise NotImplementedError()

    def _by_ref(self, value):
        raise NotImplementedError()

    def _initializer(self, struct):
        raise NotImplementedError()

    def _constexpr(self, dtype):
        raise NotImplementedError()

    def _str_len(self, string):
        raise NotImplementedError()

    def _public_inheritance(self, base):
        raise NotImplementedError()
    
    def _global_structs(self, Struct):
        raise NotImplementedError()

    def _get_queue(self, queue, opcode):
        queue_name = queue.identifier.eval().lower()
        queue_template = None
        if queue.global_type:
            opcode = self._ns_call('Opcode', f'OP_{opcode}')
            queue_template = (queue.global_type.eval(), queue.detail_type.eval(), opcode)
        
        if queue_template:
            try:
                self.queues_table[queue_name].add(queue_template)
            except:
                self.queues_table[queue_name] = set([queue_template])
        else:
            self.queues_table[queue_name] = None

        if queue_template is not None:
            return self._template_call(f'send_{queue_name}', queue_template)
            
        return f'send_{queue_name}'

    def _struct(self, WrapStruct, box):
        return (
            c.Statement(f'struct {box.name.eval()}'),
            WrapStruct(box).eval(self)
        )

    def _packer(self, Method, WrapPack, message_name, box):
        args = [
            self._data_object_ref(self._packet_type(), 'packet'),
            self._data_cref(message_name, 'data')
        ]

        declaration = c.FunctionDeclaration(
            c.Value(f'void', f'pack_{message_name}'),
            args
        )

        body = c.Block([
            *[
                WrapPack(decl).eval(self) for decl in box.fields.eval()
            ]
        ])

        return (
            declaration, 
            c.FunctionBody(declaration, body), 
            Method('void', f'pack_{message_name}', args, body)
        )

    def _generic_packer(self, Method, WrapPack, message_name, box):
        args = [
            self._data_object_ref(self._packet_type(), 'packet'),
            self._data_cref(message_name, 'data')
        ]

        declaration = c.FunctionDeclaration(
            c.Value(f'void', f'pack_message'),
            args
        )

        body = c.Block([
            *[
                WrapPack(decl).eval(self) for decl in box.fields.eval()
            ]
        ])

        return (
            declaration, 
            c.FunctionBody(declaration, body), 
            Method('void', f'pack_message', args, body)
        )

    def _unpacker(self, Method, WrapUnpack, message_name, box):
        args = [
            self._pointer_type('PacketReader', 'packet'),
            self._data_object_ref(message_name, 'data')
        ]

        declaration = c.FunctionDeclaration(
            c.Value(f'bool', f'unpack_{message_name}'),
            args
        )

        body = c.Block([
            *[
                WrapUnpack(decl).eval(self) for decl in box.fields.eval()
            ],
            c.Statement('return true')
        ])
        
        return (
            declaration, 
            c.FunctionBody(declaration, body),
            Method('bool', f'unpack_{message_name}', args, body)
        )

    @memo(1)
    def _is_trivial(self, message_name, box, include_messages=True):
        dtypes = ((decl.optional, decl.dtype.dtype.eval()) for decl in box.block.fields.eval())
        for optional, dtype in dtypes:
            if optional or dtype in ('string', 'vector'):
                return False
            
            if self.is_message(dtype):
                if not include_messages or not self._is_trivial(dtype, self.user_defined_messages[dtype]):
                    return False

        return True        

    def _templated_make_packet(self, Method, program_name, message_name):
        args = [
            self._data_cref(message_name, 'data'),
            self._template_function_arg('T', 'arg')
        ]
        
        declaration = c.FunctionDeclaration(
            c.Value(self._packet_type(), self._template_function_name('T', f'make_{program_name}')),
            args
        )

        template_declaration = self._template_function_declaration(
            'typename... T',
            declaration
        )

        packet_make = self._ns_call('Packet', 'make')
        opcode_call = self._ns_call('Opcode', 'OP_')
        opcode = self.get_opcode(program_name)
        detail_call = self._ns_call('marshal', 'pack_')

        body = c.Block([
            c.Statement(f'{self._packet_type()} packet = {packet_make}({opcode_call}{opcode}, {self._template_forward("T", "arg")})'),
            c.Statement(f'{detail_call}{message_name}(packet, data)'),
            c.Statement(f'return packet')
        ])

        self.packet_makers.add(message_name)

        return (
            template_declaration, 
            c.FunctionBody(template_declaration, body), 
            Method(self._packet_type(), f'make_{program_name}', args, body, ('typename... T', 'T'))
        )

    def _make_packet(self, Method, program_name, message_name, argument_type, argument_default):
        args = [
            self._data_cref(message_name, 'data'),
            c.Value(argument_type, f'arg{argument_default}')
        ]
        
        declaration = c.FunctionDeclaration(
            c.Value(self._packet_type(), f'make_{program_name}'),
            args
        )

        packet_make = self._ns_call('Packet', 'make')
        opcode_call = self._ns_call('Opcode', 'OP_')
        opcode = self.get_opcode(program_name)
        detail_call = self._ns_call('marshal', 'pack_')

        body = c.Block([
            c.Statement(f'{self._packet_type()} packet = {packet_make}({opcode_call}{opcode}, arg)'),
            c.Statement(f'{detail_call}{message_name}(packet, data)'),
            c.Statement(f'return packet')
        ])

        self.packet_makers.add(message_name)

        return (
            declaration, 
            c.FunctionBody(declaration, body), 
            Method(self._packet_type(), f'make_{program_name}', args, body)
        )

    def _server_s2c_from_packet(self, Method, program_name, arguments, queue):
        args = [
            self._pointer_type('Client', 'client'),
            self._data_cref(self._packet_type(), 'packet')
        ]
        
        # BY PACKET DIRECTLY
        declaration = c.FunctionDeclaration(
            c.Value('void', f'send_{program_name}'),
            args
        )

        body = c.Block([
            c.Statement(self._call_queue(queue, ['packet']))
        ])

        return (
            declaration, 
            c.FunctionBody(declaration, body), 
            Method('void', f'send_{program_name}', args, body)
        )

    def _server_s2c(self, Method, program_name, arguments, queue, argument_type=None, argument_default=None):
        args = [
            self._pointer_type('Client', 'client'),
            self._data_cref(arguments[0], 'data')
        ]

        if argument_type:
            args.append(c.Value(argument_type, f'arg{argument_default}'))

        # All in one
        declaration = c.FunctionDeclaration(
            c.Value('void', program_name),
            args
        )

        opcode = self._ns_call('Opcode', f'OP_{self.get_opcode(program_name)}')
        call_params = [opcode, 'data']
        if argument_type:
            call_params.append('arg')

        body = c.Block([
            c.Statement(self._call_queue(queue, call_params))
        ])

        return (
            declaration,
            c.FunctionBody(declaration, body), 
            Method('void', program_name, args, body)
        )

    def _templated_server_s2c(self, Method, program_name, arguments, queue):
        args = [
            self._pointer_type('Client', 'client'),
            self._data_cref(arguments[0], 'data'),
            self._template_function_arg('T', 'arg')
        ]

        # All in one
        declaration = c.FunctionDeclaration(
            c.Value('void', self._template_function_name('T', program_name)),
            args
        )

        template_declaration = self._template_function_declaration(
            'typename... T',
            declaration
        )
        
        body = c.Block([
            c.Statement(f'Packet::Ptr packet = detail::make_{program_name}(data, std::forward<T>(arg)...)'),
            c.Statement(f'detail::send_{program_name}(client, packet)')
        ])

        return (
            template_declaration,
            c.FunctionBody(template_declaration, body), 
            Method('void', program_name, args, body, ('typename... T', 'T'))
        )

    def _broadcast_server_s2c_from_packet(self, Method, program_name, arguments, postfix, queue):
        args = [
            self._pointer_type('Cell', 'cell'),
            self._data_cref(self._packet_type(), 'packet'),
            self._pointer_type('Client', 'client')
        ]

        # BY PACKET DIRECTLY
        declaration = c.FunctionDeclaration(
            c.Value('void', f'broadcast_{program_name}{postfix}'),
            args
        )

        body = c.Block([
            c.Line(f'cell->broadcast{postfix}([packet](auto client) {{'),
            c.Statement('  ' + self._call_queue(queue, ['packet'])),
            c.Statement('}, client)')
        ])
        
        return (
            declaration,
            c.FunctionBody(declaration, body), 
            Method('void', f'broadcast_{program_name}{postfix}', args, body)
        )

    def _broadcast_templated_server_s2c(self, Method, program_name, arguments, postfix, queue):
        args = [
            self._pointer_type('Cell', 'cell'),
            self._data_cref(arguments[0], 'data'),
            self._pointer_type('Client', 'client'),
            self._template_function_arg('T', 'arg')
        ]

        # All in one
        declaration = c.FunctionDeclaration(
            c.Value('void', self._template_function_name('T', f'{program_name}{postfix}')),
            args
        )

        template_declaration = self._template_function_declaration(
            'typename... T',
            declaration
        )

        body = c.Block([
            c.Statement(f'Packet::Ptr packet = detail::make_{program_name}(data, std::forward<T>(arg)...)'),
            c.Statement(f'detail::broadcast_{program_name}{postfix}(cell, packet, client)')
        ])

        return (
            template_declaration, 
            c.FunctionBody(template_declaration, body), 
            Method('void', f'{program_name}{postfix}', args, body, ('typename... T', 'T'))
        )

    
    def _broadcast_server_s2c(self, Method, program_name, arguments, postfix, queue):
        args = [
            self._pointer_type('Cell', 'cell'),
            self._data_cref(arguments[0], 'data'),
            self._pointer_type('Client', 'client')
        ]

        # All in one
        declaration = c.FunctionDeclaration(
            c.Value('void', f'{program_name}{postfix}'),
            args
        )

        opcode = self._ns_call('Opcode', f'OP_{self.get_opcode(program_name)}')
        body = c.Block([
            c.Line(f'cell->broadcast{postfix}([&data](auto client) {{'),
            c.Statement('  ' + self._call_queue(queue, [opcode, 'data'])),
            c.Statement('}, client)')
        ])

        return (
            declaration, 
            c.FunctionBody(declaration, body), 
            Method('void', f'{program_name}{postfix}', args, body, ('typename... T', 'T'))
        )

    def _server_c2s(self, Method, program_name, message_name):
        args = [
            self._pointer_type('PacketReader', 'packet'),
            self._pointer_type('Client', 'client')
        ]

        declaration = c.FunctionDeclaration(
            c.Value('void', program_name),
            args
        )

        unpack = f'unpack_{message_name}'
        fname = f'on_{program_name}'
        init = self._initializer(message_name)

        body = c.Block([
            c.Statement(f'{message_name} data{init}'),
            c.If(
                f'{unpack}(packet, data)',
                c.Block([c.Statement(f'{self._pointer_call("client", fname)}({self._pointer_call("packet", "timestamp")}(), data)')]),
                c.Block([c.Statement(f'{self._pointer_call("client", "on_read_error")}()')])
            )
        ])
        
        self.jump_table[self.get_opcode(program_name)] = program_name
        self.map_program[program_name] = message_name

        return (
            declaration,
            c.FunctionBody(declaration, body), 
            Method('void', program_name, args, body)
        )

    
    def _jump_table(self, Method, skip_status_check=False):
        args = [
            self._pointer_type('PacketReader', 'packet'),
            self._pointer_type('Client', 'client')
        ]
        
        declaration = c.FunctionDeclaration(
            c.Value('void', 'handle_packet'),
            args
        )

        def expr_state(fname, then):
            state = self.user_defined_messages[self.map_program[fname]].block.state
            if skip_status_check or state.is_any:
                return then
        
            client_call = self._pointer_call('client', 'status')
            status = self._ns_call(state.enum.eval(), state.state.eval())
            return c.If(f'{client_call}() == {status}', c.Block([then]))

        switch = self._pointer_call('packet', 'opcode')
        opcode_enum = self._ns_call('Opcode', 'OP_')
        on_error = self._pointer_call('client', 'on_read_error')
        
        body = c.Block([
            c.Line(f'switch ({switch}())'),
            c.Block([
                *[c.Collection([
                    c.Line(f'case {opcode_enum}{opcode}:'),
                    c.Block([
                        expr_state(fname, c.Statement(f'{fname}(packet, client)')),
                        c.Statement(f'break')
                    ])
                ]) for opcode, fname in self.jump_table.items()],
                c.Line(f'default:'),
                c.Block([
                    c.Statement(f'{on_error}()'),
                    c.Statement(f'break')
                ])
            ])
        ])
      
        return (
            declaration, 
            c.FunctionBody(declaration, body),
            Method('void', 'handle_packet', args, body)
        )

    def _opcode_enum(self):
        return c.Collection([
            c.Line(f'{self._enum_class()} Opcode : {self.TRIVIAL_TYPES["uint32"]}'),
            c.Block([
                c.Line(f'OP_{opcode} = 0x{opcode}, // {fname}') for fname, opcode in self.USED_OPCODES.items()
            ]),
            c.Line(';')
        ])

    def _queue_var(self, queue, param):
        raise NotImplementedError()
    
    def _call_queues_method(self, name, queue, method, params):
        queue_type = queue.specifier.queue_type
        name = f'_{name.lower()}'

        if queue_type == boxes.QueueSpecifierType.ARRAY:
            return c.Collection([
                c.Statement(f'{name}[{i}].{method}({", ".join(params)})')
                for i in range(queue.specifier.args.eval())
            ])

        return c.Statement(f'{name}.{method}({", ".join(params)})')
    
    def _queues_class(self, Cls, Method, queues):
        queue_reset = Method('void', 'reset', [], c.Block([
                self._call_queues_method(name, queue, 'clear', []) for name, queue in queues.items()
            ]))

        queue_ack = Method('void', 'ack', [c.Value(self.get_dtype('uint16'), 'block_id')], c.Block([
                self._call_queues_method(name, queue, 'ack', ['block_id']) for name, queue in queues.items()
            ]))

        queue_pending = Method('void', 'process', [
                c.Value(self.get_dtype('uint16'), 'id'),
                self._data_value_ref(self.get_dtype('uint16'), 'remaining'),
                self._data_object_ref(self._packets_by_block(), 'by_block')
            ],
            c.Block([
                self._call_queues_method(queue, param, 'process', [
                        'id', self._by_ref('remaining'), 'by_block'
                    ]) for queue, param in queues.items()
            ])
        )

        queue_decls = []
        queue_vars = []
        for name, queue in queues.items():
            queue_decls += self._queue_decl(name, queue)
            queue_vars.append(self._queue_var(name, queue))

        queue_decls += self._additional_queue_methods(queues)

        return Cls(
            'protocol_queues', 
            queue_decls, 
            [queue_reset, queue_ack, queue_pending], 
            [], [], [], 
            queue_vars
        )
    
    def is_trivial(self, dtype):
        return dtype in self.TRIVIAL_TYPES

    def is_message(self, dtype):
        return dtype in self.user_defined_messages

    def get_dtype(self, dtype):
        if dtype not in self.TRIVIAL_TYPES and dtype not in self.VALID_TYPES:
            if self.is_message(dtype):
                return dtype
            
            raise NotImplementedError(f'Invalid type `{dtype}`')

        try:
            return self.TRIVIAL_TYPES[dtype]
        except:
            return self.VALID_TYPES[dtype]

    @memo(1)
    def get_opcode(self, name):
        if name in self.USED_OPCODES:
            return self.USED_OPCODES[name]

        def get_digest(h, encoded):
            h.update(encoded)
        
            # Keep higher most byte reserved
            digest = bytearray(h.digest())
            digest[0] = digest[0] & (~(1 << 7))
            digest = bytearray.hex(digest)
            return digest
        
        encoded = name.encode('utf-8')
        h = hashlib.blake2b(digest_size=2)
        digest = get_digest(h, encoded)
        while digest in self.USED_OPCODES.values():
            digest = get_digest(h, encoded)

        self.USED_OPCODES[name] = digest
        return digest
        
    