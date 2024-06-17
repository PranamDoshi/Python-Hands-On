n = int(input())

forces = []
for i in range(n):
    forces.append(list(map(int, input().split())))

equi = []
for d in range(3):
    sum = 0
    for a in range(n):
        sum += forces[a][d]
    equi.append(sum)

if len([e for e in equi if e != 0]) != 0:
    print('NO')
else:
    print('YES')