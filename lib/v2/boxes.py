from rply.token import BaseBox
from enum import Enum

from .custom_cgen import *


class Direction(Enum):
    S2C = 0
    C2S = 1
    BOTH = 2

class QueueSpecifierType(Enum):
    STANDARD = 0
    ARRAY = 1
    SPECIALIZED = 2
    TEMPLATED = 3


class IntBox(BaseBox):
    def __init__(self, value):
        self.value = int(value.getstr())

    def eval(self):
        return self.value

class IdentifierBox(BaseBox):
    def __init__(self, value):
        self.value = value.getstr()

    def eval(self):
        return self.value

class DirectionBox(BaseBox):
    def __init__(self, token):
        if token.value == 'c2s':
            self.value = Direction.C2S
        elif token.value == 's2c':
            self.value = Direction.S2C
        elif token.value == 's<->c':
            self.value = Direction.BOTH
        else:
            assert False, 'Unexpected program direction'
    
    def eval(self):
        return self.value

class TypeBox(BaseBox):
    def __init__(self, dtype, spec=None):
        self.dtype = dtype
        self.spec = spec

    def eval(self, generator):
        dtype = generator.get_dtype(self.dtype.eval())
        if self.spec:
            dtype = f'{dtype}<{generator.get_dtype(self.spec.eval())}>'
        return dtype

class MessageQueueBox(BaseBox):
    def __init__(self, identifier, idx=None):
        self.identifier = identifier
        self.idx = idx

    def eval(self):
        if self.idx is None:
            print(self.identifier.eval())
        else:
            print(self.identifier.eval() + "(" + self.idx.eval() + ")")

class DeclarationBox(BaseBox):
    def __init__(self, dtype, name, optional):
        self.dtype = dtype
        self.name = name
        self.optional = optional

    def eval(self):
        print(self.dtype.eval() + " " + self.name.eval())

class BlockBox(BaseBox):
    def __init__(self, queue, state, fields):
        self.queue = queue
        self.state = state
        self.fields = fields
    
    def eval(self):
        self.queue.eval()
        for field in self.fields.eval():
            field.eval()

class StateBox(BaseBox):
    def __init__(self, enum, state, is_any=False):
        self.enum = enum
        self.state = state
        self.is_any = is_any
    
class FieldsBox(BaseBox):
    def __init__(self, fields=None, field=None):
        self.fields = fields
        self.field = field

    def eval(self):
        if self.fields:
            return self.fields.eval() + [self.field]
        return []

class MessageBox(BaseBox):
    def __init__(self, name, fields, base):
        self.name = name
        self.fields = fields
        self.base = base
    
    def eval(self):
        print("message " + self.name.eval())
        return self.fields.eval()

class MessageBaseBox(BaseBox):
    def __init__(self, name, template):
        self.name = name
        self.template = template

class ProgramBox(BaseBox):
    def __init__(self, queue, direction, name, args, cond):
        self.queue = queue
        self.direction = direction
        self.name = name
        self.args = args
        self.cond = cond

class QueueBox(BaseBox):
    def __init__(self, name, base, specifier):
        self.name = name
        self.base = base
        self.specifier = specifier

class QueueSubtype(BaseBox):
    def __init__(self, subtype, argument=None):
        self.subtype = subtype
        self.argument = argument

PACKERS_WITHOUT_BARE = ('most_recent_packer_with_id', 'most_recent_packer_by_opcode')

class QueueSpecifierBox(BaseBox):
    def __init__(self, queue_type, args):
        self.queue_type = queue_type
        self.args = args

class ArgumentBox(BaseBox):
    def __init__(self, arg, args=None):
        self.arg = arg
        self.args = args

    def eval(self):
        if self.args:
            return self.args.eval() + [self.arg.eval()]
        return [self.arg.eval()]
    
class ConditionBox(BaseBox):
    def __init__(self, attr=None, value=None, false_case=None):
        self.attr = attr
        self.value = value
        self.false_case = false_case

class FalseCaseBox(BaseBox):
    def __init__(self, action=None):
        self.action = action

class MainBox(BaseBox):
    def __init__(self, elements=None, element=None):
        self.elements = elements
        self.element = element

    def eval(self):
        if self.elements:
            return self.elements.eval() + [self.element]
        return []
