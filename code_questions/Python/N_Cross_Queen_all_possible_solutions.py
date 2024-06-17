"""
https://leetcode.com/problems/n-queens-ii/description/
"""
def print_board(board: list[list[int]]):

    print("----------------------------------------")
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=' ')
        print("\n")
    print("----------------------------------------")

def solution(n: int):
    
    def safeToPlace(board: list[list[int]], row_index: int, col_index: int):
        """ 
        Returns True if for given board a queen can be places at (row_index, col_index) location False otherwise. 
        Note: 
        1) Queen exists is denoting by 1
        2) This function assumes that the queens are placed starting from left to right. Hence, it only checks if a queen exists at an attacking position
        on the left side of the asked position.
        """
        # print(f"Checking if queen can be placed at ({row_index}, {col_index}) for below board")
        # print_board(board)

        # First check the positions on the left of this row
        # print(f"Checking same row")
        for i in range(col_index):
            # print(f"Checking {row_index},{i}")
            if board[row_index][i] == 1:
                return False

        # Check the upper-left diagonal
        # print(f"Checking upper-left diagonal")
        for i, j in zip(range(row_index, -1, -1), range(col_index, -1, -1)):
            # print(f"Checking {i},{j}")
            if board[i][j] == 1:
                return False

        # Check the bottom-left diagonal
        # print(f"Checking bottom-left diagonal")
        for i, j in zip(range(row_index, len(board), 1), range(col_index, -1, -1)):
            # print(f"Checking {i},{j}")
            if board[i][j] == 1:
                return False

        # print("Can place the queen")
        return True

    def placeQueen(col_index: int, size: int, board: list[list[int]] = [], solutions: list[list[list[int]]] = []):

        if col_index >= size:
            print_board(board)
            solutions.append(board)

        else:
            for row_index in range(size):
                if col_index == 0:
                    # print("Created a new board")
                    board = [[0 for _ in range(n)] for _ in range(n)]

                if safeToPlace(board, row_index, col_index):
                    print(f"Placed the queen at ({row_index}, {col_index})")
                    board[row_index][col_index] = 1
                    placeQueen(col_index+1, size, board, solutions)

                else:
                    print(f"Couldn't place the queen at ({row_index}, {col_index})")
                    board[row_index][col_index] = 0

    solutions = []
    placeQueen(0, n, solutions=solutions)
    return len(solutions)

if __name__ == "__main__":
    n = int(input())
    print(solution(n))
