import cgen as c


class TemplateSemicolon(c.Template):
    def generate(self):
        return super(TemplateSemicolon, self).generate(with_semicolon=True)

class CppRangedFor(c.Loop):
    def __init__(self, variable, container, body):
        self.variable = variable
        self.container = container

        assert isinstance(body, c.Generable)
        self.body = body

    def intro_line(self):
        return "for (%s : %s)" % (self.variable, self.container)

    mapper_method = "map_for"

class CppMethod(c.Generable):
    def __init__(self, dtype, name, args, body, template: tuple=None, modifiers=''):
        self.dtype = dtype
        self.name = name
        self.value = c.Value(dtype, name)
        self.modifiers = modifiers
        self.is_template = template is not None
        decl = c.FunctionDeclaration(self.value, args)

        if self.is_template:
            decl = c.Template(template[0], decl)

        self.fnc = c.FunctionBody(
            decl,
            body
        )

    def generate(self, with_semicolon=False, header=True, classname=None):
        if not header and self.is_template:
            return []

        if classname:
            self.value.name = f'{classname}::{self.name}'
            self.value.typename = self.dtype
        else:
            modifiers = ''
            if self.modifiers:
                modifiers = self.modifiers + ' '

            self.value.name = self.name
            self.value.typename = f'{modifiers}{self.dtype}'

        if header and not self.is_template:
            tp_lines = self.fnc.fdecl.generate()
        else:
            tp_lines = self.fnc.generate()
            
        for line in tp_lines:
            yield line

class CppClass(c.Declarator):
    def __init__(self, tpname, public_methods, protected_methods, private_methods,
        public_attrs, protected_attrs, private_attrs, header=True):
        """Initialize the structure declarator.
        *tpname* is the name of the structure, while *declname* is the
        name used for the declarator. *pad_bytes* is the number of
        padding bytes added at the end of the structure.
        *fields* is a list of :class:`Declarator` instances.
        """
        self.tpname = tpname
        self.public_methods = public_methods
        self.protected_methods = protected_methods
        self.private_methods = private_methods
        self.public_attrs = public_attrs
        self.protected_attrs = protected_attrs
        self.private_attrs = private_attrs
        self.header = header

    def source(self):
        return CppClass(
            self.tpname, 
            self.public_methods, self.protected_methods, self.private_methods,
            self.public_attrs, self.protected_attrs, self.private_attrs,
            False
        )

    def get_decl_pair(self):
        if self.header:
            return self.get_header_pair()
        return self.get_body_pair()

    def get_header_pair(self):
        def get_tp():
            yield "class %s" % self.tpname
            yield "{"
            
            if self.public_methods:
                yield "public:"
                for f in self.public_methods:
                    for f_line in f.generate():
                        yield "  " + f_line

            if self.protected_methods:
                yield "protected:"
                for f in self.protected_methods:
                    for f_line in f.generate():
                        yield "  " + f_line

            if self.private_methods:
                yield "private:"
                for f in self.private_methods:
                    for f_line in f.generate():
                        yield "  " + f_line

            if self.public_attrs:
                yield "public:"
                for f in self.public_attrs:
                    for f_line in f.generate():
                        yield "  " + f_line

            if self.protected_attrs:
                yield "protected:"
                for f in self.protected_attrs:
                    for f_line in f.generate():
                        yield "  " + f_line

            if self.private_attrs:
                yield "private:"
                for f in self.private_attrs:
                    for f_line in f.generate():
                        yield "  " + f_line
            
            yield "} " + self.struct_attributes()
        return get_tp(), None

    def get_body_pair(self):
        def get_tp():
            for f in self.public_methods:
                for f_line in f.generate(header=False, classname=self.tpname):
                    yield f_line
                    
            for f in self.protected_methods:
                for f_line in f.generate(header=False, classname=self.tpname):
                    yield f_line
                    
            for f in self.private_methods:
                for f_line in f.generate(header=False, classname=self.tpname):
                    yield f_line

        return get_tp(), None

    def generate(self):
        return super(CppClass, self).generate(with_semicolon=self.header)

    def alignment_requirement(self):
        return max(
            max(f.alignment_requirement() for f in self.public_attrs),
            max(f.alignment_requirement() for f in self.protected_attrs),
            max(f.alignment_requirement() for f in self.private_attrs)
        )

    def struct_attributes(self):
        return ""

    mapper_method = "map_struct"


