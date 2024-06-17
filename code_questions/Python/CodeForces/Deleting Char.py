inp = list(input())
cnt = 0

for i in range(len(inp) - 1):
    if inp[i] == inp[i + 1]:
        cnt = cnt + 1

print(cnt)
