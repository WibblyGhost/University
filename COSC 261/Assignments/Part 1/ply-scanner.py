import ply.lex as lex
import sys


# ToDo: 1.1.* Extend reserved words
# reserved words
reserved = {
    'do': 'DO',
    'else': 'ELSE',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'while': 'WHILE',
    'read': 'READ',
    'write': 'WRITE'
}


# all token types
tokens = [
    'SEM', 'BEC', 'LESS', 'EQ', 'GRTR', 'LEQ', 'NEQ', 'GEQ',
    'ADD', 'SUB', 'MUL', 'DIV', 'LPAR', 'RPAR', 'NUM', 'ID'
] + list(reserved.values())


# rules specifying regular expressions and actions
t_SEM = r';'
t_BEC = r':='
t_LESS = r'<'
t_EQ = r'='
t_GRTR = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_ADD = r'\+'
t_SUB = r'-'
t_LPAR = r'\('
t_RPAR = r'\)'
# ToDo: 1.2.* Extend regular expressions
t_NEQ = r'!='
t_MUL = r'\*'
t_DIV = r'\/'
t_NUM = r'[0-9]+'


def t_ID(t):
    # ToDo: 2.* Modify regular expressions to catch reserved words
    r'[a-z]+'
    # Checks t against all reserved items, if t is found return reserved word
    if t.value in reserved:
        r'{0}'.format(t.value)
        t.type = reserved[t.value]
        t.value = reserved[t.value]
        return t
    return t


# rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# rule to ignore whitespace
t_ignore = ' \t'


# error handling rule
def t_error(t):
    print("lexical error: illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)


# Show all tokens in the input.
scanner = lex.lex()
scanner.input(sys.stdin.read())

for token in scanner:
    if token.type in ['NUM', 'ID']:
        print(token.type, token.value)
    else:
        print(token.type)
