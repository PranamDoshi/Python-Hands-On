class ThreeSum:

    def threeSum(self, nums):
        """
        return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
        """
        nums.sort()
        ansElements = set()
        for i in range(len(nums) - 2):
            if not i and nums[i] > 0:
                return []
            elif i > 0 and nums[i] == nums[i - 1]:
                continue
            else:    
                left = i + 1
                right = len(nums) - 1

                while left < right:
                    sum = nums[i] + nums[left] + nums[right]
                    if sum == 0:
                        ansElements.add((nums[i], nums[left], nums[right]))
                        left += 1
                        right -= 1
                    elif sum < 0:
                        left += 1
                    elif sum > 0:
                        right -= 1
        
        return ansElements


if __name__ == "__main__":
    sol = ThreeSum()

    nums = list(map(int, input().split()))

    print(sol.threeSum(nums))
