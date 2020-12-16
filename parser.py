import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
    start : assign* expr?

    ?assign: NAME "=" expr -> assign

    ?expr : expr "+" term -> add
        |   expr "-" term -> sub
        |   comp
        |   term
    
    ?comp : expr "==" term -> eq
        |   expr "!=" term -> ne
        |   expr ">" term -> gt
        |   expr ">=" term -> ge
        |   expr "<" term -> lt
        |   expr "<=" term -> le

    ?term : term "*" pow -> mul
        |   term "/" pow -> div
        |   pow

    ?pow  : atom "^" pow -> exp
        |   atom

    ?atom: NUMBER -> number
        | NAME "(" expr ")" -> fcall
        | NAME -> var
        | "(" expr ")"

    NUMBER: /-?\d+(\.\d+(e[+-]?\d+)?)?/
    NAME: /[\w_]+/

    %ignore /\s+/
    """,
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import (
        add, sub, mul, truediv as div, pow as exp,
        eq, ne, gt, ge, lt, le
    )  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}

    def list_(self, *args):
        return list(args)

    def number(self, tk):
        print('entrou no number')
        try:
            return int(tk)
        except ValueError:
            return float(tk)

    def assign(self, name, value):
        self.env[name] = value
        return value

    def var(self, tk):
        if tk in self.variables:
            return self.variables[tk]
        else:
            self.env[tk]

    def fcall(self, name, x):
        name = str(name)
        fn = getattr(math, name)
        return fn(x)

    def start(self, *args):
        return args[-1]
