import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(r"""
?start : assign* expr ";"?

assign : NAME "=" expr ";"

?expr  : expr "+" term  -> add
       | expr "-" term  -> sub
       | term
 
?term  : term "*" pow  -> mul
       | term "/" pow  -> div
       | pow

?pow   : atom "^" pow  -> exp
       | atom

?atom  : NUMBER            -> number
       | NAME "(" expr ")" -> fcall
       | NAME              -> var
       | "(" expr ")"

NUMBER : /-?\d+(\.\d+([Ee][+-]?\d+)?)?/
NAME   : /[a-zA-Z_]+[\w_]*/
%ignore /\s+/
""")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp
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

    def fcall(self, name, x):
        name = str(name)
        fn = getattr(math, name)
        return fn(x)

    def assign(self, name, value):
        self.env[name] = value

    def var(self, name):
        return self.env[name]

    def start(self, *args):
        return args[-1]


transformer = CalcTransformer()


"""exprs = [
    "42",
    "3.14",
    "-10",
    "40 + 2",
    "21 * 2",
    "80 - 38",
    "84 / 2",
    "1 + 1 + 1",
    "1 + 1 - 1",
    "2 * 2 * 2 / 8",
    "20 * 2 + 2",
    "2 + 20 * 2",
    "32 / 4 / 2",
    "10 - 2 - 3",
    "(2 + 20) * 2",
    "(2 + (10 + 10) / 4) * 2",
    "3**2",
    "2 * 3**2",
    "3**2**3",
    "1 ^ 2 + 3", # => 0b01 ^ 0b10 = 0b11 = 6
    "3 + 2 ^ 1", # => 6
    "1 | 2 & 3", # => 0b01 | (0b10 & 0b11) = 0b11 = 3
    "1 ^ 2 & 3", # => 0b01 ^ (0b10 & 0b11) = 0b11 = 3
    "x = 20 + 20; y = 2; x + y",
]


for src in exprs:
    print(src)
    
    tree = grammar.parse(src)
    print(tree.pretty())
    
    result = transformer.transform(tree)
    print(result)
    
    print('-' * 40)"""