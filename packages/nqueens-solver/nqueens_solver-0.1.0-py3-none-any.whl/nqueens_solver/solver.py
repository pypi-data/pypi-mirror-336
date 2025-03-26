def solve_n_queens(n):
    solutions = []
    board = [-1] * n  # Store column positions of queens

    def is_safe(row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == row - i:
                return False
        return True

    def backtrack(row):
        if row == n:
            solutions.append(board[:])  # Store a valid solution
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)

    backtrack(0)
    return solutions

def print_board(solutions, n):
    print(f"Total solutions for {n}-Queens: {len(solutions)}\n")
    for sol in solutions:
        print("Solution:")
        for row in sol:
            line = ['.'] * n  # Create a row with empty spaces
            line[row] = 'Q'   # Place the queen
            print(" ".join(line))
        print("\n" + "-" * (2 * n - 1) + "\n")  # Separate solutions

if __name__ == "__main__":
    n = 4  # Change this value for different board sizes
    solutions = solve_n_queens(n)
    print_board(solutions, n)
