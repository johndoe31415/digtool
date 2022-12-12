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
from .ExpressionFormatter import ExpressionFormatterText, ExpressionFormatterTex

class ActionParse(BaseAction):
	def run(self):
		expr = parse_expression(self._args.expression)
		match self._args.format:
			case "text":
				print(ExpressionFormatterText(expr, implicit_and = not self._args.no_implicit_and))

			case "internal":
				print(expr)

			case "tex-tech":
				print(ExpressionFormatterTex(expr, neg_overline = True, implicit_and = not self._args.no_implicit_and))

			case "tex-math":
				print(ExpressionFormatterTex(expr, neg_overline = False, implicit_and = not self._args.no_implicit_and))

			case _:
				raise NotImplementedError(self._args.format)
