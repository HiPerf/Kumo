from .. import generator
from .. import gen
from .. import boxes
from .. import semantic



TYPE_CONVERSION = {
    dtype : dtype if all(not c.isnumeric() for c in dtype) else dtype + '_t' for dtype in semantic.TRIVIAL_TYPES
}
TYPE_CONVERSION['vector'] = 'std::vector'
TYPE_CONVERSION['optional'] = 'std::optional'


def if_template_or_inline(x):
    try:
        return x.template is not None or 'inline' in x.decl_modifiers
    except:
        return None


class File(object):
    def __init__(self, namespace=None):
        self.sources = []
        self.namespace = namespace

    def add(self, code):
        self.sources.append(code)

    def _root(self, prepend: list):
        if self.namespace is not None:
            return gen.Scope(prepend + [
                gen.Statement(f'namespace {self.namespace}', ending=''),
                gen.Block(self.sources)
            ])
        else:
            return gen.Scope(prepend + self.sources)

    def header(self, prepend=[]):
        header_decl = self._root(prepend).decl(0)
        header_inst = self._root([]).both(0, eval_fn=lambda x: if_template_or_inline(x) in (None, True))

        return header_decl + '\n' + header_inst

    def source(self, prepend=[]):
        source = self._root(prepend).instance(0, eval_fn=lambda x: if_template_or_inline(x) in (None, False))
        return source
    
    def __str__(self):
        code_root = self._root([])
        header_decl = code_root.decl(0)
        header_inst = code_root.both(0, eval_fn=lambda x: if_template_or_inline(x) in (None, True))
        source = code_root.instance(0, eval_fn=lambda x: if_template_or_inline(x) in (None, False))

        return header_decl + header_inst + '\n---------------------\n' + source + '\n---------------------\n' 


