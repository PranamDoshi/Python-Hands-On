s = int(input())
x = 0

for i in range(s):
    op = input()
    if op.find('+') >= 0:
        x = x + 1
    elif op.find('-') >= 0:
        x = x - 1

print(x)
