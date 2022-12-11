# digtool
digtool is a CLI tool for digital systems. It allows you to specify, parse and
reformat Boolean equations (e.g., in LaTeX form for easy inclusion in
documents). It can create tables from a given Boolean expression and draw a
KV-map with an arbitrary number of variables. It has an expression equality
checker that verifies that two expressions indeed evaluate to the same values
for every input. A Quine-McCluskey implementation is used to minify
expressions. From any expression a canonical form (either disjunctive or
conjunctive) can be generated as well.

## License
GNU GPL-3.
