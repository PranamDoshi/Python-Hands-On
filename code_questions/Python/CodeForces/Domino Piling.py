m, n = list(map(int, input().split()))

if n % 2 == 0:
    cnt = (n // 2) * m
else:
    temp = (n // 2) * m
    cnt = temp + (m // 2)    

print(cnt)
