def IfGrowth(arr, idx, n):
    end = idx + 1
    cur = idx
    length = 1

    while arr[end] >= arr[cur]:
        end += 1
        cur += 1
        length += 1
        
        if end == n:
            break

    return length, end


def LongestGrowth(arr, n):
    maxGrowth = 1
    startIdx = 0

    while True:
        if startIdx >= (n - 1):
            break

        thisGrowth, endIndex = IfGrowth(arr, startIdx, n)
        if  thisGrowth > maxGrowth:
            maxGrowth = thisGrowth
        startIdx = endIndex

       
    
    return maxGrowth


def main():
    N = int(input())
    incomes = list(map(int, input().split()))
    assert N == len(incomes)

    print(LongestGrowth(incomes, N))


if __name__ == "__main__":
    main()