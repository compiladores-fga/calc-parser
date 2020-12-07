import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(r"""
    ?start  : assign* comp?

    ?assign : NAME "=" comp 

    ?comp   : expr "==" expr    -> eq
            | expr "!=" expr    -> ne
            | expr ">" expr     -> gt
            | expr ">=" expr    -> ge
            | expr "<" expr     -> lt
            | expr "<=" expr    -> le
            | expr
    
    ?expr   : expr "+" term     -> add
            | expr "-" term     -> sub
            | term
 
    ?term   : term "*" exp      -> mul
            | term "/" exp      -> div
            | exp

    ?exp    : atom "^" exp      -> pow
            | atom

    ?atom   : NUMBER            -> number
            | NAME "(" expr ("," expr)* ")" -> fcall
            | NAME              -> var
            | "(" expr ")"

    NUMBER  : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
    NAME    : /-?([a-z]|[A-Z]|\_)\w*/
    
    %ignore /\s+/
    %ignore /\#[^\n]*/

    """,
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, eq, ne, gt, ge, lt, le  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

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
        else:
            fn = self.variables[name]
            return fn(*args)
        
    def assign(self, name, value):
        self.variables[name] = value
        return self.variables[name]

    def var(self, name):
        if name in self.variables:
            return self.variables[name]
        elif name[0] == "-" and name[1:] in self.variables:
            return -self.variables[name[1:]]
      
    def start(self, *args):
        return args[-1]