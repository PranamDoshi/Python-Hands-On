"""
There is a NxN chess board. The target is to place N queens on any square of the board such that no queen is killing any other queen.
"""
def print_board(board: list[list[int]]):

    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=' ')
        print("\n")

def solution(n: int):
    
    def safeToPlace(board: list[list[int]], row_index: int, col_index: int):
        """ 
        Returns True if for given board a queen can be places at (row_index, col_index) location False otherwise. 
        Note: 
        1) Queen exists is denoting by 1
        2) This function assumes that the queens are placed starting from left to right. Hence, it only checks if a queen exists at an attacking position
        on the left side of the asked position.
        """
        # print_board(board)

        # First check the positions on the left of this row
        print(f"Checking same row")
        for i in range(col_index):
            # print(f"Checking {row_index},{i}")
            if board[row_index][i] == 1:
                return False

        # Check the upper-left diagonal
        print(f"Checking upper-left diagonal")
        for i, j in zip(range(row_index, -1, -1), range(col_index, -1, -1)):
            # print(f"Checking {i},{j}")
            if board[i][j] == 1:
                return False
                
        # Check the bottom-left diagonal
        print(f"Checking bottom-left diagonal")
        for i, j in zip(range(row_index, len(board), 1), range(col_index, -1, -1)):
            # print(f"Checking {i},{j}")
            if board[i][j] == 1:
                return False

        return True
    
    def placeQueen(board: list[list[int]], col_index: int):

        if col_index >= len(board):
            return True

        for row_index in range(len(board)):
            print(f"Placing queen at {row_index},{col_index}")

            if safeToPlace(board, row_index, col_index):
                board[row_index][col_index] = 1

                if placeQueen(board, col_index+1):
                    print(f"Able to place queen at {row_index}, {col_index}")
                    print_board(board)
                    return True

                board[row_index][col_index] = 0

        print(f"Can't place queen at {row_index},{col_index}")
        return False

    # Test that the safeToPlace fuction is working as expected
    assert safeToPlace([
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ], 1, 1) == False

    assert safeToPlace([
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ], 1, 2) == True

    board = [[0 for _ in range(n)] for _ in range(n)]
    print_board(board)
    assert placeQueen(board, 0) == True

    print("---------------------------------------------------------------------")
    return board

if __name__ == "__main__":
    n = int(input())
    print_board(solution(n))
