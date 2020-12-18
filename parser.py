import math
from lark import Lark, InlineTransformer


grammar = Lark(
	r"""
?start : atribution* compare?

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

NUMBER : /-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/
NAME : /\-?[a-zA-Z_]\w*/
%ignore /\s+/

%ignore /\#.*/
""",
	parser="lalr",
)


class CalcTransformer(InlineTransformer):
	from operator import add, sub, mul, truediv as div, pow as exp, ne, gt, ge, lt, le, eq

	def __init__(self):
		super().__init__()
		self.variables = {
			k: v for k, v in vars(math).items() if not k.startswith("_")}
		self.variables.update(max=max, min=min, abs=abs)

	def number(self, token):
		# exponenciação tem problemas de overflow em floats grandes
		try:
			return int(token)
		except ValueError:
			return float(token)
	
	def name(self, token):
		if token[0] == '-':
			token = token.lstrip("-")
			if(token in self.variables):
				return -float(self.variables[token])
			else:
				return -float(token)
		else:
			if(token in self.variables):
				return self.variables[token]
			else:
				return token
	
	def fcall(self, *args):
		if len(args) > 2:
			if args[0][0] == "-":
				result = args[0].lstrip("-")
				return -float(self.variables.get(result)(args[1:]))
			return self.variables.get(args[0])(args[1:])
		else:
			if args[0][0] == "-":
				result = args[0].lstrip("-")
				return -float(self.variables.get(result)(args[1]))
			return self.variables.get(args[0])(args[1])

	def atribution(self, *args):
		self.variables.update({args[0]: args[1]})
		return self.variables[args[0]]
	
	def start(self, *args):
		return args[-1]
