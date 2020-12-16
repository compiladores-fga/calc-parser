import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
    start : assign* comp?

    ?assign: NAME "=" comp -> assign

    ?comp : expr "==" expr -> eq
        |   expr "!=" expr -> ne
        |   expr ">" expr -> gt
        |   expr ">=" expr -> ge
        |   expr "<" expr -> lt
        |   expr "<=" expr -> le
        |   expr

    ?expr : expr "+" term -> add
        |   expr "-" term -> sub
        |   term

    ?term : term "*" pow -> mul
        |   term "/" pow -> div
        |   pow

    ?pow  : atom "^" pow -> exp
        |   atom

    ?atom : NUMBER -> number
        |   NAME "(" expr ")" -> fcall
        |   NAME "(" expr ("," expr)+ ")" -> fcall
        |   NAME -> var
        |   "(" expr ")"

    NUMBER: /-?\d+(\.\d+(e[+-]?\d+)?)?/
    NAME: /[-+]?[\w_]+/

    %ignore /\#[^\n]*/
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
        try:
            return int(tk)
        except ValueError:
            return float(tk)

    def assign(self, name, value):
        self.env[name] = value
        return value

    def var(self, tk):
        odd_op = 1
        if tk[0] == '-':
            odd_op = -1
            tk = tk[1:]
        elif tk[0] == '+':
            tk = tk[1:]

        if tk in self.variables:
            if odd_op == -1:
                return -self.variables[tk]

            return self.variables[tk]
        else:
            return self.env[tk]

    def fcall(self, name, *args):
        name = str(name)
        odd_op = 1
        if name.startswith('-'):
            odd_op = -1
            fn = self.variables[name[1:]]
        else:
            fn = self.variables[name]
        return fn(*args) * odd_op

    def start(self, *args):
        return args[-1]
