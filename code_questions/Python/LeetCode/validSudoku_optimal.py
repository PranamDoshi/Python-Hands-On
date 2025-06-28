"""
https://leetcode.com/problems/valid-sudoku/
"""
from typing import List
from collections import defaultdict

class Solution:
    def print_matrix(self, matrix):
        print("===================================")
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                print(matrix[x][y], end=',')
            print()

    def isValidSudoku(self, board: List[List[str]]) -> bool:

        def get_sub_matrix_id(i, j):
            return ((3*(i//3)) + (j//3))

        # row_encountered_indexes = [[0 for _ in range(len(board))] for _ in range(len(board[0]))]
        # column_encountered_indexes = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
        subMatrix_encountered_values = defaultdict(list)
        visited = defaultdict(list)

        for i in range(len(board)):
            for j in range(len(board[i])):

                if board[i][j] == '.':
                    continue

                # if row_encountered_indexes[int(board[i][j])-1][i] == 1:
                #     print(f"{board[i][j]} was already seen at {i+1}")
                #     return False
                # else:
                #     row_encountered_indexes[int(board[i][j])-1][i] = 1

                # if column_encountered_indexes[int(board[i][j])-1][j] == 1:
                #     print(f"{board[i][j]} was already seen at {j+1}")
                #     return False
                # else:
                #     column_encountered_indexes[int(board[i][j])-1][j] = 1
                to_be_visited = {
                    # (int(board[i][j]), int(board[i][j])-1, i),
                    ('row', (int(board[i][j]), i)),
                    # (int(board[i][j]), j, int(board[i][j])-1)
                    ('col', (int(board[i][j]), j))
                }
                print(f"For {board[i][j]} at {i},{j} -> to be visited are {to_be_visited}")
                for loc, visiting in to_be_visited:
                    if visiting in visited[loc]:
                        print(f"{visiting} was already visited!")
                        return False
                    else:
                        print(f"Visiting {visiting}!")
                        visited[loc].append(visiting)

                subMatrixId = get_sub_matrix_id(i, j)
                if board[i][j] in subMatrix_encountered_values[subMatrixId]:
                    print(f"{board[i][j]} in {subMatrix_encountered_values[subMatrixId]} for {subMatrixId}")
                    return False
                
                else:
                    subMatrix_encountered_values[subMatrixId].append(board[i][j])
                    print(f"Added {board[i][j]} for {subMatrixId} making it {subMatrix_encountered_values[subMatrixId]}")

        return True

if __name__ == "__main__":
    input_board = [[".","8","7","6","5","4","3","2","1"],["2",".",".",".",".",".",".",".","."],["3",".",".",".",".",".",".",".","."],["4",".",".",".",".",".",".",".","."],["5",".",".",".",".",".",".",".","."],["6",".",".",".",".",".",".",".","."],["7",".",".",".",".",".",".",".","."],["8",".",".",".",".",".",".",".","."],["9",".",".",".",".",".",".",".","."]]
    Solution().print_matrix(input_board)

    print(Solution().isValidSudoku(input_board))
