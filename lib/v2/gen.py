from enum import Enum


INDENT_SPACES = 4

class Visibility(Enum):
    PUBLIC =        'public'
    PROTECTED =     'protected'
    PRIVATE =       'private'


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
    def _eval(self, level, fn, eval_fn=None, no_newline=False):
        return indent(self.stmt + self.ending + ('' if no_newline else '\n'), level)
    
    def decl(self, level, eval_fn=None, no_newline=False):
        return self._eval(level, 'decl', eval_fn=eval_fn, no_newline=no_newline)

    def instance(self, level, eval_fn=None, no_newline=False):
        return self._eval(level, 'instance', eval_fn=eval_fn, no_newline=no_newline)
    
    def both(self, level, eval_fn=None, no_newline=False):
        return self._eval(level, 'both', eval_fn=eval_fn, no_newline=no_newline)

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
    def decl(self, level, eval_fn=None):
        if self.default is not None:
            return indent(f'{self.dtype} {self.name} = {self.default}', level)

        return indent(self.instance(level, eval_fn=eval_fn), level)

    @check_eval_fn
    def instance(self, level, eval_fn=None):
        return indent(f'{self.dtype} {self.name}', level)
    
    @check_eval_fn
    def both(self, level, eval_fn=None):
        return indent(self.decl(level, eval_fn=eval_fn), level)

