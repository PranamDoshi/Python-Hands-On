import time

class Solution:

    def maxProfitBruteForce(self, prices):
        """
        Only one buy and sell
        """
        if checkNonDecreasing(prices):
            return 0
        else:
            maximumProfit = 0
            for i in range(len(prices)):
                for j in range(i + 1, len(prices)):
                    if prices[j] - prices[i] > maximumProfit:
                        maximumProfit = prices[j] - prices[i]
        
        return maximumProfit


class Solution1:

    def maxProfit(self, prices):
        """
        Only one buy and sell
        """
        buyPriceIndex, sellPriceIndex = 0, 1
        maximumProfit = 0

        while sellPriceIndex < len(prices):
            currentProfit = prices[sellPriceIndex] - prices[buyPriceIndex]

            if prices[buyPriceIndex] < prices[sellPriceIndex]:
                maximumProfit = max(currentProfit, maximumProfit)
            else:
                buyPriceIndex = sellPriceIndex

            sellPriceIndex += 1

        return maximumProfit
    
    def maxProfitMultiBuySell(self, prices):
        """
        More than one buy and sell allowed
        """
        profit = 0
        buyPrice = prices[0]

        for p in prices:
            if p < buyPrice:
                buyPrice = p
            else:
                profit += (p - buyPrice)
                buyPrice = p
        
        return profit


if __name__ == "__main__":
    sol = Solution1()

    prices = list(map(int, input().split()))

    t1 = time.time()
    print(sol.maxProfitMultiBuySell(prices))
    print('%.8f' % (time.time() - t1))