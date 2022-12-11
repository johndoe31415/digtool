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

class Table():
	def __init__(self, width, height):
		self._width = width
		self._height = height
		self._cells = [ ]
		for y in range(height):
			self._cells.append([ "" ] * width)

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	def row(self, y):
		yield from self._cells[y]

	def column(self, x):
		for y in range(self.height):
			yield self.get(x, y)

	def max_col_width(self, x):
		return max(len(cell) for cell in self.column(x))

	def get(self, x, y):
		return self._cells[y][x]

	def set(self, x, y, value):
		self._cells[y][x] = value

	def print(self):
		col_widths = [ self.max_col_width(x) for x in range(self.width) ]
		l_pad = 1
		r_pad = 1
		y_sep = ""
		for row in self._cells:
			line = [ ]
			for (x, cell_data) in enumerate(row):
				cell = f"{' ' * l_pad}{cell_data:<{col_widths[x]}}{' ' * r_pad}"
				line.append(cell)
			print(y_sep.join(line))