class LangGenerator(generator.Generator):
    def __init__(self, config, role, queues, messages, programs):
        super().__init__(config, role, queues, messages, programs)
        
        # Some helpers
        self.handler_programs = set()

        # Output code
        self.marshal_file = File(namespace='kumo')
        self.opcodes_file = File(namespace='kumo')
        self.rpc_file = File(namespace='kumo')
        self.structs_file = File(namespace='kumo')
        self.queues_file = File(namespace='kumo')

        # Flush marshal class already
        base_name = self.config.get('marshal', {}).get('base')
        base_name = '' if not base_name else f':public {base_name}'
        self.marshal_cls = gen.Class('marshal', decl_name_base=base_name, cpp_style=True)
        self.marshal_file.add(self.marshal_cls)

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
            if dtype == 'vector':
                return False

            # Including other messages might include optionals/vectors
            if self.is_message(dtype) and not self.__is_trivial(self.messages[dtype]):
                return False

        return True

    def __write_value(self, dtype, variable):
        # It seems to be a message type
        if self.is_message(dtype):
            return gen.Statement(f'pack(packet, {variable})')
        else:
            return gen.Statement(f'*packet << {variable}')

    def __write_type(self, decl, variable):
        dtype = decl.dtype.dtype.eval()
        if dtype == 'vector':
            inner = decl.dtype.spec.eval()
            ctype = inner
            if not self.is_message(inner):
                ctype = TYPE_CONVERSION[inner]

            return gen.Scope([
                gen.Statement(f'*packet << static_cast<uint8_t>(({variable}).size())'),
                gen.Statement(f'for (const {ctype}& val : {variable})', ending=''),
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
                        gen.Statement('return false')
                    ]),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'({variable}).push_back(packet->read<{TYPE_CONVERSION[inner]}>())')
                    ])
                ])
            else:
                return gen.Scope([
                    gen.Statement(f'uint8_t size = packet->read<uint8_t>()'),
                    gen.Statement(f'for (int i = 0; i < size; ++i)', ending=''),
                    gen.Block([
                        gen.Statement(f'{inner} data'),
                        gen.Statement(f'if (unpack(packet, data)', ending=''),
                        gen.Block([
                            gen.Statement(f'({variable}).push_back(std::move(data))')
                        ]),
                        gen.Statement(f'else'),
                        gen.Block([
                            gen.Statement('return false')
                        ])
                    ])
                ])

        if self.is_message(dtype):
            return gen.Scope([
                gen.Statement(f'if (!unpack(packet, {variable}))', ending=''),
                gen.Block([
                    gen.Statement('return false')
                ])
            ])

        return gen.Scope([
            gen.Statement(f'if (packet->bytes_read() + sizeof_{dtype}() > packet->buffer_size())', ending=''),
            gen.Block([
                gen.Statement('return false')
            ]),
            gen.Statement(f'{variable} = packet->read<{TYPE_CONVERSION[dtype]}>()')
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

            # Case 1
            if not self.is_message(inner) or self.__is_trivial(self.messages[inner]):
                return gen.Statement(f'size += sizeof(uint8_t) + ({variable}).size() * sizeof_{inner}()')
            # Case 2
            else:
                return gen.Scope([
                    gen.Statement('size += sizeof(uint8_t)'),
                    gen.Statement(f'for (const {ctype}& val : {variable})', ending=''),
                    gen.Block([
                        gen.Statement(f'size += packet_size(val)')
                    ])
                ])
            
        elif self.is_message(dtype):
            return gen.Statement(f'size += packet_size({variable})')
        else:
            return gen.Statement(f'size += sizeof_{dtype}()')

    def _generate_structure(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        base = ''
        # TODO(gpascualg): Check we don't really need this
        #if message.base.name is not None:
        #    base = f': public {message.base.name.eval()}'

        struct = gen.Class(message_name, decl_name_base=base, cpp_style=True, keyword='struct')
        for decl in self.message_fields_including_base(message):
            dtype = decl.dtype.dtype.eval()
            ctype = '{}'
            if decl.optional:
                ctype = 'std::optional<{}>'

            temp = dtype
            if dtype == 'vector':
                ctype = ctype.format('std::vector<{}>')
                temp = decl.dtype.spec.eval()
            
            if not self.is_message(temp):
                temp = TYPE_CONVERSION[temp]
            
            ctype = ctype.format(temp)

            struct.attributes.append(gen.Attribute(
                ctype, 
                decl.name.eval(),
                visibility=gen.Visibility.PUBLIC
            ))

        self.structs_file.add(struct)

    def _generate_base_structure(self, base):
        if base != 'has_id':
            return
        
        struct = gen.Class(base, cpp_style=True, keyword='struct')
        struct.attributes.append(gen.Attribute(
            'uint64_t',
            'id',
            visibility=gen.Visibility.PUBLIC
        ))

        self.structs_file.add(struct)
        return struct

    def _generate_message_packer(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        method = gen.Method('void', f'pack', [
            gen.Variable('const boost::intrusive_ptr<::kaminari::packet>&', 'packet'),
            gen.Variable(f'const {message_name}&', 'data')
        ], decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)

        for decl in self.message_fields_including_base(message):
            name = decl.name.eval()

            if decl.optional:
                method.append(gen.Statement(f'*packet << static_cast<bool>(data.{name})'))
                method.append(gen.Statement(f'if (static_cast<bool>(data.{name}))', ending=''))
                method.append(gen.Block([
                    self.__write_type(decl, f'*data.{name}')
                ]))
            else:
                method.append(self.__write_type(decl, f'data.{name}'))

        self.marshal_cls.methods.append(method)
        #self.marshal_file.add(method)
        return [method]

    def _generate_message_unpacker(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        method = gen.Method('bool', f'unpack', [
            gen.Variable('::kaminari::packet_reader*', 'packet'),
            gen.Variable(f'{message_name}&', 'data')
        ], decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)

        for decl in self.message_fields_including_base(message):
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

        method.append(gen.Statement('return true'))
        self.marshal_cls.methods.append(method)
        #self.marshal_file.add(method)
        return method

    def _generate_message_size(self, message: boxes.MessageBox):
        message_name = message.name.eval()

        methods = []
        method = gen.Method('uint8_t', f'packet_size', [
            gen.Variable(f'const {message_name}&', 'data')
        ], decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)
        methods.append(method)

        if self.__is_trivial(message):
            method.append(gen.Statement('(void)data'))
            method.append(gen.Statement(f'return sizeof({message_name})'))

            # Method without parameter
            method = gen.Method('uint8_t', f'sizeof_{message_name}', decl_modifiers=['static'], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'return sizeof({message_name})'))
            methods.append(method)
        else:
            method.append(gen.Statement('uint8_t size = 0'))    
            # Manually loop all types
            for decl in self.message_fields_including_base(message):
                name = decl.name.eval()

                if decl.optional:
                    method.append(gen.Statement('size += sizeof(bool)'))
                    method.append(gen.Statement(f'if (static_cast<bool>(data.{name}))', ending=''))
                    method.append(gen.Block([
                        self.__write_size(decl, f'*data.{name}')
                    ]))
                else:
                    method.append(self.__write_size(decl, f'data.{name}'))
            method.append(gen.Statement('return size'))

        for method in methods:
            self.marshal_cls.methods.append(method)

        return methods

    def _generate_program_send(self, program: boxes.ProgramBox):
        # Helpers
        program_name = program.name.eval()
        queue = program.queue.eval()
        args = program.args.eval()
        message_name = args[0]

        # Returned methods
        methods = []

        # Templated allocators
        allocators = [f'{queue.capitalize()}Allocator' for queue in self.queues.keys()]
        allocators_template = 'class ' + ', class '.join(allocators)
        allocators_names = ', '.join(allocators)
    
        # Not all methods support callback
        if self.can_queue_have_callback(self.queues[queue]):
            method = gen.Method('void', f'send_{program_name}', [
                gen.Variable(f'::kumo::protocol_queues<{allocators_names}>*', 'pq'),
                gen.Variable(f'{message_name}&&', 'data'),
                gen.Variable('T&&', 'callback')
            ], template=gen.Statement(f'template <{allocators_template}, typename T>', ending=''), visibility=gen.Visibility.PUBLIC, decl_modifiers=['inline'])
            method.append(gen.Statement(f'pq->send_{queue}(opcode::{program_name}, std::move(data), std::forward<T>(callback))'))
            methods.append(method)
        
        method = gen.Method('void', f'send_{program_name}', [
            gen.Variable(f'::kumo::protocol_queues<{allocators_names}>*', 'pq'),
            gen.Variable(f'{message_name}&&', 'data')
        ], template=gen.Statement(f'template <{allocators_template}>', ending=''), visibility=gen.Visibility.PUBLIC, decl_modifiers=['inline'])
        method.append(gen.Statement(f'pq->send_{queue}(opcode::{program_name}, std::move(data))'))
        methods.append(method)
        
        # There are two types of broadcasts, one that implies neighbouring areas
        # and one that doesn't, generate both
        for suffix in ('', '_single'):
            if self.has_queue_packed_add(self.queues[queue]):
                
                if self.can_queue_have_callback(self.queues[queue]):
                    method = gen.Method('void', f'broadcast_{program_name}{suffix}', [
                        gen.Variable('::kaminari::broadcaster<B>*', 'broadcaster'),
                        gen.Variable(f'{message_name}&&', 'data'),
                        gen.Variable('T&&', 'callback')
                    ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B, typename T>', ending=''))
                    methods.append(method)

                    method.append(gen.Statement(f'boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::{program_name}, std::forward<T>(callback))'))
                    method.append(gen.Statement(f'::kumo::marshal::pack(packet, data)'))
                    method.append(gen.Statement(f'broadcaster->broadcast([packet](auto pq) {{', ending=''))
                    method.append(gen.Scope([gen.Statement(f'pq->send_{queue}(packet)')], True))
                    method.append(gen.Statement(f'}})'))
                
                method = gen.Method('void', f'broadcast_{program_name}{suffix}', [
                    gen.Variable('::kaminari::broadcaster<B>*', 'broadcaster'),
                    gen.Variable(f'{message_name}&&', 'data')
                ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B>', ending=''))
                methods.append(method)

                method.append(gen.Statement(f'boost::intrusive_ptr<::kaminari::packet> packet = ::kaminari::packet::make((uint16_t)opcode::{program_name})'))
                method.append(gen.Statement(f'::kumo::marshal::pack(packet, data)'))
                method.append(gen.Statement(f'broadcaster->broadcast([packet](auto pq) {{', ending=''))
                method.append(gen.Scope([gen.Statement(f'pq->send_{queue}(packet)')], True))
                method.append(gen.Statement(f'}})'))

            else:
                # Adding by bare data is always available
                # But we can not have callbacks YET
                method = gen.Method('void', f'broadcast_{program_name}{suffix}', [
                    gen.Variable('::kaminari::broadcaster<B>*', 'broadcaster'),
                    gen.Variable(f'{message_name}&&', 'data')
                ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename B>', ending=''))
                methods.append(method)

                method.append(gen.Statement(f'broadcaster->broadcast([data = std::move(data)](auto pq) {{', ending=''))
                method.append(gen.Scope([
                    # Do not move data here, we need it further down in subsequent calls
                    gen.Statement(f'pq->send_{queue}(opcode::{program_name}, data)')
                    ], indent=True)
                )
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
            gen.Variable('::kaminari::packet_reader*', 'packet'),
            gen.Variable('C*', 'client')
        ], template=gen.Statement('template <typename C>', ending=''), visibility=gen.Visibility.PRIVATE, decl_modifiers=['static'])

        if program.cond.attr is not None:
            attr = program.cond.attr.eval()
            value = program.cond.value.eval()
            false_case = program.cond.false_case
            if false_case.action is not None:
                false_case = false_case.action.eval()
            else:
                false_case = 'handle_client_error'

            #method.append(gen.Statement(f'if (client->{attr}() != {attr}::{value})', ending=''))
            method.append(gen.Statement(f'if (!check_client_{attr}(client, {value}))', ending=''))
            method.append(gen.Block([
                gen.Statement(f'return {false_case}(client, static_cast<::kumo::opcode>(packet->opcode()))')
            ]))
        
        method.append(gen.Statement(f'::kumo::{message_name} data'))
        method.append(gen.Statement(f'if (!unpack(packet, data))', ending=''))
        method.append(gen.Block([
            gen.Statement('return false')
        ]))

        method.append(gen.Statement(f'return on_{program_name}(client, data, packet->timestamp())'))

        self.handler_programs.add(program_name)
        self.marshal_cls.methods.append(method)

        return [method]

    def _generate_internals(self):
        # Trivial types size
        for dtype in semantic.TRIVIAL_TYPES:
            ctype = TYPE_CONVERSION[dtype]
            method = gen.Method('uint8_t', f'sizeof_{dtype}', decl_modifiers=['inline', 'constexpr', 'static'], visibility=gen.Visibility.PUBLIC)
            method.append(gen.Statement(f'return static_cast<uint8_t>(sizeof({ctype}))'))
            self.marshal_cls.methods.append(method)

        # General packet handler
        method = gen.Method('bool', 'handle_packet', [
            gen.Variable('::kaminari::packet_reader*', 'packet'),
            gen.Variable('C*', 'client')
        ], template=gen.Statement('template <typename C>', ending=''), visibility=gen.Visibility.PUBLIC, decl_modifiers=['static'])

        method.append(gen.Statement('switch (static_cast<::kumo::opcode>(packet->opcode()))', ending=''))
        method.append(gen.Block([
            gen.Scope([
                gen.Statement(f'case opcode::{program}:', ending=''),
                gen.Scope([
                    gen.Statement(f'return handle_{program}(packet, client)') 
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
        opcodes = gen.Scope([
            gen.Statement('enum class opcode', ending=''),
            gen.Block([
                gen.Statement(f'{name: <16} = 0x{self.opcodes[name]},', ending='') for name in \
                    (program.name.eval() for program in self.programs.values())
            ], ending=';')
        ])
        self.opcodes_file.add(opcodes)

        # Protocol queues
        # for each queue we need a template allocator
        template_names = [f'{queue_name.capitalize()}Allocator' for queue_name, queue in self.queues.items()]
        template = 'template <class ' + ', class '.join(template_names) + '>'

        queues = gen.Class('protocol_queues', cpp_style=True, template=(gen.Statement(template, ending=''), template_names))
        self.queues_file.add(queues)
        
        constructor = gen.Constructor('', 'protocol_queues', [
            gen.Variable('uint8_t', 'resend_threshold'), 
            gen.Variable('Args&&...', 'allocator_args')
        ], visibility=gen.Visibility.PUBLIC, template=gen.Statement('template <typename... Args>', ending=''))
        
        for i, queue_name in enumerate(self.queues.keys()):
            constructor.initializers.append(gen.Statement(f'_{queue_name}(resend_threshold, std::get<{i}>(std::forward_as_tuple(allocator_args...)))', ending=''))

        queues.methods.append(constructor)

        reset = gen.Method('void', 'reset', visibility=gen.Visibility.PUBLIC)
        reset.append(gen.Scope([
            gen.Statement(f'_{queue}.reset()') for queue in self.queues.keys()
        ]))
        queues.methods.append(reset)

        ack = gen.Method('void', 'ack', [gen.Variable('uint16_t', 'block_id')], visibility=gen.Visibility.PUBLIC)
        ack.append(gen.Scope([
            gen.Statement(f'_{queue}.ack(block_id)') for queue in self.queues.keys()
        ]))
        queues.methods.append(ack)

        process = gen.Method('void', 'process', [
            gen.Variable('uint16_t', 'block_id'),
            gen.Variable('uint16_t&', 'remaining'),
            gen.Variable('typename ::kaminari::detail::packets_by_block&', 'by_block')
        ], visibility=gen.Visibility.PUBLIC)
        process.append(gen.Scope([
            gen.Statement(f'_{queue}.process(block_id, remaining, by_block)') for queue in self.queues.keys()
        ]))
        queues.methods.append(process)

        for queue_name, queue in self.queues.items():
            # Attribute
            queue_base = queue.base.subtype.eval()
            queue_packer = 'immediate_packer'
            queue_packer_template = f'<::kumo::marshal, {queue_name.capitalize()}Allocator>'
            if queue.specifier.queue_type == boxes.QueueSpecifierType.SPECIALIZED:
                queue_packer = queue.specifier.args.eval()

            elif queue.specifier.queue_type == boxes.QueueSpecifierType.TEMPLATED:
                queue_packer = 'unique_merge_packer'
                args = queue.specifier.args
                program_name = args[2].eval()

                queue_packer_template = f'<{args[0].eval()}, {args[1].eval()}, ::kumo::opcode::{program_name}, ::kumo::marshal, {queue_name.capitalize()}Allocator>'

            queue_packer = queue_packer + queue_packer_template
            if queue.base.argument is not None:
                queue_packer = f'{queue_packer}, {queue.base.argument.eval()}'

            queues.attributes.append(gen.Attribute(
                f'::kaminari::{queue_base}<::kaminari::{queue_packer}>',
                f'_{queue_name}'
            ))

            # General send with data
            if self.can_queue_have_callback(queue):
                send = gen.Method('void', f'send_{queue_name}', [
                    gen.Variable('::kumo::opcode', 'opcode'),
                    gen.Variable(f'D&&', 'data'),
                    gen.Variable('T&&', 'callback')
                ], template=gen.Statement('template <typename D, typename T>', ending=''), visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'_{queue_name}.add(static_cast<uint16_t>(opcode), std::forward<D>(data), std::forward<T>(callback))'))
                queues.methods.append(send)
            
            send = gen.Method('void', f'send_{queue_name}', [
                gen.Variable('::kumo::opcode', 'opcode'),
                gen.Variable(f'D&&', 'data')
            ], template=gen.Statement('template <typename D>', ending=''), visibility=gen.Visibility.PUBLIC)
            send.append(gen.Statement(f'_{queue_name}.add(static_cast<uint16_t>(opcode), std::forward<D>(data))'))

            queues.methods.append(send)

            if self.has_queue_packed_add(queue):
                send = gen.Method('void', f'send_{queue_name}', [
                    gen.Variable('const boost::intrusive_ptr<::kaminari::packet>&', 'packet')
                ], visibility=gen.Visibility.PUBLIC)
                send.append(gen.Statement(f'_{queue_name}.add(packet)'))
                queues.methods.append(send)
        
    def dump(self, path):
        def kaminari_fwd(code):
            if not isinstance(code, list):
                code = [code]

            return gen.Scope([
                gen.Statement('namespace kaminari', ending=''),
                gen.Block(code)
            ])

        include_path = self.config.get('include_path', 'kumo')

        # Do we need to include marshal base class?
        marshal_include = []
        if self.config.get("marshal", {}).get("base"):
            marshal_include.append(gen.Statement(f'#include "{self.config["marshal"]["include"]}"', ending=''),)

        with open(f'{path}/marshal.hpp', 'w') as fp:
            fp.write(self.marshal_file.header([
                gen.Statement(f'#pragma once', ending=''),
                gen.Statement(f'#include <inttypes.h>', ending=''),
                gen.Statement(f'#include <boost/intrusive_ptr.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/structs.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/buffers/packet.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/buffers/packet_reader.hpp>', ending=''),
                *marshal_include
            ]))

        with open(f'{path}/marshal.cpp', 'w') as fp:
            fp.write(self.marshal_file.source([
                gen.Statement(f'#include <{include_path}/opcodes.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/marshal.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/buffers/packet_reader.hpp>', ending=''),
            ]))

        with open(f'{path}/rpc.hpp', 'w') as fp:
            fp.write(self.rpc_file.header([
                gen.Statement(f'#pragma once', ending=''),
                gen.Statement(f'#include <{include_path}/opcodes.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/protocol_queues.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/structs.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/buffers/packet.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/broadcaster.hpp>', ending='')
            ]))

        with open(f'{path}/rpc.cpp', 'w') as fp:
            fp.write(self.rpc_file.source([
                gen.Statement(f'#include <{include_path}/marshal.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/rpc.hpp>', ending=''),
            ]))

        with open(f'{path}/structs.hpp', 'w') as fp:
            fp.write(self.structs_file.header([
                gen.Statement(f'#pragma once', ending=''),
                gen.Statement(f'#include <optional>', ending=''),
                gen.Statement(f'#include <vector>', ending=''),
                gen.Statement(f'#include <inttypes.h>', ending='')
            ]))

        with open(f'{path}/opcodes.hpp', 'w') as fp:
            fp.write(self.opcodes_file.source([
                gen.Statement(f'#pragma once', ending='')
            ]))

        with open(f'{path}/protocol_queues.hpp', 'w') as fp:
            fp.write(self.queues_file.header([
                gen.Statement(f'#pragma once', ending=''),
                gen.Statement(f'#include <inttypes.h>', ending=''),
                gen.Statement(f'#include <map>', ending=''),
                gen.Statement(f'#include <boost/intrusive_ptr.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/opcodes.hpp>', ending=''),
                gen.Statement(f'#include <{include_path}/marshal.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/queues/reliable_queue.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/queues/unreliable_queue.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/queues/eventually_synced_queue.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/packers/immediate_packer.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/packers/merge_packer.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/packers/most_recent_packer_by_opcode.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/packers/ordered_packer.hpp>', ending=''),
                gen.Statement(f'#include <kaminari/packers/unique_merge_packer.hpp>', ending=''),
                kaminari_fwd(gen.Statement('class packet')),
                kaminari_fwd([
                    gen.Statement('namespace detail', ending=''),
                    gen.Block([
                        gen.Statement('using packets_by_block = std::map<uint32_t, std::vector<boost::intrusive_ptr<packet>>>')
                    ])
                ])
            ]))
        