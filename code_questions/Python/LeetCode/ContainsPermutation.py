from collections import defaultdict
from tabnanny import check

class ContainsPermutation:

    def checkInclusion(self, s1, s2):
        if len(s1) > len(s2):
            return False
        else:
            s1Counter, s2Counter = defaultdict(int), defaultdict(int)

            for chr in s1:
                s1Counter[chr] += 1
            for chr in s2[0:len(s1)]:
                s2Counter[chr] += 1

            for i in range(0, len(s2) - len(s1) + 1):
                checker = 0
                if i > 0:
                    # print(s2, i-1)
                    # print(s2, i + len(s2) - len(s1))
                    s2Counter[s2[i - 1]] -= 1
                    if s2Counter[s2[i - 1]] == 0:
                        s2Counter.pop(s2[i - 1])
                    s2Counter[s2[i + len(s1) - 1]] += 1
                    if s2Counter[s2[i + len(s1) - 1]] == 0:
                        s2Counter.pop(s2[i + len(s1) - 1])

                #print(i, s1Counter, s2Counter)

                for key, value in s1Counter.items():
                    if s2Counter[key] == value:
                        checker += 1
                
                if checker == len(s2Counter.keys()):
                    return True

            return False


if __name__ == "__main__":
    sol = ContainsPermutation()

    s1 = input()
    s2 = input()

    print(sol.checkInclusion(s1, s2))