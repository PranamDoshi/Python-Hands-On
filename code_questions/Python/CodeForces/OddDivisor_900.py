def main():
    T = int(input())

    for i in range(T):
        N = int(input())

        while not N & 1:
            N >>= 1
        
        if N == 1:
            print("NO")
        else:
            print("YES")


def codeForcesSolution():
    T = int(input())

    for i in range(T):
        N = int(input())

        if N & (N - 1):
            print("YES")
        else:
            print("NO")


if __name__ == "__main__":
    main()
    #codeForcesSolution()