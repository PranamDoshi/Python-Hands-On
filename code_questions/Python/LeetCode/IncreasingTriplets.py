class IncreasingTriplets:

    def exists(self, nums):
        kValues, iValues = [nums[-1]], [nums[0]]
        # kIdx, iIdx, Idx = list(range(-2, -len(nums) - 1, -1)), list(range(1, len(nums))), list(range(1, len(nums) - 1))

        for i in range(-2, -len(nums) - 1, -1):
            kValues.append(max(kValues[-1], nums[i]))
        kValues = list(reversed(kValues))

        for i in range(1, len(nums)):
            iValues.append(min(nums[i], iValues[-1]))
            if nums[i] > iValues[i] and nums[i] < kValues[i]:
                return True

        # for iIdx, kIdx, Idx in zip(iIdx, kIdx, Idx):
        #     kValues.append(max(kValues[-1], nums[kIdx]))
        #     iValues.append(min(iValues[-1], nums[iIdx]))
        #     print(iValues, kValues, iIdx, kIdx, Idx, nums)
        #     if nums[Idx] > iValues[-1] and nums[Idx] < kValues[-1]:
        #         return True

        return False
    

if __name__ == "__main__":
    sol = IncreasingTriplets()

    nums = list(map(int, input().split()))

    print(sol.exists(nums))