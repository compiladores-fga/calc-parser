import re
import math
from lark import Lark, InlineTransformer, Token

# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""
    ?start  : attr* comp?
    
    ?var    : VAR -> variable
    
    ?attr   : VAR "=" comp
    
    ?expr   : term "+" expr -> sum
            | term "-" expr -> sub
            | term    
            
    ?func   : VAR "(" expr ")" -> func
            | VAR "(" expr("," expr)* ")" -> func
            
    ?pow    : atom "^" pow   -> pow
            | atom
            
    ?term   : term "*" pow -> mul
            | term "/" pow -> div
            | pow
     
    ?atom   : NUMBER -> number
            | VAR -> variable
            |"(" expr ")"
            | func
    
    ?comp   : expr ">"  expr -> bigger_then
            | expr "<"  expr -> less_then
            | expr ">=" expr -> greater_equal 
            | expr "<=" expr -> less_equal 
            | expr "!=" expr -> different
            | expr "==" expr -> equal
            | expr
    
    NUMBER  : /-?\d+(\.[0-9]+)?([eE][-+]?[0-9]+)?/
    VAR     : /[+-]?\w+/
    %ignore /\s+/
    %ignore /\#.+/
    """
)
expressions = [
    "42 != 10",
    "42 == 42",
    "pi",
    "42",
    "10^5",
    "-10",
    "3.14",
    "40 + 2",
    "21 * 2",
    "80 - 38",
    "1 + 1 + 1",
    "1 + 1 - 1",
    "2 * 2 * 2 / 8",
    "82 / 2",
    "20 * 2 + 2",
    "2 + 20 * 2",
    "32 / 4 / 2",
    "10 -2 -3",
    "(2 + 20) * 2",
    "(2 + (10+10)) * 2",
    "2 + 2 > 3",
    "4 ^ 2 - 2",
    "-cos(pi)",
    "abs(-2)",
    "x = -115",
    "-pi",
    "x = 0\nx = 21\n2 * x",
    "0 - 1 - 1"
]


class CalcTransformer(InlineTransformer):
    from operator import add as sum, sub, mul, truediv as div, pow, gt as bigger_then, eq as equal, lt as less_then, \
        ne as different, le as less_equal, ge as greater_equal

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        print(self.variables)
        self.env = {}

    def number(self, token):
        try:
            return int(token)
        except:
            return float(token)

    def variable(self, token):
        if token in self.variables:
            return self.variables[token]
        elif token[0] == "-" and token[1:] in self.variables:
            return -self.variables[token[1:]]
        else:
            return self.env[token]

    def func(self, name, *args):
        name = str(name)
        fn = self.variables[name.split('-')[-1]]
        if name[0] == '-':
            return -fn(*args)
        return fn(*args)

    def attr(self, name, value):
        self.env[name] = value
        return self.env[name]

    def start(self, *args):
        return args[-1]


transformer = CalcTransformer()
for expression in expressions:
    tree = grammar.parse(expression)
    tree = transformer.transform(tree)
    print(expression)
    print(tree)
    print('-' * 40)
