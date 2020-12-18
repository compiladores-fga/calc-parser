import math
from lark import Lark, InlineTransformer


# Implemente a gramática aqui! Você pode testar manualmente seu código
# executando o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
    start : assign* comp?

    ?assign: NAME "=" comp -> assign

    ?comp : expr "==" expr -> eq
        |   expr "!=" expr -> ne
        |   expr ">" expr -> gt
        |   expr "<" expr -> lt
        |   expr ">=" expr -> ge
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
        |   NAME "(" expr ("," expr)* ")" -> fcall
        |   NAME -> var
        |   "(" expr ")"

    NUMBER: /-?\d+(\.\d+)?(e[+-]?\d+)?/
    NAME: /[-+]?\w+/

    %ignore /\#.*/
    %ignore /\s+/
    """,
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import (
        add, sub, mul, truediv as div, eq, ne, gt, lt, ge, le, pow as exp
    )

    def __init__(self):
        super().__init__()
        self.variables = {
            k: v for k, v in vars(math).items() if not k.startswith("_")
        }
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
            return -self.variables[name[1:]](*args)
        return self.variables[name](*args)

    def var(self, token):
        if token[0] == "-" and token[1:] in self.variables:
            return -self.variables[token[1:]]
        if token in self.variables:
            return self.variables[token]
        return self.env[token]

    def assign(self, name, value):
        self.env[name] = value
        return value

    def start(self, *args):
        return args[-1]
