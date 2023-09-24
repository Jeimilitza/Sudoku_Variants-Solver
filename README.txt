Sudoku-Knight-King:

A Sudoku puzzle that adheres to the standard Sudoku rules and includes additional constraints based on chess moves. Specifically, any two cells separated by a knight move or king move in chess cannot contain the same digit.

King, Diagonal Sudoku:

There is also a sudoku with the chess King constraints and additionally the Diagonal Sudoku variant which introduces an X-like constraint as well. 

We aim to generate a solvable puzzle that requires the application of various beginner, intermediate and advanced Sudoku techniques to be solved. 


Technique used to solve the Sudokus:

Naked Singles: Identifying cells with only one possible value and filling them.
Hidden Singles: Locating cells where a digit can only go in one position within a unit (row, column, or box) and filling them.
Pointing Pairs/Triples: Finding a unit where a digit is confined to a subset of cells, eliminating that digit from other cells within the subset.
Hidden Pairs/Triples: Examining a unit (box) to determine if there are digits confined to a specific row/column, eliminating those digits from other cells in the row/column.
X-Wing: Identifying a pattern where two rows or two columns have the same candidate values for a digit, eliminating those candidates from other cells in the corresponding columns or rows.
Swordfish: Extending the X-Wing pattern to three rows or three columns.
These solving techniques provide increasingly complex strategies to solve the Sudoku puzzle while incorporating the king and knight move constraints.

