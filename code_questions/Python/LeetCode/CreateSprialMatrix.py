class SpriralMatrix:

    def generateMatrix(self, n):
        """
        Generate Spiral matrix of n ✕ n
        1 2 3
        8 9 4
        7 6 5
        """
        ansMatrix = [[0] * n for i in range(n)]
        value = 1 

        for i in range(n // 2 + 1):
            offset = n - 1 - i*2

            for j in range(i, n - 1 - i):
                ansMatrix[i][j] = value
                ansMatrix[j][n - 1 - i] = value + offset
                ansMatrix[n - 1 - i][n - 1 - j] = value + offset * 2
                ansMatrix[n - 1 - j][i] = value + offset * 3
                value += 1
            
            value += offset * 3

            if n & 1 and n // 2 == i:
                ansMatrix[i][i] = value
          
        return ansMatrix


if __name__ == "__main__":
    sol = SpriralMatrix()

    n = int(input())

    ansMatrix = sol.generateMatrix(n)
    for row in ansMatrix:
        print(' '.join(list(map(str, row))), end = '\n')