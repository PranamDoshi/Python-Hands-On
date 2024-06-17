from math import ceil

class Solution:

    def searchMatrix(self, matrix, target):
        tempArr = []
        for row in matrix:
            tempArr.extend(row)
        
        return binarySearch(tempArr, 0, len(matrix)*len(matrix[0]), target)


class Solution1:

    def searchMatrix(self, matrix, target):
        start, end = 0, len(matrix) - 1

        while start < end:
            mid = start + ceil((end - start) / 2)

            if matrix[mid][0] == target:
                return True
            elif matrix[mid][0] < target:
                start = mid
            else:
                end = mid - 1
        
        targetRow = end
        start, end = 0, len(matrix[0])

        while start < end:
            mid = start + ((end - start) >> 1)

            if matrix[targetRow][mid] == target:
                return True
            elif matrix[targetRow][mid] < target:
                start = mid + 1
            else:
                end = mid
        
        return False

def binarySearch(matrix, start, end, target):
    if end >= start:
        mid = start + ((end - start) // 2)
        
        if matrix[mid] == target:
            return True
        elif matrix[mid] < target:
            return binarySearch(matrix, mid + 1, end, target)
        else:
            return binarySearch(matrix, start, mid - 1, target)

    else: 
        return False

if __name__ == "__main__":
    sol = Solution1()

    n = int(input())
    matrix = []
    for i in range(n):
        matrix.append(list(map(int, input().split())))
    target = int(input())
    
    print(sol.searchMatrix(matrix, target))