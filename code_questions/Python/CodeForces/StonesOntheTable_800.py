def main():
    N = int(input())
    inputArr = list(input())
    assert N == len(inputArr)
    count = 0

    for i in range(N - 1):
        #print(i, inputArr)
        if inputArr[i] == inputArr[i + 1]:
            #inputArr.pop(i)
            count += 1
    
    print(count)


if __name__ == "__main__":
    main()