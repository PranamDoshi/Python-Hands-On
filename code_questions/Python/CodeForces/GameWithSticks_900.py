def main():
    m, n = list(map(int, input().split()))

    turn = 0
    
    if m <= n:
        if m % 2 == 0:
            turn = 0
        else:
            turn = 1
    else:
        if n % 2 == 0:
            turn = 0
        else:
            turn = 1

    if turn == 0:
        print("Malvika")
    else:
        print("Akshat")


if __name__ == "__main__":
    main()