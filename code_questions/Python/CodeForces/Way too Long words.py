def create_abr(longString):
    abr = str(longString[0]) + str((len(longString) - 2)) + str(longString[len(longString) - 1])
    print(abr)

n = int(input())
for i in range(n):
    longString = input()
    if(len(longString) > 10):
        create_abr(longString)
    else:
        print(longString)
