# import re
import math
# from lark import Lark, InlineTransformer, Token
from lark import Lark, InlineTransformer

grammar = Lark(r"""
    ?value: expression | name | comparison

    name : /[a-zA-Z]\w*/
    number : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/

    add : expression "+" priority2
    sub : expression "-" priority2
    mul : priority2 "*" priority1
    div : priority2 "/" priority1
    pow : expression_item "^" priority1

    ?priority1 : pow | expression_item
    ?priority2 : mul | div | priority1
    ?priority3 : add | sub

    ?expression : priority3 | priority2

    ?expression_item : number | "(" expression ")"

    eq : expression "==" number
    ge : expression ">=" number
    le : expression "<=" number
    gt : expression ">" number
    lt : expression "<" number
    ne : expression "!=" number

    ?comparison : eq | ge | le | gt | lt | ne

    %import common.WS
    %ignore WS

""", start="value", parser="lalr")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, eq, ge, le, lt, gt, ne

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, n):
        # Peguei essa dica com um brother.
        try:
            return int(n)
        except ValueError:
            return float(n)


if __name__ == "__main__":
    tree = grammar.parse("595 ^ 5 * 121")
    print(tree.pretty())
    parsed = CalcTransformer().transform(tree)
    print(parsed)
