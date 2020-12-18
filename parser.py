# import re
import math
# from lark import Lark, InlineTransformer, Token
from lark import Lark, InlineTransformer

grammar = Lark(r"""
    ?value: expression | name

    name : /[a-zA-Z]\w*/
    number : /(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/

    add : priority1 "+" expression
    sub : priority1 "-" expression
    mul : priority1 "*" expression_item
    div : priority1 "/" expression_item
    pow: priority1 "^" expression_item

    ?priority1 : mul | div | pow | expression_item
    ?priority2 : add | sub

    ?expression : priority2 | priority1

    ?expression_item : number | "(" expression ")"

    %import common.WS
    %ignore WS

""", start="value", parser="lalr")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, n):
        return float(n)


if __name__ == "__main__":
    tree = grammar.parse("2 * (2 + 1) + 1")
    print(tree.pretty())
    parsed = CalcTransformer().transform(tree)
    print(parsed)
