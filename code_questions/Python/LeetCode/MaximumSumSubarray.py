import time

class Solution:

    def maxSubArray(self, nums):
        # maxSum = -99999999
        # sumsArray = []
        # sum = 0

        # for value in nums:
        #     sum += value
        #     if sum > maxSum:
        #         maxSum = sum
        #     sumsArray.append(sum)

        # for i in range(1, len(nums)):
        #     for j in range(i, len(nums)):
        #         sum = sumsArray[j] - sumsArray[i - 1]
        #         if sum > maxSum:
        #             maxSum = sum
        
        # return maxSum

        #           OR

        # sum = 0

        # for value in nums:
        #     if value > 0:
        #         sum += value
        
        # return sum

        #           OR

        cur, ans, maxNum = 0, 0, nums[0]
        
        for i in range(len(nums)):
            cur = max(cur + nums[i], nums[i])
            ans = max(cur, ans)
            if nums[i] > maxNum:
                maxNum = nums[i]
        
        return ans or maxNum

if __name__ == "__main__":
    inputArray = list(map(int, input().split()))
    sol = Solution()
    t1 = time.time()
    print(sol.maxSubArray(inputArray))
    #print(time.time() - t1)
