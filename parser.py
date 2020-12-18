import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(r"""
?start : code

?code : statement+ -> multiple

?statement : expr
           | assignment

?assignment : NAME "=" expr

?expr : comparison
      | addition

?comparison : addition ">" addition -> gt
           | addition "<" addition -> lt
           | addition ">=" addition -> ge
           | addition "<=" addition -> le
           | addition "==" addition -> eq
           | addition "!=" addition -> ne

?addition : addition "+" multiplication -> add
          | addition "-" multiplication -> sub
          | multiplication

?multiplication : multiplication "*" power -> mul
                | multiplication "/" power -> div
                | power

?power : atom "^" power
       | atom

?fargs : "(" expr ("," expr)* ")"

?atom : NUMBER -> number
      | NAME -> var
      | "(" expr ")"
      | "-" atom -> neg
      | NAME fargs -> fcall

NUMBER : /\d+(\.\d+)?([eE][+-]?\d+)?/
NAME : /[a-zA-Z_][a-zA-Z_0-9]*/
COMMENT : /#[^\n]*/
WHITESPACE : /\s+/

%ignore WHITESPACE
%ignore COMMENT
""",
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, lt, gt, le, ge, eq, ne, neg

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def assignment(self, name, value):
        self.variables[name] = value
        return value

    def var(self, name):
        return self.variables[name]

    def power(self, x, y):
        return pow(x, y)

    def number(self, x):
        try:
            return int(x)
        except ValueError:
            return float(x)

    def fargs(self, *args):
        return args

    def fcall(self, name, args):
        return self.variables[name](args)

    def multiple(self, *values):
        return values[-1]
