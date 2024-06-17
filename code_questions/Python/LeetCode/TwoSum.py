class Solution:

    def twosum(self, nums, target):
        for i in range(len(nums)):
            try:
                temp = nums.index(target - nums[i])
            except ValueError:
                temp  = -1
            if temp != -1 and temp != i:
                return list([i, nums.index(target - nums[i])])


class Solution1:

    def twosum(self, nums, target):
        cacheMem = {}

        for i, value in enumerate(nums):
            if target - nums[i] in cacheMem:
                return [i, cacheMem[target - nums[i]]]
            else:
                cacheMem[value] = i


if __name__ == "__main__":
    sol = Solution1()

    nums = list(map(int, input().split()))
    target = int(input())
    
    print(sol.twosum(nums, target))