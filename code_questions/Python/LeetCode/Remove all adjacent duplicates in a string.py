class KAdjacentDuplicates:

    def RemoveFromString(self, s, k):
        uniqueChar = set(s)
        newString = s[:]
        
        while s:
            # leftPoint, rightPoint = 0, k

            # while rightPoint <= len(s):
            #     if s[leftPoint:rightPoint] == s[leftPoint]*k:
            #         s = s.replace(s[leftPoint]*k, '')
            #     leftPoint += 1
            #     rightPoint += 1

            for chr in uniqueChar:
                s = s.replace(chr*k, '')

            if newString == s:
                break
            newString = s
            
        return s

    def RemoveFromString(self, s, k):
        CharCounter = []

        for chr in s:
            if CharCounter and CharCounter[-1][0] == chr:
                CharCounter[-1][1] += 1

                if CharCounter[-1][1] == k:
                    CharCounter.pop()
            else:
                CharCounter.append([chr, 1])
        
        ansString = ''
        for pair in CharCounter:
            ansString += pair[0]*pair[1]
        
        return ansString


if __name__ == "__main__":
    sol = KAdjacentDuplicates()

    s = input()
    k = int(input())

    print(sol.RemoveFromString(s, k))