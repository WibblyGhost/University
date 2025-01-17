import re
import sys


# ToDo: 1.0.* Import scanner.py
class Scanner:
    """The interface comprises the methods lookahead and consume.
       Other methods should not be called from outside of this class."""

    def __init__(self, input_file):
        """Reads the whole input_file to input_string, which remains constant.
           current_char_index counts how many characters of input_string have
           been consumed.
           current_token holds the most recently found token and the
           corresponding part of input_string."""
        # source code of the program to be compiled
        self.input_string = input_file.read()
        # index where the unprocessed part of input_string starts
        self.current_char_index = 0
        # a pair (most recently read token, matched substring of input_string)
        self.current_token = self.get_token()

    def skip_white_space(self):
        """Consumes all characters in input_string up to the next
           non-white-space character."""
        for string in self.input_string[self.current_char_index:]:
            if string in (" ", "\n", "\t"):
                self.current_char_index += 1
            else:
                break

    def no_token(self):
        """Stop execution if the input cannot be matched to a token."""
        print('lexical error: no token found at the start of ' +
              self.input_string[self.current_char_index:])
        sys.exit()

    def get_token(self):
        """Returns the next token and the part of input_string it matched.
           The returned token is None if there is no next token.
           The characters up to the end of the token are consumed.
           Raise an exception by calling no_token() if the input contains
           extra non-white-space characters that do not match any token."""
        self.skip_white_space()
        # find the longest prefix of input_string that matches a token
        token, longest = None, ''
        for (t, r) in Token.token_regexp:
            match = re.match(r, self.input_string[self.current_char_index:])
            if match and match.end() > len(longest):
                token, longest = t, match.group()
        # consume the token by moving the index to the end of the matched part
        self.current_char_index += len(longest)
        # If there is no matching token, report an error
        if token is None and self.input_string[self.current_char_index:] != "":
            self.no_token()
        return token, longest

    def lookahead(self):
        """Returns the next token without consuming it.
           Returns None if there is no next token."""
        return self.current_token[0]

    def unexpected_token(self, found_token, expected_tokens):
        """Stop execution because an unexpected token was found.
           found_token contains just the token, not its value.
           expected_tokens is a sequence of tokens."""
        print('syntax error: token in ' + repr(sorted(expected_tokens)) +
              ' expected but ' + repr(found_token) + ' found')
        sys.exit()

    def consume(self, *expected_tokens):
        """Returns the next token and consumes it, if it is in
           expected_tokens. Calls unexpected_token(...) otherwise.
           If the token is a number or an identifier, not just the
           token but a pair of the token and its value is returned."""
        curr_token = self.current_token
        self.current_token = self.get_token()
        if curr_token[0] in expected_tokens:
            if curr_token[0] in (Token.ID, Token.NUM):
                return curr_token[0], curr_token[1]
            else:
                return curr_token[0]
        else:
            self.unexpected_token(curr_token[0], expected_tokens)


class Token:
    # The following enumerates all tokens.
    DO = 'DO'
    ELSE = 'ELSE'
    READ = 'READ'
    WRITE = 'WRITE'
    END = 'END'
    IF = 'IF'
    THEN = 'THEN'
    WHILE = 'WHILE'
    SEM = 'SEM'
    BEC = 'BEC'
    LESS = 'LESS'
    EQ = 'EQ'
    GRTR = 'GRTR'
    LEQ = 'LEQ'
    NEQ = 'NEQ'
    GEQ = 'GEQ'
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAR = 'LPAR'
    RPAR = 'RPAR'
    NUM = 'NUM'
    ID = 'ID'

    # The following list gives the regular expression to match a token.
    # The order in the list matters for mimicking Flex behaviour.
    # Longer matches are preferred over shorter ones.
    # For same-length matches, the first in the list is preferred.
    token_regexp = [
        (DO,    'do'),
        (ELSE,  'else'),
        (READ,  'read'),
        (WRITE, 'write'),
        (END,   'end'),
        (IF,    'if'),
        (THEN,  'then'),
        (WHILE, 'while'),
        (SEM,   ';'),
        (BEC,   ':='),
        (LESS,  '<'),
        (EQ,    '='),
        (NEQ,   '!='),
        (GRTR,  '>'),
        (LEQ,   '<='),
        (GEQ,   '>='),
        (ADD,   '\\+'),  # + is special in regular expressions
        (SUB,   '-'),
        (MUL,   '\\*'),
        (DIV,   '\\/'),
        (LPAR,  '\\('),  # ( is special in regular expressions
        (RPAR,  '\\)'),  # ) is special in regular expressions
        (ID,    '[a-z]+'),
        (NUM,   '[0-9]+'),
    ]


