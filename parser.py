import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(r"""
        ?start : assign* test* 
        
        assign: NAME "=" test       -> assign
        
        ?test : expr "<=" atom      -> le
              | expr ">=" atom      -> ge
              | expr ">" atom       -> gt
              | expr "<" atom       -> lt
              | expr "!=" atom      -> ne
              | expr "==" atom      -> eq
              | NEG atom            -> neg
              | expr

        ?expr : expr "+" term       -> add
              | expr "-" term       -> sub
              | term
        
        ?term : term "*" pow        -> mul
              | term "/" pow        -> div 
              | pow
        
        ?pow  : atom "^" pow        -> pow
              | atom
        
        ?atom : NUMBER              -> number
              | NAME "(" expr ("," expr)* ")"   -> fcall
              | NAME                -> var
              | "(" expr ")"
              
        NEG    : /(?<=^)-/
        NUMBER : /(-?\d+(\.\d+)?(e[+-]?\d+)?)|pi/
        NAME   : /[\w_]+/
        %ignore /\s+|#.*/
""")


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, abs, pow, lt, le, eq, ne, gt, ge

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, token):
        try:
            return int(token)
        except ValueError:
            if token == 'pi':
                return math.pi
            else:
                return float(token)

    def max(self, y):
        return max(y)

    def min(self, y):
        return min(y)

    def neg(self, x, y):
        return y*(-1)

    def cos(self, y):
        return math.cos(y)

    def sin(self, y):
        return math.sin(y)

    def var(self, name):
        return self.variables[name]

    def assign(self, name, value):
        self.variables[name] = value
        return self.variables[name]

    def fcall(self, name, *args):
        name = str(name)
        fn = getattr(self, name)
        if len(args) == 1:
            return fn(args[0])
        else:
            return fn(args)

    def start(self, *args):
        return args[-1]
