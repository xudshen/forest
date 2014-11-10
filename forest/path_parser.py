__author__ = 'xudshen@hotmail.com'

tokens = (
    'NAME', 'NUMBER', 'STRING',
    'LPAREN', 'RPAREN', 'LSQUAR', 'RSQUAR',
    'COMMA'
)

# Tokens

t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUAR = r'\['
t_RSQUAR = r'\]'
t_NAME = r'[a-zA-Z][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_STRING(t):
    r'\'[\s\S]+\''
    try:
        t.value = str(t.value)
        t.value = t.value[1:-1]
    except ValueError:
        print("Can not parser string", t.value)
        t.value = ""
    return t

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lexer = lex.lex()
# while 1:
# try:
# s = input('calc > ')  # Use raw_input on Python 2
# except EOFError:
# break
# lexer.input(s)
# while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         print(tok)

# Parsing rules

# precedence = ((),)

# dictionary of names
names = {}

def p_function_chain(t):
    '''FUNCTION_CHAIN : FUNCTION
                      | FUNCTION_CHAIN FUNCTION'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]

def p_function(t):
    '''FUNCTION : LPAREN NAME RPAREN
                | LPAREN NAME COMMA ARGUMENT_LIST RPAREN'''
    t[0] = {"func": t[2]}
    if len(t) > 4:
        t[0]["argu"] = t[4]


def p_argument_list(t):
    '''ARGUMENT_LIST : ARGUMENT
                     | ARGUMENT_LIST COMMA ARGUMENT'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]


def p_argument(t):
    '''ARGUMENT : STRING
                | NUMBER'''
    t[0] = t[1]


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()

while 1:
    try:
        s = input('calc > ')  # Use raw_input on Python 2
    except EOFError:
        break
    # lexer.input(s)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)

    print(parser.parse(s))