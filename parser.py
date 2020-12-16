import re
import math
from lark import Lark, InlineTransformer, Token


"""
Implemente a gramática aqui! Você pode testar
manualmente seu código executando o arquivo
calc.py e testá-lo utilizando o pytest.
"""
grammar = Lark(r"""
    ?start : assign* comp?

    assign : NAME "=" comp

    ?comp  : comp "==" expr -> equal
        | comp "!=" expr -> not_equal
        | comp "<=" expr -> smaller_equal
        | comp "<" expr -> smaller
        | comp ">=" expr -> greather_equal
        | comp ">" expr -> greather
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
        | CONST        -> const
        | NAME "(" expr ")" -> fcall
        | NAME "(" expr ("," expr)* ")" -> fcall
        | NAME              -> var
        | "(" expr ")"

    NUMBER : /-?\d+(\.\d+)?([eE][+-]?\d+)?/
    NAME   : /[-+]?\w+/
    CONST : /[+-]?(pi|e|nan)/
    %ignore /\s+/
    %ignore /\#.*/
""")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div

    def __init__(self):
        super().__init__()
        self.variables = {k: v
                    for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)

    def greather(self, x, y):
        return x > y

    def smaller(self, x, y):
        return x < y

    def greather_equal(self, x, y):
        return x >= y

    def smaller_equal(self, x, y):
        return x <= y

    def equal(self, x, y):
        return x == y

    def not_equal(self, x, y):
        return x != y

    def exp(self, x, y):
        return x ** y

    def const(self, token):
        const = self.variables[token.split('-')[-1]]
        if token[0] == '-':
            const *= -1
        return const

    def fcall(self, name, *args):
        name = str(name)
        fn = self.variables[name.split('-')[-1]]
        if name[0] == '-':
            return -fn(*args)
        return fn(*args)

    def var(self, name):
        try:
            return self.variables[name]
        except:
            return self.env[name]

    def assign(self, name, value):
        self.env[name] = value
        return self.env[name]

    def start(self, *args):
        return args[-1]
