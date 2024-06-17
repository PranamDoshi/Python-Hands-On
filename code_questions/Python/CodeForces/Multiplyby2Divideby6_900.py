def main():
    T = int(input())

    for i in range(T):
        N = int(input())
        stepCount = 0

        if N == 1:
            print(0)
            continue
        elif N % 3 != 0:
            print(-1)
            continue
        else:
            while N != 1:
                if N % 3 != 0:
                    stepCount = -1
                    break 
                elif N % 6 == 0:
                    N /= 6
                else:
                    N *= 2
                stepCount += 1
        
        print(stepCount)


def codeForcesSolution():
    T = int(input())

    for t in range(T):
        N = int(input())
        divisibleBy2Cnt = 0
        divisibleBy3Cnt = 0

        while N % 2 == 0:
            N /= 2
            divisibleBy2Cnt += 1
        while N % 3 == 0:
            N /= 3
            divisibleBy3Cnt += 1

        if N == 1 and divisibleBy2Cnt <= divisibleBy3Cnt:
            print(2*divisibleBy3Cnt - divisibleBy2Cnt)
        else:
            print(-1)


if __name__ == "__main__":
    main()