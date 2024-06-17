#import numpy as np

arr = []
for idx in range(5):
    arr.append(list(map(int, input().split())))
#array = np.array(arr)

#i, j = np.where(array == 1)

for idx in range(5):
    for idy in range(5):
        if arr[idx][idy] == 1:
            i, j = idx, idy
    
cnt = abs(2 - i) + abs(2 - j)
print(cnt)