class Method(Block):
    def __init__(self, dtype, name, parameters = None, decl_modifiers = None, visibility=Visibility.PRIVATE, template=None, interface=False, hide_visibility=False):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.parameters = parameters or []
        self.decl_modifiers = decl_modifiers or []
        self.visibility = visibility
        self.template = template
        self.interface = interface
        self.hide_visibility = hide_visibility

    @check_eval_fn
    def decl(self, level, modifiers=[], eval_fn=None):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.decl(0, eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        return template + indent(f'{modifiers}{self.dtype} {self.name}({parameters});\n', level)

    @check_eval_fn
    def instance(self, level, name_ns='', modifiers=[], postfix='', eval_fn=None):
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.instance(0, eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        fnc = template + indent(f'{modifiers}{self.dtype} {name_ns}{self.name}({parameters}){postfix}\n', level)
        return fnc + super().instance(level, eval_fn=eval_fn)

    @check_eval_fn
    def both(self, level, modifiers=[], name_ns='', postfix='', eval_fn=None):
        modifiers = modifiers + self.decl_modifiers
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        parameters = ', '.join(x.both(0, eval_fn=eval_fn) for x in self.parameters)
        template = '' if self.template is None else self.template.decl(level, eval_fn=eval_fn)
        postfix = postfix if not self.interface else ';'
        fnc = template + indent(f'{modifiers}{self.dtype} {name_ns}{self.name}({parameters}){postfix}\n', level)
        if self.interface:
            return fnc
        return fnc + super().both(level, eval_fn=eval_fn)

class Constructor(Method):
    def __init__(self, dtype, name, parameters = None, decl_modifiers = None, visibility=Visibility.PRIVATE, template=None):
        super().__init__(dtype, name, parameters, decl_modifiers, visibility, template)
        self.initializers = []

    @check_eval_fn
    def instance(self, level, name_ns='', modifiers=[], eval_fn=None):
        initializers = ''
        if self.initializers:
            initializers = ':\n' + ',\n'.join(x.instance(level + 1, no_newline=True) for x in self.initializers)
        
        return super().instance(level, name_ns, modifiers, initializers)

    @check_eval_fn
    def both(self, level, name_ns='', eval_fn=None):
        initializers = ''
        if self.initializers:
            initializers = ':\n' + '\n'.join(x.both(level + 1, no_newline=True) for x in self.initializers)
        
        return super().both(level, name_ns, initializers)

class Attribute(object):
    def __init__(self, dtype, name, default=None, decl_modifiers=None, visibility=Visibility.PRIVATE):
        super().__init__()

        self.dtype = dtype
        self.name = name
        self.default = default
        self.visibility = visibility
        self.decl_modifiers = decl_modifiers or []

    @check_eval_fn
    def decl(self, level, modifiers=[], eval_fn=None):
        if self.default is not None:
            modifiers = '' if not (modifiers + self.decl_modifiers) else (' '.join(modifiers + self.decl_modifiers) + ' ')
            return Statement(f'{modifiers}{self.dtype} {self.name} = {self.default}').decl(level, eval_fn=eval_fn)

        return self.instance(level, modifiers=modifiers + self.decl_modifiers, eval_fn=eval_fn) 

    @check_eval_fn
    def instance(self, level, modifiers=[], eval_fn=None):
        modifiers = '' if not modifiers else (' '.join(modifiers) + ' ')
        return Statement(f'{modifiers}{self.dtype} {self.name}').instance(level, eval_fn=eval_fn)
    
    @check_eval_fn
    def both(self, level, modifiers=[], eval_fn=None):
        return self.decl(level, modifiers=modifiers, eval_fn=eval_fn)

class Class(object):
    def __init__(self, name, decl_modifiers=None, decl_name_base='', template=(None, None), cpp_style=False, csharp_style=False, keyword='class'):
        self.keyword = keyword
        self.name = name
        self.decl_modifiers = decl_modifiers or []
        self.decl_name_base = decl_name_base
        self.cpp_style = cpp_style
        self.csharp_style = csharp_style
        self.template_decl = template[0]
        self.template_names = template[1]
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
        methods = (x.decl(level, modifiers if not x.hide_visibility else [], eval_fn=eval_fn) for x in self.methods if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style and methods:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    def _get_template_args(self, level):
        preface = ''
        template_names = ''
        if self.template_decl is not None:
            preface = self.template_decl.instance(level)
            template_names = '<' + ', '.join(self.template_names) + '>'

        return preface, template_names

    def _in_decl_templates(self, level, eval_fn=None):
        preface, template_names = self._get_template_args(level)
        name_ns = '' if not self.cpp_style else f'{self.name}{template_names}::'
        return ''.join(preface + x.instance(level, name_ns, modifiers=[y for y in x.decl_modifiers if y in ('inline', 'constexpr')], eval_fn=None) \
            for x in self.methods if self.template_decl is not None or x.template is not None or 'inline' in x.decl_modifiers)
    
    def _instance_methods(self, visibility, level, templates=False, eval_fn=None):
        preface, template_names = self._get_template_args(level)
        name_ns = '' if not self.cpp_style else f'{self.name}{template_names}::'
        return preface + ''.join(x.instance(level, name_ns, eval_fn=eval_fn) for x in self.methods if x.visibility == visibility and (templates or x.template is None))

    def _both_methods(self, visibility, level, eval_fn=None):
        modifiers = [] if not self.csharp_style else [visibility.value]
        methods = (x.both(level, modifiers if not x.hide_visibility else [], eval_fn=eval_fn) for x in self.methods if x.visibility == visibility)
        methods = ''.join(methods)

        if self.cpp_style and methods:
            return indent(visibility.value + ':\n', level - 1) + methods

        return methods

    @check_eval_fn
    def decl(self, level, eval_fn=None):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'
        preface, _ = self._get_template_args(level)
        return preface + Statement(f'{self.keyword} {self.name}').decl(level, eval_fn=eval_fn)

    @check_eval_fn
    def instance(self, level, eval_fn=None):
        assert not self.csharp_style, 'Call \'both\' in csharp_style'

        if self.template_decl is not None:
            return ''

        return self._instance_methods(Visibility.PUBLIC, level, eval_fn=eval_fn) + \
            self._instance_methods(Visibility.PROTECTED, level, eval_fn=eval_fn) + \
            self._instance_methods(Visibility.PRIVATE, level, eval_fn=eval_fn)
    
    @check_eval_fn
    def both(self, level, eval_fn=None):
        template_preface, _ = self._get_template_args(level)
        modifiers = '' if not self.decl_modifiers else (' '.join(self.decl_modifiers) + ' ')
        ending = '' if not self.cpp_style else ';'
        cls = indent(f'{modifiers}{self.keyword} {self.name}{self.decl_name_base}\n', level)
        preface = indent('{\n', level)
        postface = indent('}' + ending + '\n', level)

        if self.cpp_style:
            # eval_fn is omitted on purpouse in the _decl_methods calls

            return template_preface + cls + preface + \
                self._decl_methods(Visibility.PUBLIC, level + 1) + \
                self._decl_methods(Visibility.PROTECTED, level + 1) + \
                self._decl_methods(Visibility.PRIVATE, level + 1) + \
                self._decl_attributes(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
                self._decl_attributes(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
                self._decl_attributes(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
                postface + '\n' + \
                ('' if self.csharp_style else self._in_decl_templates(level, eval_fn=eval_fn))

        return cls + preface + \
            self._both_methods(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._both_methods(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._both_methods(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PUBLIC, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PROTECTED, level + 1, eval_fn=eval_fn) + \
            self._decl_attributes(Visibility.PRIVATE, level + 1, eval_fn=eval_fn) + \
            postface + '\n'
