import sys
import os
import unittest

# Ensure the package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nqueens_solver.solver import solve_n_queens

class TestNQueensSolver(unittest.TestCase):
    def test_nqueens_solutions(self):
        """Test if the solver returns correct number of solutions"""
        self.assertEqual(len(solve_n_queens(4)), 2)  # 4-Queens has 2 valid solutions
        self.assertEqual(len(solve_n_queens(8)), 92)  # 8-Queens has 92 valid solutions

    def test_solution_format(self):
        """Test if the solutions are valid (each row has only one queen)"""
        solutions = solve_n_queens(4)
        for sol in solutions:
            self.assertEqual(len(set(sol)), 4)  # Ensure unique column per row

if __name__ == "__main__":
    unittest.main()
