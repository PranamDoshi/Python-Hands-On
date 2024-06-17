T = int(input())

def findMinCov(segments):
    start = 0
    end = 0
    cov = 0
    for i in range(len(segments)):
        if i == 0:
            end = segments[i]
            cov = end

for i in range(T):
    n = int(input())
    segments = list(map(int, input().split()))
    print(findMinCov(segments))