def indent(s, level):
    return '    ' * level + s + '\n'


# Each of the following classes is a kind of node in the abstract syntax tree.
# indented(level) returns a string that shows the tree levels by indentation.


class Program_AST:
    def __init__(self, program):
        self.program = program

    def __repr__(self):
        return repr(self.program)

    def indented(self, level):
        return self.program.indented(level)

    def code(self):
        program = self.program.code()
        local = symbol_table.size()
        java_scanner = symbol_table.location('Java Scanner')
        return '.class public Program\n' + \
               '.super java/lang/Object\n' + \
               '.method public <init>()V\n' + \
               'aload_0\n' + \
               'invokenonvirtual java/lang/Object/<init>()V\n' + \
               'return\n' + \
               '.end method\n' + \
               '.method public static main([Ljava/lang/String;)V\n' + \
               '.limit locals ' + str(local) + '\n' + \
               '.limit stack 1024\n' + \
               'new java/util/Scanner\n' + \
               'dup\n' + \
               'getstatic java/lang/System.in Ljava/io/InputStream;\n' + \
               'invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V\n' + \
               'astore ' + str(java_scanner) + '\n' + \
               program + \
               'return\n' + \
               '.end method\n'


class Statements_AST:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result

    def indented(self, level):
        result = indent('Statements', level)
        for st in self.statements:
            result += st.indented(level + 1)
        return result

    def code(self):
        result = ''
        for st in self.statements:
            result += st.code()
        return result


class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then

    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
               repr(self.then) + ' end'

    def indented(self, level):
        return indent('If', level) + \
               self.condition.indented(level + 1) + \
               self.then.indented(level + 1)

    def code(self):
        l1 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               l1 + ':\n'


# ToDo: 2.0.* Implement If_Else_AST Class
class If_Else_AST:
    def __init__(self, condition, then, if_else):
        self.condition = condition
        self.if_else = if_else
        self.then = then

    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
            repr(self.then) + ' else ' + repr(self.if_else) + ' end'

    def indented(self, level):
        return indent('If-Else', level) + \
            self.condition.indented(level + 1) + \
            self.then.indented(level + 1) + \
            self.if_else.indented(level + 1)

    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'


class While_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ' + repr(self.condition) + ' do ' + \
               repr(self.body) + ' end'

    def indented(self, level):
        return indent('While', level) + \
               self.condition.indented(level + 1) + \
               self.body.indented(level + 1)

    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'


class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return repr(self.identifier) + ':=' + repr(self.expression)

    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level + 1) + \
               self.expression.indented(level + 1)

    def code(self):
        loc = symbol_table.location(self.identifier.identifier)
        return self.expression.code() + \
               'istore ' + str(loc) + '\n'


class Write_AST:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return 'write ' + repr(self.expression)

    def indented(self, level):
        return indent('Write', level) + self.expression.indented(level + 1)

    def code(self):
        return 'getstatic java/lang/System/out Ljava/io/PrintStream;\n' + \
               self.expression.code() + \
               'invokestatic java/lang/String/valueOf(I)Ljava/lang/String;\n' + \
               'invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n'


class Read_AST:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return 'read ' + repr(self.identifier)

    def indented(self, level):
        return indent('Read', level) + self.identifier.indented(level + 1

    def code(self):
        java_scanner = symbol_table.location('Java Scanner')
        loc = symbol_table.location(self.identifier.identifier)
        return 'aload ' + str(java_scanner) + '\n' + \
               'invokevirtual java/util/Scanner.nextInt()I\n' + \
               'istore ' + str(loc) + '\n'


class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)

    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level + 1) + \
               self.right.indented(level + 1)


class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'

    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level + 1) + \
               self.right.indented(level + 1)


class Number_AST:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return self.number

    def indented(self, level):
        return indent(self.number, level)


class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return self.identifier

    def indented(self, level):
        return indent(self.identifier, level)


