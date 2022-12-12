#	digtool - Tool to compute and simplify problems in digital systems
#	Copyright (C) 2022-2022 Johannes Bauer
#
#	This file is part of digtool.
#
#	digtool is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	digtool is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with digtool; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import enum
import functools
from . import tpg

class Operator(enum.Enum):
	Or = "+"
	And = "*"
	Xor = "^"
	Not = "!"
	Nand = "@"
	Nor = "#"

	@classmethod
	def lookup(cls, value):
		return {
			"+":	cls.Or,
			"|":	cls.Or,
			"*":	cls.And,
			"&":	cls.And,
			"^":	cls.Xor,
			"!":	cls.Not,
			"-":	cls.Not,
			"~":	cls.Not,
			"@":	cls.Nand,
			"#":	cls.Nor,
		}[value]

class Variable():
	def __init__(self, varname):
		self._varname = varname

	@property
	def varname(self):
		return self._varname

	def evaluate(self, var_dict):
		return var_dict[self.varname]

	def __str__(self):
		return self.varname

class Constant():
	def __init__(self, value):
		assert(value in (0, 1))
		self._value = value

	@property
	def value(self):
		return self._value

	def evaluate(self, var_dict):
		return self.value

	def __str__(self):
		return str(self.value)

class UnaryOperator():
	def __init__(self, op, rhs):
		self._op = Operator.lookup(op)
		self._rhs = rhs

	@property
	def op(self):
		return self._op

	@property
	def rhs(self):
		return self._rhs

	def evaluate(self, var_dict):
		assert(self._op == Operator.Not)
		return int(not self.rhs.evaluate(var_dict))

	def __repr__(self):
		return f"{self.op.value}({self.rhs})"

class BinaryOperator():
	def __init__(self, lhs, op, rhs):
		self._lhs = lhs
		self._op = Operator.lookup(op)
		self._rhs = rhs

	@property
	def lhs(self):
		return self._lhs

	@property
	def op(self):
		return self._op

	@property
	def rhs(self):
		return self._rhs

	def evaluate(self, var_dict):
		lhs = self.lhs.evaluate(var_dict)
		rhs = self.rhs.evaluate(var_dict)
		fnc = {
			Operator.Or: lambda x, y: x | y,
			Operator.And: lambda x, y: x & y,
			Operator.Xor: lambda x, y: x ^ y,
			Operator.Nand: lambda x, y: int(not (x & y)),
			Operator.Nor: lambda x, y: int(not (x | y)),
		}[self.op]
		return fnc(lhs, rhs)

	def __repr__(self):
		return f"({self.lhs} {self.op.value} {self.rhs})"

class ExpressionParser(tpg.Parser):
	r"""
		separator space '\s+';

		token or_op     '[|+]';
		token and_op    '[&*]';
		token xor_op    '[\^]';
		token nand_op    '@';
		token nor_op    '#';
		token neg_op	'[!-]';
		token const 	'[01]';
		token variable  '[a-zA-Z_][a-zA-Z0-9_]*'		$ Variable

		START/e ->
				Expr/e
		;

		Expr/lhs -> Term/lhs ( or_op/op Term/rhs		$ lhs = BinaryOperator(lhs, op, rhs)
					)*
		;

		Term/lhs -> Atom/lhs ( and_op/op Atom/rhs		$ lhs = BinaryOperator(lhs, op, rhs)
							| xor_op/op Atom/rhs		$ lhs = BinaryOperator(lhs, op, rhs)
							| nand_op/op Atom/rhs		$ lhs = BinaryOperator(lhs, op, rhs)
							| nor_op/op Atom/rhs		$ lhs = BinaryOperator(lhs, op, rhs)
							| Atom/rhs					$ lhs = BinaryOperator(lhs, "*", rhs)
					)*
		;

		Atom/a ->
				variable/a
			|	const/a					$ a = Constant(int(a))
			|	neg_op/op Atom/a		$ a = UnaryOperator(op, a)
			|   '\(' Expr/a '\)'
		;

	"""

class ParsedExpression():
	def __init__(self, expr):
		self._expr = expr

	@property
	def expr(self):
		return self._expr

	@property
	def state_count(self):
		return 1 << len(self.variables)

	@functools.cached_property
	def variables(self):
		varnames = set()
		for element in self:
			if isinstance(element, Variable):
				varnames.add(element.varname)
		varnames = tuple(sorted(varnames))
		return varnames

	def _traverse(self, element):
		yield element
		if isinstance(element, UnaryOperator):
			yield from self._traverse(element.rhs)
		elif isinstance(element, BinaryOperator):
			yield from self._traverse(element.lhs)
			yield from self._traverse(element.rhs)

	def table(self):
		for value in range(self.state_count):
			value_dict = { varname: int((value & (1 << (len(self.variables) - 1 - varno))) != 0) for (varno, varname) in enumerate(self.variables) }
			evaluation = self._expr.evaluate(value_dict)
			yield (value_dict, evaluation)

	def minterms(self):
		for (value_dict, evaluation) in self.table():
			if evaluation == 1:
				yield value_dict

	def maxterms(self):
		for (value_dict, evaluation) in self.table():
			if evaluation == 0:
				yield value_dict

	def __iter__(self):
		yield from self._traverse(self._expr)

	def __str__(self):
		return str(self.expr)

def parse_expression(expr):
	parser = ExpressionParser()
	return ParsedExpression(parser(expr))


if __name__ == "__main__":
	parser = ExpressionParser()

	testcases = [
			"A + B",
			"A + B + C",
			"A + (B + C)",
			"A * B + C",
			"A + B * C",
			"A + B ^ C",
			"A ^ B ^ C",
			"A ^ B + C",
			"A B C + !A !B !C + A !B C Foo",
			"A ^ !B",
			"!(A ^ B)",
			]
	for input_value in testcases:
		try:
			parsed = parser(input_value)
			print(parsed)
		except Exception as e:
			print(tpg.exc())
			raise
