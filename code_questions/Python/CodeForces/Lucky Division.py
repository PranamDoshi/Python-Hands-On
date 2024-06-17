N = int(input())

divd = [4, 7, 47, 74, 444, 447, 474, 744, 477, 747, 774, 777]

str_N = list(str(N))
f = False

if len([n for n in str_N if n not in ('4', '7')]) == 0:
    print('YES')
else:
    for d in divd:
        if d < N and N % d == 0:
            print('YES')
            f = True
            break
    if not f:
        print('NO')