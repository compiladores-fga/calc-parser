import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
r"""

?start: attr* comp*

?comp: sum ">" sum -> greater
    | sum "<" sum -> less
    | sum "<=" sum -> leq
    | sum ">=" sum -> geq
    | sum "==" sum -> eq
    | sum "!=" sum -> neq
    | sum 

?attr: NAME "=" comp

?sum: sum "+" divide -> add
    | sum "-" divide -> minus
    | divide

?divide: divide "*" pow -> mult
    | divide "/" pow -> div
    | pow

?pow: complexatom "^" pow -> pow
    | complexatom

?complexatom: "-" atom -> signedatom
    | atom

?atom: NAME -> variable
    | NUMBER -> number
    | "(" sum ")" -> group
    | call

?call: NAME "(" sum ("," sum)* ")"

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /-?\d+(?:\.\d+)?(?:(?:E|e)(?:\+|-)?\d+)?/

%import common.WS
%ignore /#[^\n]+/ 
%ignore WS
""",
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def pow(self, number, exp):
        return number ** exp

    def sum(self, n1, n2):
        return n1 + n2

    def signedatom(self, value):
        return -value

    def mult(self, n1, n2):
        return n1*n2

    def minus(self, n1, n2):
        return n1 - n2

    def greater(self, n1, n2):
        return n1 > n2

    def less(self, n1, n2):
        return n1 < n2

    def eq(self, n1, n2):
        return n1 == n2

    def neq(self, n1, n2):
        return n1 != n2

    def geg(self, a, b):
        return a >= b

    def leq(self, a, b):
        return a <= b

    def name(self, name):
        return name.value

    def variable(self, name):
        return self.variables[name.value]

    def sig(self, name):
        return name

    def number(self, token):
        return eval(token)

    def attr(self, variable, atom):
        self.variables[variable]=atom

        return self.variables[variable]

    def start(self, *args):
        return args[-1]

    def div(self, n1, n2):
        return  n1/n2

    def call(self, function, *values):

        return self.variables[function](*values)

    def group(self, val):
        return val


if __name__ == '__main__':
    expressions = [
        'x=21',
        'x=21\n2*x',
        '-pi',
    ]
    transformer = CalcTransformer()
    for expression in expressions:
        tree = grammar.parse(expression)
        tree = transformer.transform(tree)
        print(expression)
