"""
https://leetcode.com/problems/3sum-closest/
"""

class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:

        def sum_of_3(a, b, c):
            return a+b+c

        def how_close(current_sum, target):
            if target < 0:

                if current_sum < 0:
                    return target-current_sum if target < current_sum else current_sum-target

                return current_sum-target

            else:
                
                if current_sum < 0:
                    return target - current_sum

                return target-current_sum if target > current_sum else current_sum-target

        closest_sum = 9999999
        how_close_old = how_close(closest_sum, target)

        for index, pivot in enumerate(nums):

            for index_1, num1 in enumerate(nums):
                if index_1 <= index:
                    continue

                for index_2, num2 in enumerate(nums):
                    if index_2 <= index_1:
                        continue

                    current_sum = sum_of_3(pivot, num1, num2)
                    print(f"For {pivot}, {num1}, {num2} = {current_sum} >/</= {closest_sum}")

                    if current_sum == target:
                        return target

                    how_close_new = how_close(current_sum, target)
                    if how_close_new <= how_close_old:
                        closest_sum = current_sum
                        how_close_old = how_close_new
        
        return closest_sum

class Solution2:

    def threeSumClosest(self, nums: list[int], target: int) -> int:

        def sum_of_3(a, b, c):
            return a+b+c

        def how_close(current_sum, target):
            return abs(current_sum-target)
            # if target < 0:

            #     if current_sum < 0:
            #         return target-current_sum if target < current_sum else current_sum-target

            #     return current_sum-target

            # else:
                
            #     if current_sum < 0:
            #         return target - current_sum

            #     return target-current_sum if target > current_sum else current_sum-target

        nums = sorted(nums)
        closest_sum = 1e9
        how_close_old = how_close(closest_sum, target)

        for index in range(len(nums)):

            begin, end = index+1, len(nums)-1

            while begin < end:
                
                current_sum = sum_of_3(nums[index], nums[begin], nums[end])
                how_close_new = how_close(current_sum, target)

                if how_close_new <= how_close_old:
                    closest_sum = current_sum
                    how_close_old = how_close_new

                if current_sum == target:
                    return target
                
                elif current_sum < target:
                    begin += 1
                
                else:
                    end -= 1

        return closest_sum
