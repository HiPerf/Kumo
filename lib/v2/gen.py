from enum import Enum


INDENT_SPACES = 4

class Visibility(Enum):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'


def indent(x, level):
    return ' ' * level * INDENT_SPACES + x


def check_eval_fn(f):
    def inner(self, *args, **kwargs):
        if kwargs.get('eval_fn'):
            if not kwargs['eval_fn'](self):
                return ''

        return f(self, *args, **kwargs)
    
    return inner

class Statement(object):
    def __init__(self, stmt, ending=';'):
        super().__init__()

        self.stmt = stmt
        self.ending = ending

    @check_eval_fn
    def _eval(self, level, fn, eval_fn=None):
        return indent(self.stmt + self.ending + '\n', level)
    
    def decl(self, level, eval_fn=None):
        return self._eval(level, 'decl', eval_fn=eval_fn)

    def instance(self, level, eval_fn=None):
        return self._eval(level, 'instance', eval_fn=eval_fn)
    
    def both(self, level, eval_fn=None):
        return self._eval(level, 'both', eval_fn=eval_fn)

class Scope(list):
    def __init__(self, content=[], indent=False):
        super().__init__(content)
        self.indent = indent

    @check_eval_fn
    def _eval(self, level, fn, eval_fn=None):
        return ''.join(getattr(x, fn)(level + int(self.indent), eval_fn=eval_fn) for x in self)
    
    def decl(self, level, eval_fn=None):
        return self._eval(level, 'decl', eval_fn=eval_fn)

    def instance(self, level, eval_fn=None):
        return self._eval(level, 'instance', eval_fn=eval_fn)
    
    def both(self, level, eval_fn=None):
        return self._eval(level, 'both', eval_fn=eval_fn)

    def __str__(self):
        return self.decl(0)

class Block(Scope):
    def __init__(self, content=[], ending=''):
        super().__init__(content)
        self.ending = ending

    @check_eval_fn
    def _eval(self, level, fn, eval_fn=None):
        preface = indent('{\n', level)
        postface = indent(f'}}{self.ending}\n', level)
        return preface + super()._eval(level + 1, fn, eval_fn=eval_fn) + postface
    
    def decl(self, level, eval_fn=None):
        return self._eval(level, 'decl', eval_fn=eval_fn)

    def instance(self, level, eval_fn=None):
        return self._eval(level, 'instance', eval_fn=eval_fn)
    
    def both(self, level, eval_fn=None):
        return self._eval(level, 'both', eval_fn=eval_fn)

class Variable(object):
    def __init__(self, dtype, name, default=None):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.default = default

    @check_eval_fn
    def decl(self, eval_fn=None):
        if self.default is not None:
            return f'{self.dtype} {self.name} = {self.default}'

        return self.instance(eval_fn=eval_fn) 

    @check_eval_fn
    def instance(self, eval_fn=None):
        return f'{self.dtype} {self.name}'
    
    @check_eval_fn
    def both(self, eval_fn=None):
        return self.decl(eval_fn=eval_fn)

