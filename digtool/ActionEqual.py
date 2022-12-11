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

from .BaseAction import BaseAction
from .ExpressionParser import parse_expression

class ActionEqual(BaseAction):
	def run(self):
		expr1 = parse_expression(self._args.expression1)
		expr2 = parse_expression(self._args.expression2)

		e1_vars = set(expr1.variables)
		e2_vars = set(expr2.variables)
		intersection = e1_vars & e2_vars

		if (intersection != e1_vars) and (intersection != e2_vars):
			print("Cannot compare expressions with different variables.")
			return 2

		if intersection == e2_vars:
			# expr1 has more variables
			(dominant_expr, subordinate_expr) = (expr1, expr2)
		else:
			# expr2 has more variables
			(dominant_expr, subordinate_expr) = (expr2, expr1)

		eq = True
		for (value_dict, eval1) in dominant_expr.table():
			eval2 = subordinate_expr.expr.evaluate(value_dict)
			if eval1 != eval2:
				eq = False
				print(f"Not equal: {value_dict} gives {eval1} on LHS but {eval2} on RHS")
				return 1
		if eq:
			print("Expressions equal.")
			return 0
