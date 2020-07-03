from enum import Enum


INDENT_SPACES = 4

def indent(x, level):
    return ' ' * level * INDENT_SPACES + x

class Statement(object):
    def __init__(self, stmt, ending=';'):
        super().__init__()

        self.stmt = stmt
        self.ending = ending

    def _eval(self, level, fn):
        return indent(self.stmt + self.ending + '\n', level)
    
    def decl(self, level):
        return self._eval(level, 'decl')

    def instance(self, level):
        return self._eval(level, 'instance')
    
    def both(self, level):
        return self._eval(level, 'both')

class Scope(list):
    def __init__(self, content=[], indent=False):
        super().__init__(content)
        self.indent = indent

    def _eval(self, level, fn):
        return ''.join(getattr(x, fn)(level + int(self.indent)) for x in self)
    
    def decl(self, level):
        return self._eval(level, 'decl')

    def instance(self, level):
        return self._eval(level, 'instance')
    
    def both(self, level):
        return self._eval(level, 'both')

    def __str__(self):
        return self.decl(0)

class Block(Scope):
    def __init__(self, content=[]):
        super().__init__(content)

    def _eval(self, level, fn):
        preface = indent('{\n', level)
        postface = indent('}\n', level)
        return preface + super()._eval(level + 1, fn) + postface
    
    def decl(self, level):
        return self._eval(level, 'decl')

    def instance(self, level):
        return self._eval(level, 'instance')
    
    def both(self, level):
        return self._eval(level, 'both')

class Variable(object):
    def __init__(self, dtype, name, default=None):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.default = default

    def decl(self):
        if self.default is not None:
            return f'{self.dtype} {self.name} = {self.default}';

        return self.instance() 

    def instance(self):
        return f'{self.dtype} {self.name}'

    def both(self):
        return self.decl()

class Visibility(Enum):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

class Method(Block):
    def __init__(self, dtype, name, parameters = [], decl_modifiers = [], visibility=Visibility.PRIVATE, template=None):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.parameters = parameters
        self.decl_modifiers = decl_modifiers
        self.visibility = visibility
        self.template = template

    def decl(self, level, modifiers=[]):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.decl() for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level)
        return template + indent(f'{modifiers}{self.dtype} {self.name}({parameters});\n', level)

    def instance(self, level, name_ns=''):
        parameters = ', '.join(x.instance() for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level)
        fnc = template + indent(f'{self.dtype} {name_ns}{self.name}({parameters})\n', level)
        return fnc + super().instance(level)

    def both(self, level, modifiers=[], name_ns=''):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.both() for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level)
        fnc = template + indent(f'{modifiers}{self.dtype} {name_ns}{self.name}({parameters})\n', level)
        return fnc + super().both(level)

class Class(list):
    def __init__(self, name, decl_modifiers=[], cpp_style=False, csharp_style=False):
        self.name = name
        self.decl_modifiers = decl_modifiers
        self.cpp_style = cpp_style
        self.csharp_style = csharp_style

    def _decl_methods(self, visibility, level):
        modifiers = [] if not self.csharp_style else [visibility.value]
        methods = (x.decl(level, modifiers) for x in self if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    def _in_decl_templates(self, level):
        name_ns = '' if not self.cpp_style else f'{self.name}::'
        return ''.join(x.instance(level, name_ns) for x in self if x.template is not None)
    
    def _instance_methods(self, visibility, level, templates=False):
        name_ns = '' if not self.cpp_style else f'{self.name}::'
        return ''.join(x.instance(level, name_ns) for x in self if x.visibility == visibility and (templates or x.template is None))

    def _both_methods(self, visibility, level):
        modifiers = [] if not self.csharp_style else [visibility.value]
        methods = (x.both(level, modifiers) for x in self if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    def decl(self, level):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'

        modifiers = '' if not self.decl_modifiers else (' '.join(self.decl_modifiers) + ' ')
        ending = '' if not self.cpp_style else ';'
        cls = indent(f'{modifiers}class {self.name}\n', level)
        preface = indent('{\n', level)
        postface = indent('}' + ending + '\n', level)

        return cls + preface + \
            self._decl_methods(Visibility.PUBLIC, level + 1) + \
            self._decl_methods(Visibility.PROTECTED, level + 1) + \
            self._decl_methods(Visibility.PRIVATE, level + 1) + \
            postface + '\n' + \
            self._in_decl_templates(level)

    def instance(self, level):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'

        return self._instance_methods(Visibility.PUBLIC, level) + \
            self._instance_methods(Visibility.PROTECTED, level) + \
            self._instance_methods(Visibility.PRIVATE, level)
    
    def both(self, level):
        modifiers = '' if not self.decl_modifiers else (' '.join(self.decl_modifiers) + ' ')
        ending = '' if not self.cpp_style else ';'
        cls = indent(f'{modifiers}class {self.name}\n', level)
        preface = indent('{\n', level)
        postface = indent('}' + ending + '\n', level)

        return cls + preface + \
            self._both_methods(Visibility.PUBLIC, level + 1) + \
            self._both_methods(Visibility.PROTECTED, level + 1) + \
            self._both_methods(Visibility.PRIVATE, level + 1) + \
            postface + '\n' + \
            ('' if self.csharp_style else self._in_decl_templates(level))
