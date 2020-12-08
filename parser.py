import re
import math
from lark import Lark, InlineTransformer, Token


# Implemente a gramática aqui! Você pode testar manualmente seu código executando
# o arquivo calc.py e testá-lo utilizando o pytest.
grammar = Lark(
    r"""

?start 	: bool

?bool	: expr ">" expr			-> maior
       	| expr ">=" expr		-> maiorigual
       	| expr "<" expr			-> menor
       	| expr "<=" expr		-> menorigual
       	| expr "==" expr		-> igual
       	| expr "!=" expr		-> diferente
       	| expr 
       	| expr com 				-> exprcom
       	| com

?com 	: COMMENT			-> com

?expr	: expr "+" term  	-> so
       	| expr "-" term  	-> su
       	| term
 
?term  	: term "*" pow  	-> mu
       	| term "/" pow  	-> di
       	| pow

?pow   	: atom "^" pow  	-> po
       	| atom

?atom  	: NUMBER        			-> num
		| VARIABLE 					-> var
       	| VARIABLE "(" expr ")"		-> func
       	| "(" expr ")"

VARIABLE 	: /-?\w+/
NUMBER 		: /-?\d+(\.[\d|e|\+|-]+)?/
COMMENT 	: /#.+$/

%ignore /\s+/
""",
	parser="lalr",
)


class CalcTransformer(InlineTransformer):
	from operator import add, sub, mul, truediv as div  # ... e mais! 

	def __init__(self):
		super().__init__()
		self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
		self.variables.update(max=max, min=min, abs=abs)

	def var(self, token):
		if token == 'pi':
			return math.pi
		elif token == '-pi':
			return -math.pi
		elif token == 'sin':
			return math.sin
		elif token == '-sin':
			return -math.sin
		elif token == 'cos':
			return math.cos
		elif token == '-cos':
			return -math.cos
		return str(token)

	def func(self, token, x):
		if token == 'abs':
			return abs(x)
		if token[0] == '-':
			token = token[1:]
			fn = getattr(math, str(token))
			return fn(x)*-1
		fn = getattr(math, str(token))
		return fn(x)

	def num(self, token):
		return float(token)

	def so(self, x, y):
		return x + y

	def su(self, x, y):
		return x - y

	def mu(self, x, y):
		return x * y

	def di(self, x, y):
		return x / y

	def po(self, x, y):
		return x ** y

	def maior(self, x, y):
		return x > y

	def menor(self, x, y):
		return x < y

	def maiorigual(self, x, y):
		return x >= y

	def menorigual(self, x, y):
		return x <= y

	def igual(self, x, y):
		return x == y

	def diferente(self, x, y):
		return x != y

	def com(self, token):
		return ''

	def exprcom(self, expr, com):
		return expr