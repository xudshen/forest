__author__ = 'xudshen@hotmail.com'

from forest.logger import log_d

tokens = (
    'NAME', 'NUMBER', 'STRING', 'STRING_PATH',
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
    'SQUOTE', 'COMMA'
)

# Tokens

t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_SQUOTE = r'\''
t_NAME = r'[a-zA-Z][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        log_d("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_STRING_PATH(t):
    r'\{[\s\S]+\}'
    try:
        t.value = str(t.value)
        t.value = t.value[1:-1]
    except ValueError:
        log_d("Can not parser string", t.value)
        t.value = ""
    return t


def t_STRING(t):
    r'\'[\s\S]+\''
    try:
        t.value = str(t.value)
        t.value = t.value[1:-1]
    except ValueError:
        log_d("Can not parser string", t.value)
        t.value = ""
    return t

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    log_d("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

lexer = lex.lex()


def p_path(t):
    '''PATH : STRING_PATH
            | FUNCTION_CHAIN
            | PATH FUNCTION_CHAIN'''
    if len(t) == 2:
        t[0] = {"path": t[1]} if type(t[1]) is str else {"chain": t[1]}
    else:
        t[0] = t[1]
        if "chain" not in t[0]:
            t[0]["chain"] = []
        t[0]["chain"] += t[2]


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
    t[0] = [t[2]]
    if len(t) > 4:
        t[0] += t[4]


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
    log_d("Syntax error at '%s'" % (t.value if t is not None else "unknown"))


import ply.yacc as yacc

parser = yacc.yacc()


def resolve_xpath(path):
    log_d("resolve xpath", path)
    ast = parser.parse(path)
    if ast is None:
        log_d("resolve xpath failed: " + path)
        return None, None
    return ast["path"] if "path" in ast else None, ast["chain"] if "chain" in ast else None


if __name__ == '__main__':
    while 1:
        try:
            s = input('> ')  # Use raw_input on Python 2
        except EOFError:
            break
        lexer.input(s)
        # while True:
        #     tok = lexer.token()
        #     if not tok:
        #         break
        #     log_d(tok)

        log_d(parser.parse(s, lexer=lexer))