class Method(Block):
    def __init__(self, dtype, name, parameters = [], decl_modifiers = [], visibility=Visibility.PRIVATE, template=None):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.parameters = parameters
        self.decl_modifiers = decl_modifiers
        self.visibility = visibility
        self.template = template

    @check_eval_fn
    def decl(self, level, modifiers=[], eval_fn=None):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.decl(eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        return template + indent(f'{modifiers}{self.dtype} {self.name}({parameters});\n', level)

    @check_eval_fn
    def instance(self, level, name_ns='', eval_fn=None):
        parameters = ', '.join(x.instance(eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        fnc = template + indent(f'{self.dtype} {name_ns}{self.name}({parameters})\n', level)
        return fnc + super().instance(level, eval_fn=eval_fn)

    @check_eval_fn
    def both(self, level, modifiers=[], name_ns='', eval_fn=None):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.both(eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        fnc = template + indent(f'{modifiers}{self.dtype} {name_ns}{self.name}({parameters})\n', level)
        return fnc + super().both(level, eval_fn=eval_fn)

class Attribute(object):
    def __init__(self, dtype, name, default=None, visibility=Visibility.PRIVATE):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.default = default
        self.visibility = visibility

    @check_eval_fn
    def decl(self, level, modifiers=[], eval_fn=None):
        if self.default is not None:
            modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
            return Statement(f'{modifiers}{self.dtype} {self.name} = {self.default}').decl(level, eval_fn=eval_fn)

        return self.instance(level, eval_fn=eval_fn) 

    @check_eval_fn
    def instance(self, level, modifiers=[], eval_fn=None):
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        return Statement(f'{modifiers}{self.dtype} {self.name}').instance(level, eval_fn=eval_fn)
    
    @check_eval_fn
    def both(self, level, modifiers=[], eval_fn=None):
        return self.decl(level, modifiers=modifiers, eval_fn=eval_fn)

class Class(object):
    def __init__(self, name, decl_modifiers=[], decl_name_base='', cpp_style=False, csharp_style=False, keyword='class'):
        self.keyword = keyword
        self.name = name
        self.decl_modifiers = decl_modifiers
        self.decl_name_base = decl_name_base
        self.cpp_style = cpp_style
        self.csharp_style = csharp_style
        self.methods = []
        self.attributes = []

    def _decl_attributes(self, visibility, level, eval_fn=None):
        modifiers = [] if not self.csharp_style else [visibility.value]
        attributes = (x.decl(level, modifiers, eval_fn=eval_fn) for x in self.attributes if x.visibility == visibility)
        attributes = ''.join(attributes)

        if self.cpp_style and attributes:
            return indent(visibility.value + ':\n', level - 1) + attributes

        return attributes

    def _decl_methods(self, visibility, level, eval_fn=None):
        modifiers = [] if not self.csharp_style else [visibility.value]
        methods = (x.decl(level, modifiers, eval_fn=eval_fn) for x in self.methods if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style and methods:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    def _in_decl_templates(self, level, eval_fn=None):
        name_ns = '' if not self.cpp_style else f'{self.name}::'
        return ''.join(x.instance(level, name_ns, eval_fn=eval_fn) for x in self.methods if x.template is not None)
    
    def _instance_methods(self, visibility, level, templates=False, eval_fn=None):
        name_ns = '' if not self.cpp_style else f'{self.name}::'
        return ''.join(x.instance(level, name_ns, eval_fn=eval_fn) for x in self.methods if x.visibility == visibility and (templates or x.template is None))

    def _both_methods(self, visibility, level, eval_fn=None):
        modifiers = [] if not self.csharp_style else [visibility.value]
        methods = (x.both(level, modifiers, eval_fn=eval_fn) for x in self.methods if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    @check_eval_fn
    def decl(self, level, eval_fn=None):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'

        modifiers = '' if not self.decl_modifiers else (' '.join(self.decl_modifiers) + ' ')
        decl_name_base = '' if not self.decl_name_base else f' {self.decl_name_base} '
        ending = '' if not self.cpp_style else ';'
        cls = indent(f'{modifiers}{self.keyword} {self.name}{decl_name_base}\n', level)
        preface = indent('{\n', level)
        postface = indent('}' + ending + '\n', level)

        return cls + preface + \
            self._decl_methods(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._decl_methods(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._decl_methods(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            postface + '\n' + \
            self._in_decl_templates(level, eval_fn=eval_fn)

    @check_eval_fn
    def instance(self, level, eval_fn=None):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'

        return self._instance_methods(Visibility.PUBLIC, level, eval_fn=eval_fn) + \
            self._instance_methods(Visibility.PROTECTED, level, eval_fn=eval_fn) + \
            self._instance_methods(Visibility.PRIVATE, level, eval_fn=eval_fn)
    
    @check_eval_fn
    def both(self, level, eval_fn=None):
        if self.cpp_style:
            return ''

        modifiers = '' if not self.decl_modifiers else (' '.join(self.decl_modifiers) + ' ')
        ending = '' if not self.cpp_style else ';'
        cls = indent(f'{modifiers}{self.keyword} {self.name}\n', level)
        preface = indent('{\n', level)
        postface = indent('}' + ending + '\n', level)

        return cls + preface + \
            self._both_methods(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._both_methods(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._both_methods(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            postface + '\n' + \
            ('' if self.csharp_style else self._in_decl_templates(level, eval_fn=eval_fn))
