import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
r"""
?start      : assign* expr?

assign      : NAME "=" expr

?expr  : expr "+" term -> sum
       | expr "-" term -> sub
       | term
       | comparison

?comparison : mexpr ">" mexpr                 -> greater
            | mexpr "<" mexpr                 -> smaller
            | mexpr ">=" mexpr                -> greater_eq
            | mexpr "<=" mexpr                -> smaller_eq
            | mexpr "==" mexpr                -> eq
            | mexpr "!=" mexpr                -> not_eq
            | mexpr

?mexpr      : expr "+" term                 -> sum
            | expr "-" term                 -> sub
            | term

?term       : term "*" pow                  -> mul
            | term "/" pow                  -> div
            | pow

?pow        : atom "^" pow                 -> exp
            | atom

?atom       : NUMBER                        -> number
            | CONST                         -> const
            | NAME "(" expr ")"             -> fcall
            | NAME "(" expr ("," expr)* ")" -> fcall
            | NAME                          -> var
            | "(" expr ")"

NUMBER      : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
NAME        : /-?\w+/
CONST       : /-?(pi|e|tau|inf|nan)/

%ignore /\s+/
%ignore /\#[^\n]*/
"""
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.env = {}

    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)
    
    def sum(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y
    
    def mul(self, x, y):
        return x * y
    
    def div(self, x, y):
        return x / y
    
    def exp(self, x, y):
        return x ** y

    def greater(self, x, y):
        return x > y

    def smaller(self, x, y):
        return x < y

    def greater_eq(self, x, y):
        return x >= y

    def smaller_eq(self, x, y):
        return x <= y

    def eq(self, x, y):
        return x == y

    def not_eq(self, x, y):
        return x != y

    def fcall(self, name, *args):
        name = str(name)
        if name.startswith('-'):
            fn = self.variables[name.split('-')[1]]
            try:
                return -fn(*args)
            except TypeError:
                return -fn(args)
        else:
            fn = self.variables[name]
            try:
                return fn(*args)
            except TypeError:
                return fn(args)

    def assign(self, name, value):
        self.env[name] = value
        return self.env[name]

    def const(self, name):
        return -self.variables[name.split('-')[1]] if name.startswith('-')  else self.variables[name]

    def var(self, name):
        return self.variables[name] if name in self.variables else self.env[name]

    def start(self, *args):
        return args[-1]
