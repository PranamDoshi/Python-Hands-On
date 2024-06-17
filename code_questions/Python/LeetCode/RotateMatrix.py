class RotateMatrix:

    def rotate(self, matrix):
        # ansMatrix = []
        # for i in range(len(matrix[0])):
        #     reversedCol = []
        #     for j in range(-1, -len(matrix) - 1, -1):
        #         reversedCol.append(matrix[j][i])
        #     ansMatrix.append(reversedCol)
        
        # #print(ansMatrix)
        # matrix = ansMatrix

        N = len(matrix)
        for i in range((N+1)//2):
            for j in range(N//2):
                a1,b1 = i, j
                a2,b2 = j, -i-1
                a3,b3 = -i-1, -j-1
                a4,b4 = -j-1, i
                
                matrix[a1][b1], matrix[a2][b2], matrix[a3][b3], matrix[a4][b4] = matrix[a4][b4], matrix[a1][b1], matrix[a2][b2], matrix[a3][b3]
                print(matrix)


if __name__ == "__main__":
    sol = RotateMatrix()
    
    n = int(input())
    matrix = []
    for i in range(n):
        matrix.append(list(map(int, input().split())))
    
    sol.rotate(matrix)

    print(matrix)