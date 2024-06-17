import time

def check(N):
    while N >= 2020:
        if (N % 2020 == 0) or (N % 2021 == 0):
            return True
        else:
            return (check(N - 2020) or check(N - 2021))
    return False


def possibility(N):    
    if ((int("".join(list(str(N))[:-3]))*1000) % 2000 == 0) and ((int("".join(list(str(N))[:-3]))*1000) // 2000) >= (N % 2020):
        return True
    else:
        return False


def main(T, N):
    #T = int(input())
    t1 = time.time()

    for i in range(T):
        #N = int(input())

        if N[i] < 2020:
            #print("NO")
            continue
        elif possibility(N[i]):
            print("In Possible")
            if check(N[i]):
                print("YES")
            # else:
            #     print("NO") 
            #print(possibility(N), N, check(N))
        else:
            #print("NO")
            continue
    print("Time Taken: ", (time.time() - t1))


if __name__ == "__main__":
    T = 10000
    N = [i for i in range(T)]
    main(T, N)
