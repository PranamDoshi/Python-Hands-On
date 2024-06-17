import sortedcontainers as sc

class Solution:

    def containsDuplicate(self, nums):
        counterDict = {}

        for value in nums:
            if value in counterDict:
                return 'true'
            else:
                counterDict[value] = 1
        return 'false'

        #           OR
        """
        if len(set(nums)) != len(nums):
            return True
        else:
            return False
        """

    def containsNearbyDuplicate(self, nums, k):
        counterDict = {}

        if len(set(nums)) == len(nums):
            return False

        for idx, value in enumerate(nums):
            if value in counterDict:
                if abs(counterDict[value] - idx) <= k:
                    return True
            counterDict[value] = idx
        return False

    def containsNearbyAlmostDuplicate(self, nums, t, k):
        s = sc.SortedSet([])
        
        for idx, num in enumerate(nums):
            
            if list(s.irange(num - t, num + t)):
                print(s, num - t, num + t)
                return True
            
            s.add(num)
            if len(s) > k:
                s.remove(nums[idx - k])
                    
        return False
    
if __name__ == "__main__":
    sol = Solution()

    inputList = list(map(int, input().split()))
    k, t = list(map(int, input().split()))
    
    print(sol.containsNearbyAlmostDuplicate(inputList, t, k))
