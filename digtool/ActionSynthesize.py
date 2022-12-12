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

import re
from .BaseAction import BaseAction
from .ExpressionParser import parse_expression
from .ExpressionFormatter import ExpressionFormatterText
from .QuineMcCluskey import QuineMcCluskey

class ActionSynthesize(BaseAction):
	_RE_SEP = re.compile("\s+")

	def run(self):
		minterms = [ ]
		dc_expr = [ ]

		varnames = None
		with open(self._args.filename) as f:
			for (lineno, line) in enumerate(f, 1):
				line = line.rstrip("\r\n")
				if line.startswith("#"):
					continue

				if varnames is None:
					varnames = self._RE_SEP.split(line)
				else:
					values = self._RE_SEP.split(line)
					if len(values) != len(varnames) + 1:
						print(f"Error: cannot parse line {lineno}")
					else:
						minterm = " ".join(f"{'-' if (int(value) == 0) else ''}{varname}" for (varname, value) in zip(varnames, values))
						evaluation = values[-1]
						try:
							evaluation = int(evaluation)
						except ValueError:
							evaluation = None

						if evaluation == 1:
							# Minterm
							minterms.append(minterm)
						elif evaluation is None:
							# Don't care
							dc_expr.append(minterm)

		if len(minterms) == 0:
			print("0")
			return 0

		expr = parse_expression(" + ".join(minterms))
		if len(dc_expr) > 0:
			dc_expr = parse_expression(" + ".join(dc_expr))
		else:
			dc_expr = None
		if not self._args.no_optimization:
			qmc = QuineMcCluskey(expr, dc_expr, verbosity = self._args.verbose)
			result = qmc.optimize()
		else:
			result = str(ExpressionFormatterText(expr))
		print(result)
