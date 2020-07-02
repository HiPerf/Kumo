from .boxes import *
import cgen as c


class WrapStruct(object):
    def __init__(self, base):
        self.base = base

    def eval(self, generator):
        if isinstance(self.base, MessageBox):
            inherits = ''
            if self.base.base.name:
                inherits = f' : public {self.base.base.name.eval()}'
                if self.base.base.template:
                    inherits = f'{inherits}<{self.base.base.template.eval()}>'

            return c.Struct(
                f'{self.base.name.eval()}{inherits}',
                WrapStruct(self.base.block).eval(generator)
            )

        elif isinstance(self.base, BlockBox):
            return [WrapStruct(x).eval(generator) for x in self.base.fields.eval()]

        elif isinstance(self.base, DeclarationBox):
            dtype = self.base.dtype.eval(generator)
            if self.base.optional:
                dtype = f'std::optional<{dtype}>'
            return c.Value(dtype, self.base.name.eval())

class WrapPack(object):
    def __init__(self, base):
        assert isinstance(base, DeclarationBox)
        self.base = base

    def _pack(self, generator, variable):
        dtype = self.base.dtype.dtype.eval()
        if dtype == 'vector':
            spec = self.base.dtype.spec.eval()
            return c.Collection([
                c.Statement(f'*packet << static_cast<uint8_t>(({variable}).size())'),
                CppRangedFor('auto& x', variable, c.Block([
                    c.Statement('*packet << x') if generator.is_trivial(spec) else \
                        c.Statement(f'pack_{spec}(packet, x)')
                ]))
            ])
        else:
            if generator.is_trivial(dtype):
                return c.Statement(f'*packet << {variable}')
            else:
                return c.Statement(f'pack_{dtype}(packet, {variable})')

    def eval(self, generator):
        block = c.Collection()
        raw_variable = f'data.{self.base.name.eval()}'
        if self.base.optional:
            variable = f'*{raw_variable}'
            
            block.append(c.Statement(f'*packet << static_cast<bool>({raw_variable})'))
            block.append(c.If(
                raw_variable,
                c.Block([self._pack(generator, variable)])
            ))
        else:
            block.append(self._pack(generator, raw_variable))
        
        return block

class WrapUnpack(object):
    def __init__(self, base):
        assert isinstance(base, DeclarationBox)
        self.base = base

    @staticmethod
    def _guard(size):
        return c.If(
            f'packet->size() + {size} > packet->length()',
            c.Block([c.Statement('return false')])
        )

    def _unpack_vector(self, generator, variable):
        spec = self.base.dtype.spec.eval()
        if generator.is_trivial(spec):
            return c.Block([
                self._guard(f'sizeof({spec})'),
                c.Statement(f'{variable}.push_back(packet->read<{spec}>())')
            ])
        else:
            return c.Block([
                c.If(
                    f'!unpack_{spec}(packet, {variable}.emplace_back())',
                    c.Block([c.Statement('return false')])
                )
            ])

    def _unpack(self, generator, variable, idl_dtype, dtype):
        if generator.is_trivial(idl_dtype):
            return c.Collection([
                self._guard(f'sizeof({dtype})'),
                c.Statement(f'{variable} = packet->read<{dtype}>()')
            ])
        else:
            return c.Collection([
                c.If(
                    f'!unpack_{idl_dtype}(packet, {variable})',
                    c.Block([c.Statement('return false')])
                )
            ])

    def eval(self, generator):
        variable = f'data.{self.base.name.eval()}'
        idl_dtype = self.base.dtype.dtype.eval()
        dtype = generator.get_dtype(idl_dtype)
        
        ret_block = block = c.Collection()
        if self.base.optional:
            conditional_block = c.Block()
            block.append(self._guard('sizeof(bool)'))
            block.append(c.If(
                'packet->read<bool>()',
                conditional_block
            ))
            block = conditional_block
            variable = f'(*{variable})'
            
        if idl_dtype == 'vector':
            spec = self.base.dtype.spec.eval()

            block.append(self._guard('sizeof(uint8_t)'))
            block.append(c.If(
                f'auto size_{spec} = packet->read<uint8_t>(); size_{spec} > 0',
                c.Block([
                    c.Statement(f'{variable}.reserve(size_{spec})'),
                    c.For('uint8_t i = 0', f'i < size_{spec}', '++i',
                        self._unpack_vector(generator, variable)
                    )
                ])
            ))
        else:
            block.append(self._unpack(generator, variable, idl_dtype, dtype))
    
        return ret_block
