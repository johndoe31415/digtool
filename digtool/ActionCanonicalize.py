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

class ActionCanonicalize(BaseAction):
	def run(self):
		self._expr = parse_expression(self._args.expression)

		if not self._args.ccnf:
			minterms = [ ]
			for minterm in self._expr.minterms():
				minterm_str = [ ]
				for varname in self._expr.variables:
					if minterm[varname]:
						minterm_str.append(f"{varname}")
					else:
						minterm_str.append(f"-{varname}")
				minterm_str = " ".join(minterm_str)
				minterms.append(minterm_str)
			print(" + ".join(minterms))
		else:
			maxterms = [ ]
			for maxterm in self._expr.maxterms():
				maxterm_str = [ ]
				for varname in self._expr.variables:
					if maxterm[varname]:
						maxterm_str.append(f"-{varname}")
					else:
						maxterm_str.append(f"{varname}")
				maxterm_str = "(" + " + ".join(maxterm_str) + ")"
				maxterms.append(maxterm_str)
			print("".join(maxterms))
