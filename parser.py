# import re
import math
# from lark import Lark, InlineTransformer, Token
from lark import Lark, InlineTransformer

grammar = Lark(r"""
    ?value: name
          | number
          | expression

    name : /[a-zA-Z]\w*/
    number : /(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/

    operator : "+"
             | "-"
             | "/"
             | "*"
             | "^"

    expression : simple_expression | composite_expression

    expression_item : number | composite_expression

    simple_expression : expression_item operator expression_item [(operator expression_item)*]
    composite_expression: "(" simple_expression ")"

    %import common.WS
    %ignore WS

""", start="value", parser="lalr")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div  # ... e mais!

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)


if __name__ == "__main__":
    tree = grammar.parse("ti")
    print(tree)
