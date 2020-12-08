import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
start  : atom

?atom  : NAME -> var
       | NUMBER -> number

NAME   : /[-+]?\w+/
NUMBER : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
%ignore /\s+/
%ignore /\#.*/
""")

exprs = [
    "pi",
    "x",
    "x0",
    "variavel_como_nome_longo"
]

for src in exprs:
    tree = grammar.parse(src)
    print(src)
    print(tree.pretty())
    print('-' * 40)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
