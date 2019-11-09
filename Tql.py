from sly import Lexer
from sly import  Parser
import ast
from collections import  deque
# ThreaQueryLanguage(TQL)
class TqlLexer(Lexer):
    tokens = {
              FLOAT,
              STRING,
              LBRACK,
              RBRACK,
              COMMA,
              OR,
              AND,
              GT,
              LT,
              GTE,
              LTE,
              EQ,
              NTEQ,
              ADD,
              DIV,
              MUL,
              MOD,
              SUB,
              LPAREN,
              RPAREN,
              CONTAINS,
              NOT,
              VARIABLE,
              }
    # reserved keyword tokens
    VARIABLE["and"] = AND
    VARIABLE["or"] = OR
    VARIABLE["AND"] = AND
    VARIABLE["OR"] = OR
    VARIABLE["IN"] = CONTAINS
    VARIABLE["in"] = CONTAINS
    VARIABLE["NOT"] = NOT
    VARIABLE["not"] = NOT

    ignore = ' \t'

    ADD = r'\+'
    SUB = r'\-'
    DIV = r'/'
    MUL = r'\*'
    MOD = r'\%'
    EQ = r'='
    NTEQ = r'!='
    GT = r'>'
    LT = r'<'
    GTE = r'>='
    LTE = r'<='
    FLOAT = r'[+-]?(\d+([.]\d*)?(e[+-]?\d+)?|[.]\d+(e[+-]?\d+)?)'
    LBRACK = r'\['
    RBRACK = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r'\,'
    CONTAINS = r'in|IN'
    NOT = r'not|NOT'
    VARIABLE = r'\$?[a-zA-Z_][a-zA-Z0-9_]*'
    OR = r'OR|or'
    AND = r'and|AND'



    @_(r's?(?P<quote>["\'])([^\\\n]|(\\.))*?(?P=quote)')
    def STRING(self,t):
        if t.value == 's':
            t.value = t.value[1:]
        return t

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

class TqlParser(Parser):

    tokens = TqlLexer.tokens

    precedence = (
        ('left', OR, AND),
        ('right', NOT),
        ('nonassoc', EQ, NTEQ, GTE, GT, LTE, LT, CONTAINS),
        ('left', ADD, SUB),
        ('left', MUL, DIV,MOD),
    )

    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIV expr',
       'expr MOD expr')
    def expr(self,p):
        if p[1] == "+":
            return p[0] + p[2]
        elif p[1] == "-":
            return p[0] - p[2]
        elif p[2] == "*":
            return p[0] * p[2]
        elif p[2] == '/':
            return p[0]/p[2]
        else:
            return p[0] % p[2]

    @_('FLOAT')
    def expr(self,p):
        print(float(p.FLOAT))
        return float(p.FLOAT)

    @_('STRING')
    def expr(self,p):
        return p.STRING

    @_('VARIABLE')
    def expr(self,p):
        return p.VARIABLE

    @_('expr AND expr',
       'expr OR expr')
    def expr(self,p):
        if p[1]=='and' or p[1]=='AND':
            return p[0] and p[2]
        else:
            return p[0] or p[2]

    @_('expr GT expr',
       'expr GTE expr',
       'expr LT expr',
       'expr LTE expr')
    def expr(self,p):
        if p[1]=='<':
            return p[0] < p[2]
        elif p[1]=='>':
            return p[0] > p[2]
        elif p[1]=='<=':
            return p[0] <= p[2]
        else:
            return p[0] >= p[2]

    @_('expr CONTAINS expr',
       'expr NOT CONTAINS expr')
    def expr(self,p):
        pythn_lst = p.expr1
        if p[1]=="in" or p[1]=="IN":

            if p.expr0 in pythn_lst:
                return True
        else:
            if p.expr0 not in pythn_lst:
                return True

        return False

    @_('LBRACK RBRACK',
       'LBRACK items RBRACK',
       'LBRACK items COMMA RBRACK')
    def expr(self,p):
        if len(p)<4:
            return p[1]

    @_('expr',
       'items COMMA expr')
    def items(self,p):

        if len(p) == 1:
            element_list = deque()
            element_list.append(p.expr)
        else:
            element_list = p.items
            element_list.append(p.expr)
        return element_list

    @_('LPAREN expr RPAREN')
    def expr(self,p):
        return p.expr
    @_('expr EQ expr',
       'expr NTEQ expr')
    def expr(self,p):

        if p[1] == "=" and p.expr0 == p.expr1:
            return True
        else:
            if p[1] == "!=" and p.expr0 != p.expr1:
                return True
        return False






import time

if __name__=='__main__':
    data =  '''(1 = 0.1e-3 or 1 not in [1,3])'''
    lexer = TqlLexer()
    for t in lexer.tokenize(data):
        print(t)
    parser = TqlParser()
    ans = parser.parse(lexer.tokenize(data))
    print(ans)


