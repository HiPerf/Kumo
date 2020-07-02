from .boxes import *
import cgen as c


WRITE_MAP = {
    'uint8' : 'Int8',
    'int8': 'Int8',
    'uint16' : 'Int16',
    'int16': 'Int16',
    'uint32' : 'Int32',
    'int32': 'Int32',
    'uint64' : 'Int64',
    'int64': 'Int64',
    'bool': 'bool'
}

READ_MAP = {
    'uint8' : 'UInt8',
    'int8': 'Int8',
    'uint16' : 'UInt16',
    'int16': 'Int16',
    'uint32' : 'UInt32',
    'int32': 'Int32',
    'uint64' : 'UInt64',
    'int64': 'Int64',
    'bool': 'bool'
}

def base_methods(base, message_name, subtype=None):
    base_name = None
    if base.name is not None:
        base_name = base.name.eval()
        inherits = f' : {base_name}'
        if base.template:
            subtype = base.template.eval()
            inherits = f'{inherits}<{subtype}>'
    else:
        inherits = ' : IData'

    methods =  [
        CSharpMethod('override void', 'pack', 
            [
                c.Value('Packet', 'packet')
            ], 
            c.Block([c.Statement(f'marshal.pack_{message_name}(packet, this)')])
        ),
        CSharpMethod('override byte', 'size', [], 
            c.Block([c.Statement(f'return marshal.message_size(this)')])
        ),
    ]

    if base_name == 'has_id':
        methods += [
            CSharpMethod('override ulong', 'get_id', [], c.Block([c.Statement('return id')])),
            CSharpMethod('override void', 'set_id', [c.Value('ulong', 'id_')], c.Block([c.Statement('id = id_')]))
        ]
    elif base_name == 'has_data_vector':
        methods += [
            CSharpMethod(f'override List<{subtype}>', 'get_data', [], c.Block([c.Statement('return data')])),
            CSharpMethod('override void', 'init', [], c.Block([c.Statement(f'data = new List<{subtype}>()')]))
        ]

    return methods, inherits

class WrapStruct(object):
    def __init__(self, base):
        self.base = base

    def eval(self, generator):
        if isinstance(self.base, MessageBox):
            methods, inherits = base_methods(self.base.base, self.base.name.eval())

            return CSharpClass(
                f'{self.base.name.eval()}{inherits}',
                methods, [], [],
                WrapStruct(self.base.block).eval(generator), [], []
            )
        
        elif isinstance(self.base, BlockBox):
            return [WrapStruct(x).eval(generator) for x in self.base.fields.eval()]

        elif isinstance(self.base, DeclarationBox):
            dtype = self.base.dtype.eval(generator)
            if self.base.optional:
                dtype = f'Optional<{dtype}>'
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
                c.Statement(f'packet.Data.WriteInt8((byte)(({variable}).Count))'),
                CSharpRangedFor('var x', variable, c.Block([
                    c.Statement(f'packet.Data.Write{WRITE_MAP[spec]}(x)') if generator.is_trivial(spec) else \
                        c.Statement(f'pack_{spec}(packet, x)')
                ]))
            ])
        else:
            if generator.is_trivial(dtype):
                return c.Statement(f'packet.Data.Write{WRITE_MAP[dtype]}({variable})')
            else:
                return c.Statement(f'pack_{dtype}(packet, {variable})')

    def eval(self, generator):
        block = c.Collection()
        raw_variable = f'data.{self.base.name.eval()}'
        if self.base.optional:
            variable = f'{raw_variable}.Value'
            
            block.append(c.Statement(f'packet.Data.WriteByte((byte)Convert.ToInt32({raw_variable}.HasValue))'))
            block.append(c.If(
                f'{raw_variable}.HasValue',
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
            f'packet.Data.Size + {size} > packet.length()',
            c.Block([c.Statement('return false')])
        )

    def _unpack_vector(self, generator, variable):
        spec = self.base.dtype.spec.eval()
        if generator.is_trivial(spec):
            return c.Block([
                self._guard(f'sizeof({spec})'),
                c.Statement(f'{variable}.Add(packet.Data.Read{READ_MAP[spec]}())')
            ])
        else:
            return c.Block([
                c.Statement(f'{spec} var = new {spec}()'),
                c.Statement(f'{variable}.Add(var)'),
                c.If(
                    f'!unpack_{spec}(packet, var)',
                    c.Block([c.Statement('return false')])
                )
            ])

    def _unpack(self, generator, variable, idl_dtype, dtype):
        if generator.is_trivial(idl_dtype):
            return c.Collection([
                self._guard(f'sizeof({dtype})'),
                c.Statement(f'{variable} = packet.Data.Read{READ_MAP[idl_dtype]}()')
            ])
        elif idl_dtype == 'string':
            # TODO(gpascualg): Not the solution i enjoy the most
            return c.Collection([
                c.If(
                    f'!unpack_{idl_dtype}(packet, ref {variable})',
                    c.Block([c.Statement('return false')])
                )
            ])
        else:
            return c.Collection([
                c.Statement(f'{variable} = new {idl_dtype}()'),
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
                'packet.Data.ReadByte() == 1',
                conditional_block
            ))
            block = conditional_block
            variable = f'{variable}.Value'
            
        if idl_dtype == 'vector':
            spec = self.base.dtype.spec.eval()

            block.append(self._guard('sizeof(byte)'))
            block.append(c.Statement(f'var size_{spec} = packet.Data.ReadUInt8()'))
            block.append(c.If(
                f'size_{spec} > 0',
                c.Block([
                    c.Statement(f'{variable} = new List<{spec}>(size_{spec})'),
                    c.For('byte i = 0', f'i < size_{spec}', '++i',
                        self._unpack_vector(generator, variable)
                    )
                ])
            ))
        else:
            block.append(self._unpack(generator, variable, idl_dtype, dtype))
    
        return ret_block
