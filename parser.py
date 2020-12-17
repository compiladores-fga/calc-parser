import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
?start  : assign* comp? 
?assign : NAME "=" comp
?comp   : expr "==" expr                    -> eq
        | expr "!=" expr                    -> ne
        | expr "<" expr                     -> lt
        | expr ">" expr                     -> gt
        | expr "<=" expr                    -> le
        | expr ">=" expr                    -> ge
        | expr
?expr   : expr "+" term                     -> add
        | expr "-" term                     -> sub
        | term
?term   : term "*" pow                      -> mul
        | term "/" pow                      -> div
        | pow
?pow    : atom "^" pow                      -> exp
        | atom
?atom   : NUMBER                            -> number
        | NAME "(" expr ("," expr)* ")"     -> function
        | NAME                              -> var
        | "(" expr ")"

NUMBER  : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
NAME    : /[-+]?\w+/

%ignore /\s+/
%ignore /\#.*/
"""
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp, eq, ne, lt, gt, le, ge

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}

    def start(self, *args):
        return args[-1]

    def assign(self, name, value):
        self.env[name] = value
        return self.env[name]
    
    def number(self, num):
        try:
            return int(num)
        except:
            return float(num)
    
    def function(self, name, *args):
        name = str(name)
        fn = self.variables[name.split('-')[-1]]
        if name[0] == '-':
            return -fn(*args)
        else:
            return fn(*args)

    def var(self, name):
        if name in self.variables:
            return self.variables[name]
        elif name[0] == "-" and name[1:] in self.variables:
            return -self.variables[name[1:]]
        else:
            return self.env[name]
