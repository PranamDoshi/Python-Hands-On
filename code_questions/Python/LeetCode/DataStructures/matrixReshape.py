import numpy as np
from itertools import chain


class Solution:

    def matrixReshape(self, mat, r, c):
        if len(mat)*len(mat[0]) == r * c:
            reshapedMat = []
            ridx, cidx = 0, 0
            m, n = 0, 0
            print(m, n)
            while ridx < r:
                tempArr = []
                
                while cidx < c:
                    tempArr.append(mat[m][n])
                    if n < len(mat[0]) - 1:
                        n += 1
                    else:
                        n = 0
                        m += 1
                    cidx += 1
                    print(tempArr, ridx, cidx, m, n)
                
                reshapedMat.append(tempArr)
                ridx += 1
                cidx = 0  

            return reshapedMat
        else:
            return mat


class Solution1:

    def matrixReshape(self, mat, r, c):
        ArrayMat = np.array(mat)
        if ArrayMat.shape[0] * ArrayMat.shape[1] == r * c:
            ArrayMat = ArrayMat.reshape(r, c)

            return ArrayMat
        else:
            return mat


class Solution2:

    def matrixReshape(self, mat, r, c):
        if len(mat) * len(mat[0]) == r * c:
            reshapedArr = []

            flatMat = []
            for i in range(len(mat)):
                for j in range(len(mat[0])):
                    flatMat.append(mat[i][j])

            for i in range(r):
                temp = []
                for j in range(c):
                    temp.append(flatMat.pop(0))
                reshapedArr.append(temp)

            return reshapedArr
        else:
            return mat


class Solution4:

    def matrixReshape(self, mat, r, c):
        if len(mat) * len(mat[0]) == r * c:
            reshapedArr = []

            mat = list(chain(*mat))
            for i in range(0, len(mat)*len(mat[0]), c):
                reshapedArr.append(mat[i : i + c])

            return reshapedArr
        else:
            return mat



if __name__ == "__main__":
    sol = Solution2()

    m, n = map(int, input().split())
    mat = []
    for i in range(m):
        mat.append(list(map(int, input().split())))
    r, c = map(int, input().split())

    print(sol.matrixReshape(mat, r, c))