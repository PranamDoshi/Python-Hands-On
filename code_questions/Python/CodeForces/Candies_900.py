def generateK():
    k = 0
    totalK = 0

    while True:
        totalK += (2 ** k)
        k += 1

        yield totalK


def main():
    T = int(input())

    for i in range(T):
        N = int(input())
        foundK = False

        gen = generateK()
        while True:
            tempK = next(gen)
            
            if list(str(N/tempK))[-1] == '0':
                x = N/tempK
                if tempK != 1:
                    foundK = True
                #print(x, tempK)
            elif foundK:
                #print(x, tempK)
                break

        print(int(x))


if __name__ == "__main__":
    main()