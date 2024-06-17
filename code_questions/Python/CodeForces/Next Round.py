n, k = list(map(int, input().split()))
scores = list(map(int, input().split()))

i, cnt = 0, 0
while i < len(scores):
    if scores[i] > 0:
        if cnt < k:
            cnt = cnt + 1
        else:
            if scores[i] == scores[i - 1]:
                cnt = cnt + 1
            else:
                break
    else:
        break
    i = i + 1
   
print(cnt)

