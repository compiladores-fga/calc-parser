import math
from lark import Lark, InlineTransformer


# creating lark grammar for lexical analysis

grammar = Lark(
    r"""
?start  : assign* comp?
?assign: NAME "=" comp
?comp  : expr ">" expr  -> gt
       | expr ">=" expr -> ge
       | expr "<" expr  -> lt
       | expr "<=" expr -> le
       | expr "!=" expr -> ne
       | expr "==" expr -> eq
       | expr
?expr  : expr "+" term  -> add
       | expr "-" term  -> sub
       | term
?term  : term "*" pow   -> mul
       | term "/" pow   -> div
       | pow
?pow   : atom "^" pow   -> pow
       | atom
?atom  : NUMBER                        -> number
       | NAME "(" expr ")"             -> function_call
       | NAME "(" expr ("," expr)* ")" -> function_call
       | NAME                          -> var
       | "(" expr ")"
NAME   : /[-+]?\w+/
NUMBER : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
%ignore /\s+/
%ignore /\#.*/
""", parser='lalr')


class CalcTransformer(InlineTransformer):
    '''
    InlineTransformer for syntactic analysis
    and converting everything to valid python operations
    '''

    from operator import add, sub, mul, truediv as div, pow, gt, ge, lt, ne, eq, le

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(
            math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}

    def start(self, *args):
        return args[-1]

    def number(self, token):
        '''
        Tries to convert number to integer
        if conversion fails, then it's a float
        '''

        try:
            return int(token)
        except BaseException:
            return float(token)

    def function_call(self, name, *args):
        '''
        Converting function calls to
        python functions
        '''

        name = str(name)
        fn = self.variables[name.split('-')[-1]]
        if name[0] == '-':
            return -fn(*args)
        return fn(*args)

    def assign(self, name, value):
        '''
        Assinging user defined variables
        '''

        self.env[name] = value
        return self.env[name]

    def var(self, token):
        '''
        Recovering the value for defined
        variables
        '''

        if token in self.variables:
            return self.variables[token]
        elif token[0] == "-" and token[1:] in self.variables:
            return -self.variables[token[1:]]
        else:
            return self.env[token]
