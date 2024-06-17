class ZeroOneMatrix:

    def updateMatrix(self, mat):
        x = 0         


if __name__ == "__main__":
    sol = ZeroOneMatrix()

    numRows = int(input())
    mat = []
    for i in range(numRows):
        mat.append(list(map(int, input().split())))

    for row in mat:
        print(' '.join(map(str, row)))

    for row in sol.updateMatrix(mat):
        print(' '.join(map(str, row)))