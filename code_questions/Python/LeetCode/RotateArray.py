class RotateArray:

    def rotate(self, nums, k):
        tempNum = nums[0]
        nums[0] = 'start'
        idx = 0
        idx = (idx + k) % len(nums)
        while nums[idx] != 'start':
            print(nums, tempNum, idx)
            tempNum, nums[idx] = nums[idx], tempNum
            idx = (idx + k) % len(nums)
        nums[idx] = tempNum

if __name__ == '__main__':
    sol = RotateArray()

    # nums = [1, 2, 3, 4, 5, 6, 7]
    # k = 3
    nums = list(map(int, input().split()))
    k = int(input())

    sol.rotate(nums, k)
    print(nums)