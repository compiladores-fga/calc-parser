# import re
import math
# from lark import Lark, InlineTransformer, Token
from lark import Lark, InlineTransformer

grammar = Lark(r"""
    ?value : assignment* start?
    ?start : expression | comparison

    NAME : /\-?[a-zA-Z_]\w*/
    number : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/

    ?function_body : expression [("," expression)*]

    name: NAME

    ?function : NAME "(" function_body ")" | name

    ?assignment : NAME "=" expression

    add : expression "+" priority2
    sub : expression "-" priority2
    mul : priority2 "*" priority1
    div : priority2 "/" priority1
    pow : expression_item "^" priority1

    ?priority1 : pow | expression_item
    ?priority2 : mul | div | priority1
    ?priority3 : add | sub

    ?expression : priority3 | priority2

    ?expression_item : number | "(" expression ")" | function

    eq : expression "==" number
    ge : expression ">=" number
    le : expression "<=" number
    gt : expression ">" number
    lt : expression "<" number
    ne : expression "!=" number

    ?comparison : eq | ge | le | gt | lt | ne

    %import common.WS
    %ignore WS
    %ignore /#.*/

""", start="value", parser="lalr")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, eq, ge, le, lt, gt, ne

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, n):
        try:
            return int(n)
        except ValueError:
            return float(n)

    def name(self, n):
        negative = False

        if n[0] == "-":
            n = n[1:]
            negative = True

        if n in self.variables:
            var = self.variables[n]

            if negative:
                try:
                    return var * -1
                except TypeError:
                    return ("-", var)
            else:
                return var

        return n

    def function(self, *args):
        func = args[0].value
        mul = 1

        if func[0] == "-":
            func = func[1:]
            mul = -1

        if func in self.variables:
            func = self.variables[func]
            try:
                values = args[1].children
                return func(values) * mul
            except AttributeError:
                return func(args[1]) * mul
            return func(args[1]) * mul

        return args

    def assignment(self, *args):
        print("arg0", args[0])
        print("arg1", args[1])
        self.variables[args[0]] = args[1]
        return args[1]

    def value(self, *args):
        return args[-1]


if __name__ == "__main__":
    # tree = grammar.parse("x = 0\nx = 21\n2 * x")
    tree = grammar.parse("cos(pi)")
    print(tree.pretty())
    parsed = CalcTransformer().transform(tree)
    print(parsed)
