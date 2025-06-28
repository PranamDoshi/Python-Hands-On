"""
https://leetcode.com/problems/search-in-rotated-sorted-array/description/
"""
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            pass

if __name__ == "__main__":
    print(Solution().search([4,5,6,7,0,1,2], 0))
