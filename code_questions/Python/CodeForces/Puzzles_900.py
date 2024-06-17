def main():
    n, m = list(map(int, input().split()))
    puzzles = sorted(list(map(int, input().split())))
    assert m == len(puzzles)

    minDiff = 9999
    
    for i in range(0, m - n + 1):
        if puzzles[i + n - 1] - puzzles[i] < minDiff:
            minDiff = puzzles[i + n - 1] - puzzles[i]

    print(minDiff)

    
if __name__ == "__main__":
    main()