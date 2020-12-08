import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
start  : expr
       | comp

?comp  : comp ">" expr  -> gt
       | comp ">=" expr -> ge
       | comp "<" expr  -> lt
       | comp "<=" expr -> le
       | comp "!=" expr -> ne
       | comp "==" expr -> eq
       | expr

?expr  : expr "+" term  -> add
       | expr "-" term  -> sub
       | term

?term  : term "*" pow   -> mul
       | term "/" pow   -> div
       | pow

?pow   : atom "^" pow   -> exp
       | atom

?atom  : NUMBER         -> number
       | NAME           -> var
       | "(" expr ")"

NAME   : /[-+]?\w+/
NUMBER : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
%ignore /\s+/
%ignore /\#.*/
""")

exprs = [
    "40 > 2"
]

for src in exprs:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print('-' * 40)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp, gt, ge, lt, le, ne, eq

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, token):
        try:
            return int(token)
        except:
            return float(token)
    
    def start(self, *args):
        return args[-1]