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

import sys
from .ActionParse import ActionParse
from .ActionTable import ActionTable
from .ActionSynthesize import ActionSynthesize
from .ActionEqual import ActionEqual
from .ActionQMC import ActionQMC
from .ActionCanonicalize import ActionCanonicalize
from .ActionRandom import ActionRandom
from .MultiCommand import MultiCommand

def main():
	mc = MultiCommand(description = "Tool to compute and simplify problems in digital systems", run_method = True)

	def genparser(parser):
		parser.add_argument("-n", "--no-implicit-and", action = "store_true", help = "By default, AND operations are implicity expressed (using a space character). This causes an actual operator to be emitted here.")
		parser.add_argument("-f", "--format", choices = [ "tex-tech", "tex-math", "internal" ], default = "tex-tech", help = "Print the expression in the desired format. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("expression", help = "Input expression to parse")
	mc.register("parse", "Parse and reformat a Boolean expression", genparser, action = ActionParse)

	def genparser(parser):
		parser.add_argument("-z", "--kv-show-zeros", action = "store_true", help = "Show zeros explicitly in a KV map")
		parser.add_argument("-f", "--format", choices = [ "text", "table", "tex", "kv" ], default = "text", help = "Print the table in the desired format. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("expression", help = "Input expression to create truth table from")
		parser.add_argument("dc_expression", nargs = "?", help = "Optional expression that gives all don't care values")
	mc.register("table", "Create a truth table for a Boolean expression", genparser, action = ActionTable)

	def genparser(parser):
		parser.add_argument("-n", "--no-optimization", action = "store_true", help = "Do not automatically optimize the resulting expression.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("filename", help = "Filename that contains the table data")
	mc.register("synthesize", "Synthesize a Boolean expression from a given truth table", genparser, action = ActionSynthesize)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("expression1", help = "Input expression 1")
		parser.add_argument("expression2", help = "Input expression 2")
	mc.register("equal", "Comprare two Boolean expression for equality", genparser, action = ActionEqual)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("expression", help = "Expression to minimize")
		parser.add_argument("dc_expression", nargs = "?", help = "Optional expression that gives all don't care values")
	mc.register("qmc", "Minimize a Boolean expression using the Quine-McCluskey method", genparser, action = ActionQMC)

	def genparser(parser):
		parser.add_argument("-c", "--ccnf", action = "store_true", help = "By default, the canonical disjunctive normal form (CDNF) is generated. With this switch, the canonical conjunctive normal form (CCNF) is generated instead.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("expression", help = "Input expression to canonicalize")
	mc.register("canonicalize", "Canonicalize an expression into CDNF or CCNF", genparser, action = ActionCanonicalize)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be given multiple times.")
		parser.add_argument("var_count", type = int, help = "Number of variables in expression")
		parser.add_argument("minterm_count", type = int, help = "Number of minterms in expression")
	mc.register("random", "Generate a randomized CDNF", genparser, action = ActionRandom)

	sys.exit(mc.run(sys.argv[1:]) or 0)

if __name__ == "__main__":
	main()
