N = int(input())

def checkNulity(Strng):
    if len([c for c in strng if c == 'B']) == (len(strng) / 2):
        return True
    return False

for i in range(N):
    strng = list(input())
    if checkNulity(strng):
        print('YES')
    else:
        print('NO')