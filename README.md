# Sudoku Solver using Backtracking
This Python script solves Sudoku puzzles using a backtracking algorithm. Given an incomplete Sudoku puzzle, the program fills in the missing values such that the completed puzzle adheres to the rules of Sudoku - each row, column, and 3x3 subgrid must contain all the digits from 1 to 9 without repetition.

## How to Use
Input the Sudoku Puzzle:

  1. **Modify the board variable in the script to represent your Sudoku puzzle. Use -1 to denote empty cells.
  python
  ```
  board = [
      [3, 9, -1, -1, 5, -1, -1, -1, -1],
      [-1, -1, -1, 2, -1, -1, -1, -1, 5],
      ... (complete the puzzle)
  ]**
```
2. **Run the Script:**

  Execute the script, and the solver will attempt to fill in the missing values.
  python using backtracking

3. **View the Result:**

The solved puzzle will be printed using the pprint module.
