class ArrayProduct:

    def productExceptSelf(self, nums):
        # zeros - counts number of zeros
        prod, zeros = 1, 0
        for i in range(len(nums)):
            if not nums[i]:
                zeros += 1
            else:
                prod *= nums[i]

        # return all zeros array if there are more than 1 zeros
        if zeros > 1:
            return [0]*len(nums)

        for i in range(len(nums)):
            if not nums[i]:
                nums[i] = prod
            elif zeros:
                nums[i] = 0
            else:
                nums[i] = int(prod / nums[i])
        
        return nums

    def productExceptSelf(self, nums):
        productsBeforeIdx, productsAfterIdx = [0]*len(nums), [0]*len(nums)
        prodBeforeIdx, prodAfterIdx = 1, 1

        for i in range(len(nums)):
            prodBeforeIdx *= nums[i]
            productsBeforeIdx[i] = prodBeforeIdx
            prodAfterIdx *= nums[len(nums) - 1 - i]
            productsAfterIdx[len(nums) - 1 -i] = prodAfterIdx

        for j in range(len(nums)):
            if not j:
                nums[j] = productsAfterIdx[j+1]
            elif j == len(nums) - 1:
                nums[j] = productsBeforeIdx[j-1]
            else:
                nums[j] = productsBeforeIdx[j-1]*productsAfterIdx[j+1]
        
        return nums


if __name__ == "__main__":
    sol = ArrayProduct()

    nums = list(map(int, input().split()))

    print(sol.productExceptSelf(nums))