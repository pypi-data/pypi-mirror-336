def solve_n_queens(n):
    """Finds and prints all solutions to the N-Queens problem."""
    def print_board(solution, n):
        """Convert solution array into a matrix format and print."""
        board = [['0' for _ in range(n)] for _ in range(n)]
        for row, col in enumerate(solution):
            board[row][col] = 'Q'
        for row in board:
            print(" ".join(row))
        print("\n")

    def is_safe(board, row, col):
        """Check if it's safe to place a queen at board[row][col]."""
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def backtrack(board, row):
        """Recursive function to place queens."""
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1

    solutions = []
    board = [-1] * n
    backtrack(board, 0)

    print(f"Solutions for {n}-Queens:")
    for solution in solutions:
        print_board(solution, n)

    return solutions  # Returns a list of solutions