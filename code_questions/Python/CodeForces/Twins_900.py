def findMinimumReq(arr, n):
    my_half = 0
    other_half = sum(arr, 0)
    #print(other_half)
    numberOfcoins = 0
    idx = -1
    #dict = {}

    # for i in range(n):
    #     if arr[i] in dict.keys():
    #         dict[arr[i]] += 1
    #     else:
    #         dict[arr[i]] = 1
    while my_half <= other_half and abs(idx) <= n:
        my_half += arr[idx]
        other_half -= arr[idx]
        numberOfcoins += 1
        idx -= 1

    return numberOfcoins


def main():
    N = int(input())
    input_coins = list(map(int, input().split()))
    assert N == len(input_coins)

    print(findMinimumReq(sorted(input_coins), N))


if __name__ == "__main__":
    main()