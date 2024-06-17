def KthNum(n, k):
    if n % 2 == 0:
        if k > (n /2):
            return 2*(k - (n/2))
        else:
            return (2*k) - 1
    else:
        if k > ((n+1)/2):
            return 2*(k - ((n+1)/2))
        else:
            return (2*k) - 1


def main():
    N, k = list(map(int, input().split()))

    print(int(KthNum(N, k)))


if __name__ == "__main__":
    main()