# The following methods comprise the recursive-descent parser.

def program():
    sts = statements()
    return Program_AST(sts)


def statements():
    result = [statement()]
    while scanner.lookahead() == Token.SEM:
        scanner.consume(Token.SEM)
        st = statement()
        result.append(st)
    return Statements_AST(result)


# ToDo: 4.2.* Modify statement to include write
# ToDo: 5.2.* Modify statement to include read
def statement():
    if scanner.lookahead() == Token.IF:
        return if_statement()
    elif scanner.lookahead() == Token.WHILE:
        return while_statement()
    elif scanner.lookahead() == Token.ID:
        return assignment()
    elif scanner.lookahead() == Token.WRITE:
        return write()
    elif scanner.lookahead() == Token.READ:
        return read()
    else:  # error
        return scanner.consume(Token.IF, Token.WHILE, Token.ID, Token.WRITE, Token.READ)


# ToDo: 3.0.* Extend if_statement
def if_statement():
    scanner.consume(Token.IF)
    condition = comparison()
    scanner.consume(Token.THEN)
    then = statements()
    if scanner.lookahead() == Token.ELSE:
        scanner.consume(Token.ELSE)
        if_else = statements()
        scanner.consume(Token.END)
        return If_Else_AST(condition, then, if_else)
    else:
        scanner.consume(Token.END)
        return If_AST(condition, then)


def while_statement():
    scanner.consume(Token.WHILE)
    condition = comparison()
    scanner.consume(Token.DO)
    body = statements()
    scanner.consume(Token.END)
    return While_AST(condition, body)


def assignment():
    ident = identifier()
    scanner.consume(Token.BEC)
    expr = expression()
    return Assign_AST(ident, expr)


operator = {Token.LESS: '<', Token.EQ: '=', Token.GRTR: '>',
            Token.LEQ: '<=', Token.NEQ: '!=', Token.GEQ: '>=',
            Token.ADD: '+', Token.SUB: '-', Token.MUL: '*', Token.DIV: '/'}


def comparison():
    left = expression()
    op = scanner.consume(Token.LESS, Token.EQ, Token.GRTR,
                         Token.LEQ, Token.NEQ, Token.GEQ)
    right = expression()
    return Comparison_AST(left, operator[op], right)


def expression():
    result = term()
    while scanner.lookahead() in [Token.ADD, Token.SUB]:
        op = scanner.consume(Token.ADD, Token.SUB)
        tree = term()
        result = Expression_AST(result, operator[op], tree)
    return result


def term():
    result = factor()
    while scanner.lookahead() in [Token.MUL, Token.DIV]:
        op = scanner.consume(Token.MUL, Token.DIV)
        tree = factor()
        result = Expression_AST(result, operator[op], tree)
    return result


def factor():
    if scanner.lookahead() == Token.LPAR:
        scanner.consume(Token.LPAR)
        result = expression()
        scanner.consume(Token.RPAR)
        return result
    elif scanner.lookahead() == Token.NUM:
        value = scanner.consume(Token.NUM)[1]
        return Number_AST(value)
    elif scanner.lookahead() == Token.ID:
        return identifier()
    else:  # error
        return scanner.consume(Token.LPAR, Token.NUM, Token.ID)


def identifier():
    value = scanner.consume(Token.ID)[1]
    return Identifier_AST(value)


# ToDo: 4.1.* Implement write statement
def write():
    scanner.consume(Token.WRITE)
    return Write_AST(expression())


# ToDo: 5.1.* Implement read statement
def read():
    scanner.consume(Token.READ)
    return Read_AST(identifier())


# Initialise scanner.

scanner = Scanner(sys.stdin)

# Uncomment the following to test the scanner without the parser.
# Show all tokens in the input.
#
# token = scanner.lookahead()
# while token != None:
#     if token in [Token.NUM, Token.ID]:
#         token, value = scanner.consume(token)
#         print(token, value)
#     else:
#         print(scanner.consume(token))
#     token = scanner.lookahead()
# sys.exit()

# Call the parser.

ast = program()
if scanner.lookahead() != None:
    print('syntax error: end of input expected but token ' +
          repr(scanner.lookahead()) + ' found')
    sys.exit()

# Show the syntax tree with levels indicated by indentation.

print(ast.indented(0), end='')
