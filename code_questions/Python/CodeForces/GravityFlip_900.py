import time

def main():
    N = int(input())
    input_arr = list(map(int, input().split()))

    t1 = time.time()
    for i in range(N):
        max, max_idx, shift = 0, -1, -1
        for j in range(i, N):
            if input_arr[j] < input_arr[i]:
                #print(min, shift, input_arr)
                if (input_arr[i] - input_arr[j]) > max:
                    shift = input_arr[i] - input_arr[j]
                    max = shift
                    max_idx = j
            else:
                j = N
        
        if shift != -1:
            input_arr[i] -= shift
            input_arr[max_idx] += shift
    
    print("Time Taken: %.5f" % (time.time() - t1))

    print(*input_arr)


if __name__ == "__main__":
    main()
