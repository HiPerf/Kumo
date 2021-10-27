from rply import ParserGenerator
from .boxes import *


pg = ParserGenerator([
    "EQUALS",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "LPAREN",
    "RPAREN",
    "LACUTE",
    "RACUTE",
    "OR",
    "NUMBER",
    "MESSAGE",
    "QUEUE",
    "C2S",
    "S2C", 
    "BI",
    "IF",
    "ELSE",
    "IDENTIFIER",
    "SEMICOLON",
    "COLON",
    "COMMA",
    "DOT"
])

@pg.production("main : main message")
def main_message(p):
    return MainBox(p[0], p[1])

@pg.production("main : main program")
def main_program(p):
    return MainBox(p[0], p[1])

@pg.production("main : main queue")
def main_queue(p):
    return MainBox(p[0], p[1])

@pg.production("main : ")
def main_empty(p):
    return MainBox()

@pg.production("message : MESSAGE identifier base LBRACE fields RBRACE")
def message(p):     
    return MessageBox(p[1], p[4], p[2])

@pg.production("base : COLON identifier")
def message_base(p):
    return MessageBaseBox(p[1], None)

@pg.production("base : COLON identifier LACUTE identifier RACUTE")
def message_compound_base(p):
    return MessageBaseBox(p[1], p[3])

@pg.production("base : ")
def message_empty_base(p):
    return MessageBaseBox(None, None)

@pg.production("program : identifier direction identifier LPAREN argument RPAREN condition SEMICOLON")
def program(p):
    return ProgramBox(p[0], p[1], p[2], p[4], p[6])

@pg.production("argument : identifier OR argument")
def argument(p):
    return ArgumentBox(p[0], p[2])

@pg.production("argument : identifier")
def argument_single(p):
    return ArgumentBox(p[0])

@pg.production("condition : IF identifier EQUALS complex false_case")
def condition(p):
    return ConditionBox(p[1], p[3], p[4])

@pg.production("condition : ")
def condition_none(p):
    return ConditionBox()

@pg.production("false_case : ELSE identifier")
def false_case(p):
    return FalseCaseBox(p[1])

@pg.production("false_case : ")
def false_case_none(p):
    return FalseCaseBox()

@pg.production("fields : fields declaration")
def expr_fields(p):
    return FieldsBox(p[0], p[1])

@pg.production("fields : ")
def expr_empty_fields(p):
    return FieldsBox()

@pg.production("declaration : options type identifier SEMICOLON")
def declaration(p):
    return DeclarationBox(p[0], p[1], p[2])

@pg.production("queue : options QUEUE identifier COLON queue_subtype LBRACE LACUTE queue_specifier RACUTE RBRACE")
def queue(p):
    return QueueBox(p[0], p[2], p[4], p[7])

@pg.production("queue_subtype : identifier")
def queue_subtype_simple(p):
    return QueueSubtype(p[0])

@pg.production("queue_subtype : identifier LPAREN number RPAREN")
def queue_subtype_with_arg(p):
    return QueueSubtype(p[0], p[2])

@pg.production("queue_specifier : identifier")
def queue_specifier_specialized(p):
    return QueueSpecifierBox(QueueSpecifierType.SPECIALIZED, p[0])

@pg.production("queue_specifier : identifier COMMA identifier COMMA identifier")
def queue_specifier_templated(p):
    return QueueSpecifierBox(QueueSpecifierType.TEMPLATED, (p[0], p[2], p[4]))

@pg.production("queue_specifier : number")
def queue_specifier_array(p):
    return QueueSpecifierBox(QueueSpecifierType.ARRAY, p[0])

@pg.production("queue_specifier : ")
def queue_specifier_standard(p):
    return QueueSpecifierBox(QueueSpecifierType.STANDARD, None)

@pg.production("options : options option")
def options(p):
    return OptionsBox(p[0], p[1])

@pg.production("options : ")
def options_empty(p):
    return OptionsBox()

@pg.production("option : LBRACKET identifier RBRACKET")
def option(p):
    return p[1]

@pg.production("complex : identifier complex_postfix ")
def complex(p):
    return IdentifierBox(p[0].eval() + p[1].eval())

@pg.production("complex : number ")
def complex(p):
    return IdentifierBox(p[0].eval())

@pg.production("complex_postfix : DOT identifier complex_postfix ")
def complex_postfix_iden(p):
    return IdentifierBox('.' + p[1].eval() + p[2].eval())

@pg.production("complex_postfix : COLON COLON identifier complex_postfix ")
def complex_postfix_colon(p):
    return IdentifierBox('::' + p[2].eval() + p[3].eval())

@pg.production("complex_postfix :  ")
def complex_postfix_empty(p):
    return IdentifierBox('')

@pg.production("type : identifier")
def dtype(p): 
    return TypeBox(p[0])
    
@pg.production("type : identifier LACUTE identifier RACUTE")
def dtype_spec(p): 
    return TypeBox(p[0], p[2])

@pg.production("number : NUMBER")
def number(p):
    return IntBox(p[0])

@pg.production("direction : C2S")
def identifier(p):
    return DirectionBox(p[0])

@pg.production("direction : S2C")
def identifier(p):
    return DirectionBox(p[0])

@pg.production("direction : BI")
def identifier(p):
    return DirectionBox(p[0])

@pg.production("identifier : IDENTIFIER")
def identifier(p):
    return IdentifierBox(p[0])
