class SearchInsertPosition:

    def searchInsert(self, nums, target):
        start, end = 0, len(nums) - 1

        while start <= end:
            mid = start + ((end - start) // 2)

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                start = mid + 1
            elif nums[mid] > target:
                end = mid - 1
        
        return start


if __name__ == "__main__":
    sol = SearchInsertPosition()

    nums = list(map(int, input().split()))
    target = int(input())

    print(sol.searchInsert(nums, target))