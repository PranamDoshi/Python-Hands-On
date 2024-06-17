class SearchMatrix:

    def searchMatrix(self, matrix, target):
        """
        Matrix Properties:
        Integers in each row are sorted in ascending from left to right.
        Integers in each column are sorted in ascending from top to bottom.
        """
        for i in range(len(matrix)):
            if BinarySearchIterative(matrix[i], target):
                return True
        
        return False
        

def BinarySearchIterative(nums, target):
    """
    Iterative Algorithm
    """
    start, end = 0, len(nums) - 1

    while start <= end:
        mid = start + ((end - start) // 2)

        if nums[mid] == target:
            return True
        elif nums[mid] < target:
            start = mid + 1
        elif nums[mid] > target:
            end = mid - 1
        
    return False

if __name__ == "__main__":
    sol = SearchMatrix()

    matrix = []
    n = int(input())
    for i in range(n):
        matrix.append(list(map(int, input().split())))
    target = int(input())
    
    print(sol.searchMatrix(matrix, target))