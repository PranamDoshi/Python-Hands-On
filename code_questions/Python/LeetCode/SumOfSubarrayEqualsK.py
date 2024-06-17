from collections import defaultdict

class SubArraySum:

    def subarraySum(self, nums, k):
        increasingSum, ansCount = 0, 0
        seenSums = defaultdict(int)
        seenSums[0] = 1

        for n in nums:
            increasingSum += n

            if seenSums[increasingSum - k]:
                ansCount += seenSums[increasingSum - k]
            
            seenSums[increasingSum] += 1

            #print(seenSums, increasingSum, ansCount)
        
        return ansCount


if __name__ == "__main__":
    sol = SubArraySum()

    nums = list(map(int, input().split()))
    k = int(input())

    print(sol.subarraySum(nums, k))