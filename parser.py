import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
start  : comp?

?atom  : NUMBER -> number
       | NAME "(" expr ")" -> function
       | NAME "(" expr ("," expr)* ")" -> function
       | NAME -> variable
       | "(" expr ")"

?comp  : expr ">" expr  -> gt
       | expr "<" expr  -> lt
       | expr ">=" expr -> ge
       | expr "<=" expr -> le
       | expr "==" expr -> eq
       | expr "!=" expr -> ne
       | expr

?expr  : expr "-" term -> sub
       | expr "+" term -> add
       | term

?term  : term "/" pow -> div
       | term "*" pow -> mul
       | pow

?pow   : atom "^" pow -> exp
       | atom


NAME   : /[-+]?\w+/
NUMBER : /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
%ignore /\s+/
%ignore /\#.*/
""")


class CalcTransformer(InlineTransformer):
       from operator import add, sub, mul, truediv as div, pow as exp, gt, ge, lt, le, ne, eq

       def __init__(self):
              super().__init__()
              self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
              self.variables.update(max=max, min=min, abs=abs)
              self.env = {}

       def number(self, token):
              try:
                     return int(token)
              except:
                     return float(token)

       def const(self, token):
              value = self.variables[token]

              return value

       def variable(self, token):
              if token in self.variables:
                     return self.variables[token]
              elif token[0] == "-" and token[1:] in self.variables:
                     return -(self.variables[token[1:]])
              else:
                     return self.env[token]

       def function(self, name, *args):
              name = str(name)
              fn = self.variables[name.split('-')[-1]]
       
              if name[0] == '-':
                     return -fn(*args)
              
              return fn(*args)

       def start(self, *args):
              return args[-1]
