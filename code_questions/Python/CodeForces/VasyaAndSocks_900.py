def main():
    n, m = list(map(int, input().split()))
    days = 0

    while n:
        days += 1
        n -= 1
        if days % m == 0:
            n += 1
    
    print(days)


if __name__ == "__main__":
    main()