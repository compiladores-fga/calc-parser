import re
import math
from lark import Lark, InlineTransformer, Token

# BASIC CALCULATOR: https://lark-parser.readthedocs.io/en/latest/examples/calc.html?highlight=calculator#
# OPERATOR: https://docs.python.org/3/library/operator.html
# Example: https://github.com/lark-parser/lark/blob/master/examples/calc.py

# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.

grammar = Lark(
    r"""
    
    ?start  : assign* comp?

    ?assign: NAME "=" comp

    ?comp   : expr ">" expr  -> gt
            | expr ">=" expr -> ge
            | expr "<" expr  -> lt
            | expr "<=" expr -> le
            | expr "!=" expr -> ne
            | expr "==" expr -> eq
            | expr

    ?expr   : expr "+" term  -> add
            | expr "-" term  -> sub
            | term



    ?term   : term "*" exp   -> mul
            | term "/" exp   -> div
            | "not" term     -> not_
            | term "%" exp   -> mod
            | term "&" exp   -> and_
            | term "|" exp   -> or_
            | term "<<" exp   -> lshift            
            | exp


    ?exp    : atom "^" exp   -> pow
            | atom

    ?atom   : NUMBER                        -> number
            | NAME "(" expr ")"             -> fcall
            | NAME "(" expr ("," expr)* ")" -> fcall
            | NAME                          -> var
            | "(" expr ")"

    NAME    : /([\w]|[-+])\w*/

    NUMBER : /([-+])?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
    
    
    %ignore /\s+/
    %ignore /\#.*/
    %ignore /\#[^\n]*/

    """,
    parser="lalr",

)


class CalcTransformer(InlineTransformer):
    
    # OPERATOR : https://docs.python.org/3/library/operator.html
    # Tomou-se a liberdade de acrescentar-se algumas outras operacoes
    from operator import add, sub, mul, truediv as div, pow, eq, ne, gt, ge, lt, le, not_, mod, lshift, and_, or_  # ... e mais! 

    def __init__(self):
        super().__init__()
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)
        self.vars = {}

    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)

    def var(self, token):
        try:
            if token in self.variables:
                return self.variables[token]
            elif token[0] == "-" and token[1:] in self.variables:
                return -self.variables[token[1:]]
            else:
                return self.vars[token]
        except KeyError:
            # ENTRADA INVALIDA
            return "Invalid input: " + str(token)

    def fcall(self, name, *args):
        fn = self.variables[name.split('-')[-1]]
        try:
            if name[0] == '-':
                return -fn(*args)
            else:
                fn = self.variables[name]
                return fn(*args)
        except:
            return "Invalid!"

    def assign(self, name, value):
        self.vars[name] = value
        print("ASSIGN", self.vars[name])
        return self.vars[name]
    
    def start(self, *args):
        return args[-1]

