import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(r"""
    ?start  : assign* comp?

    ?assign : NAME "=" comp

    ?comp   : expr "==" expr   -> eq
            | expr "!=" expr   -> ne
            | expr ">"  expr   -> gt
            | expr "<"  expr   -> lt
            | expr ">=" expr   -> ge
            | expr "<=" expr   -> le 
            | expr

    ?expr   : expr "+" term    -> add
            | expr "-" term    -> sub
            | term

    ?term   : term "*" pow     -> mul
            | term "/" pow     -> div
            | pow

    ?pow    : atom "^" pow      -> exp
            | atom

    ?atom   : NUMBER                           -> number
            | NAME "(" expr ( "," expr)* ")"   -> func
            | NAME                             -> var
            | "(" expr ")"

    NUMBER: /-?\d+(\.\d+)?([eE][+-]?\d+)?/
    NAME: /-?([a-z]|[A-Z]\_?)\w*/

    %ignore /\s+/
    %ignore /\#.*/

""",
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp, eq, ne, gt, lt, ge, le  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, token):
        try:
            return int(token)
        except: 
            return float(token)

    def var(self, name):
        if name in self.variables:
            return self.variables[name]
        elif name[0] == "-" and name[1:] in self.variables:
            return -self.variables[name[1:]]

    def func(self, name, *args):
        name = str(name)
        if name[0] == "-":
            fn = self.variables[name[1:]]
            return -fn(*args)
        else:
            fn = self.variables[name]
            return fn(*args)

    def assign(self, name, value):
        self.variables[name] = value
        return self.variables[name]

    def start(self, *args):
        return args[-1]

