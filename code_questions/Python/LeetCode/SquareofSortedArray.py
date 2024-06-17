import time

class SortedSqaures:

    def sortedSquares(self, nums):
        tempIdx = -1
        for i in range(len(nums)):
            if nums[i] >= 0 and tempIdx == -1:
                tempIdx = i
            nums[i] = nums[i] ** 2
        
        if tempIdx > 0:
            tempArr = list(reversed(nums[:tempIdx]))
            nums = nums[tempIdx:]

            tempIdx, Idx = 0, 0

            while tempIdx < len(tempArr) and Idx < len(nums):
                if nums[Idx] <= tempArr[tempIdx]:
                    Idx += 1
                else:
                    nums.insert(Idx, tempArr[tempIdx])
                    tempIdx += 1
                
            while tempIdx < len(tempArr):
                nums.append(tempArr[tempIdx])
                tempIdx += 1
        elif tempIdx == -1:
            return list(reversed(nums))

        return nums


if __name__ == '__main__':
    sol = SortedSqaures()

    #nums = list(map(int, input().split()))
    nums = [i for i in range(-10000, 10001)]

    t1 = time.time()
    #print(sol.sortedSquares(nums))
    ans1 = sol.sortedSquares(nums)
    print('%.6f' % (time.time() - t1))

    t1 = time.time()
    for i in range(len(nums)):
        nums[i] **= 2
    ans2 = sorted(nums)
    print('%.6f' % (time.time() - t1))