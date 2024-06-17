from collections import defaultdict

class Solution:

    def isValidSudoku(self, board):
        AreawiseCount = defaultdict(list)
        colwiseCount = defaultdict(list)
        rowwiseCount = defaultdict(list)

        for i in range(9):
            for j in range(9):
                if board[i][j] != '.':
                    if board[i][j] not in AreawiseCount[createKey(i, j)]:
                        AreawiseCount[createKey(i, j)].append(board[i][j])
                    else:
                        return False
                    if board[i][j] not in colwiseCount[j]:
                        colwiseCount[j].append(board[i][j])
                    else:
                        return False
                    if board[i][j] not in rowwiseCount[i]:
                        rowwiseCount[i].append(board[i][j])
                    else:
                        return False
        
        return True


def createKey(rowIdx, colIdx):
    if rowIdx < 3:
        if colIdx < 3:
            return 0
        elif colIdx > 2 and colIdx < 6:
            return 3
        else:
            return 6
    elif rowIdx > 2 and rowIdx < 6:
        if colIdx < 3:
            return 1
        elif colIdx > 2 and colIdx < 6:
            return 4
        else:    
            return 7
    else:
        if colIdx < 3:
            return 2
        elif colIdx > 2 and colIdx < 6:
            return 5
        else:
            return 8

if __name__ == "__main__":
    sol = Solution()

    board = []
    for i in range(9):
        board.append(list(input().split(',')))
    
    print(sol.isValidSudoku(board))