class CSharpRangedFor(c.Loop):
    def __init__(self, variable, container, body):
        self.variable = variable
        self.container = container

        assert isinstance(body, c.Generable)
        self.body = body

    def intro_line(self):
        return "foreach (%s in %s)" % (self.variable, self.container)

    mapper_method = "map_for"

class CSharpStruct(c.Struct):
    def __init__(self, *args, visibility='public', **kwargs):
        self.visibility = visibility
        super(CSharpStruct, self).__init__(*args, **kwargs)

    def get_decl_pair(self):
        def get_tp():
            if self.tpname is not None:
                yield f"{self.visibility} class {self.tpname}"
            else:
                yield f"{self.visibility} class"
            yield "{"
            for f in self.fields:
                for f_line in f.generate():
                    yield f"  {self.visibility} " + f_line
            if self.pad_bytes:
                yield "  unsigned char _cgen_pad[%d];" % self.pad_bytes
            yield "} " + self.struct_attributes()
        return get_tp(), self.declname
    
    def generate(self):
        return super(CSharpStruct, self).generate(with_semicolon=False)

class CSharpMethod(c.Generable):
    def __init__(self, dtype, name, args, body, template: tuple=None):
        self.name = name
        self.is_template = template is not None

        if self.is_template:
            self.name = f'{self.name}<{template[1]}>'

        self.value = c.Value(dtype, self.name)
        self.decl = c.FunctionDeclaration(self.value, args)

        if body is None:
            self.fnc = None
        else:
            self.fnc = c.FunctionBody(
                self.decl,
                body
            )

        self.modifiers = []
        self.constraints = []

    def modifier(self, mod):
        self.modifiers.append(mod)
        return self

    def where(self, constraint):
        self.constraints.append(constraint)
        return self

    def generate(self, visibility, with_semicolon=False, header=True, classname=None):
        tp_lines = iter(self.decl.generate()) if self.fnc is None else iter(self.fnc.generate())
        constraints = ''
        if self.is_template and self.constraints:
            constraints = ' where ' + ', '.join(self.constraints)

        yield ' '.join((visibility, *self.modifiers)) + ' ' + next(tp_lines) + constraints
        for line in tp_lines:
            yield line

class CSharpClass(c.Declarator):
    def __init__(self, tpname, public_methods, protected_methods, private_methods,
        public_attrs, protected_attrs, private_attrs, header=True, visibility='public'):
        """Initialize the structure declarator.
        *tpname* is the name of the structure, while *declname* is the
        name used for the declarator. *pad_bytes* is the number of
        padding bytes added at the end of the structure.
        *fields* is a list of :class:`Declarator` instances.
        """
        self.tpname = tpname
        self.public_methods = public_methods
        self.protected_methods = protected_methods
        self.private_methods = private_methods
        self.public_attrs = public_attrs
        self.protected_attrs = protected_attrs
        self.private_attrs = private_attrs
        self.header = header
        self.visibility = visibility

    def source(self):
        return self

    def get_decl_pair(self):
        def get_tp():
            yield f"{self.visibility} class {self.tpname}"
            yield "{"
            
            if self.public_methods:
                for f in self.public_methods:
                    for f_line in f.generate('public'):
                        yield "  " + f_line

            if self.protected_methods:
                for f in self.protected_methods:
                    for f_line in f.generate('protected'):
                        yield "  " + f_line

            if self.private_methods:
                for f in self.private_methods:
                    for f_line in f.generate('private'):
                        yield "  " + f_line

            if self.public_attrs:
                for f in self.public_attrs:
                    for f_line in f.generate():
                        yield "  public " + f_line

            if self.protected_attrs:
                for f in self.protected_attrs:
                    for f_line in f.generate():
                        yield "  protected " + f_line

            if self.private_attrs:
                for f in self.private_attrs:
                    for f_line in f.generate():
                        yield "  private " + f_line
            
            yield "} " + self.struct_attributes()
        return get_tp(), None

    def generate(self):
        return super(CSharpClass, self).generate(with_semicolon=False)

    def alignment_requirement(self):
        return max(
            max(f.alignment_requirement() for f in self.public_attrs),
            max(f.alignment_requirement() for f in self.protected_attrs),
            max(f.alignment_requirement() for f in self.private_attrs)
        )

    def struct_attributes(self):
        return ""

    mapper_method = "map_struct"