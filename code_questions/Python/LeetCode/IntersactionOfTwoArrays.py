class Solution:

    def intersect(self, nums1, nums2):
        counterNums1 = {}
        counterNums2 = {}

        for i in nums1:
            if i in counterNums1:
                counterNums1[i] += 1
            else:
                counterNums1[i] = 1
        for i in nums2:
            if i in counterNums2:
                counterNums2[i] += 1
            else:
                counterNums2[i] = 1
        
        commonElements = []
        for key, value in counterNums1.items():
            if key in counterNums2:
                commonElements.extend([key]*min(counterNums1[key], counterNums2[key]))
        
        return commonElements


if __name__ == "__main__":
    sol = Solution()

    nums1 = list(map(int, input().split()))
    nums2 = list(map(int, input().split()))

    print(sol.intersect(nums1, nums2))