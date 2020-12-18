import re
import math
from lark import Lark, InlineTransformer, Token


grammar = Lark(r"""
?start : assign* compare ?

?assign : NAME "=" compare

?compare    : expr ">" expr -> gt
            | expr "<" expr -> lt
            | expr ">=" expr -> ge
            | expr "<=" expr -> le
            | expr "==" expr -> eq
            | expr "!=" expr -> ne
            | expr

?expr  : expr "+" term  -> add
       | expr "-" term  -> sub
       | term
 
?term  : term "*" pow  -> mul
       | term "/" pow  -> div
       | pow

?pow   : atom "^" pow  -> exp
       | atom

?atom  : NUMBER            -> number
       | NAME "(" expr ("," expr)+ ")" -> fcall
       | NAME "(" expr ")" -> fcall
       | NAME              -> var
       | "(" expr ")"

NUMBER : /-?\d+(\.\d+([Ee][+-]?\d+)?)?/
NAME   : /[+-]?[a-zA-Z_]+[\w_]*/
%ignore /\s+/
%ignore /\#.*/
""")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp, gt, lt, ge, le, eq, ne
    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}
    
    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)

    def fcall(self, name, *args):
        name = str(name)
        if name[0] == "-":
            fn = self.variables[name[1:]]
            return -fn(*args)
        
        fn = self.variables[name]
        return fn(*args)

    def assign(self, name, value):
        self.env[name] = value
        return value 

    def var(self, name):
        if name[0] == "-" and name[1:] in self.variables:
            return -self.variables[name [1:]]
        elif name in self.variables:
            return self.variables[name]
        else:
            return self.env[name]

    def start(self, *args):
        return args[-1]