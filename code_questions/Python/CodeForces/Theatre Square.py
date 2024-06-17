n, m, a = list(map(int, input().split()))

cnt = (m // a) + (((n // a) - 1) * (m // a))

if n % a != 0 and m % a != 0:
    cnt += 1
if n % a != 0:
    cnt += (m // a)
if m % a != 0:
    cnt += (n // a)

print(cnt)