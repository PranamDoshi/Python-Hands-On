from itertools import combinations

class LargestPerimeter:

    def largestPerimeter(self, nums):
        nums = list(reversed(sorted(nums)))

        for i in range(len(nums) - 2):
            if nums[i + 2] + nums[i + 1] > nums[i]:
                return nums[i + 2] + nums[i + 1] + nums[i]

        return 0
    

if __name__ == "__main__":
    sol = LargestPerimeter()

    nums = list(map(int, input().split()))

    print(sol.largestPerimeter(nums))