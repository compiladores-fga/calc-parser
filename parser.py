import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
        ?start: sum
            | NAME "=" sum    -> assign_var
        ?sum: product
            | sum "+" product   -> add
            | sum "-" product   -> sub
        ?product: atom
            | product "*" atom  -> mul
            | product "/" atom  -> div
        ?atom: NUMBER           -> number
            | "-" atom         -> neg
            | NAME             -> var
            | "(" sum ")"
        
        NUMBER  : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
        NAME: /-?([a-z]|[A-Z]|\_)\w*/
    """,
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
