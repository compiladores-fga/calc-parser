import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
	r"""
?start : compare
	| atribution

?atribution : NAME "=" expr

?compare : expr "==" term -> eq
	| expr ">=" term	-> ge
	| expr "<=" term	-> le
	| expr ">" term		-> gt
	| expr "<" term		-> lt
	| expr "!=" term	-> ne
	| expr

?expr : expr "+" term  	-> add
	| expr "-" term  	-> sub
	| term

?term : term "*" pow  	-> mul
	| term "/" pow  	-> div
	| pow

?pow  : atom "^" pow  	-> exp
	| atom

?atom : NUMBER			-> number
	| NAME 				-> name
	| NAME "(" expr ("," expr)* ")" -> fcall
	| "(" expr ")"

NUMBER : /(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
NAME : /[a-zA-Z_]\w*/
%ignore /\s+/

""",
	parser="lalr",
)


class CalcTransformer(InlineTransformer):
	from operator import add, sub, mul, truediv as div, pow as exp, ne, gt, ge, lt, le, eq

	def __init__(self):
		super().__init__()
		self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
		self.variables.update(max=max, min=min, abs=abs)

	def number(self, token):
		return float(token)