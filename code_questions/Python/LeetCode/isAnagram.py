import time
from collections import defaultdict, Counter


class Solution:

    def isAnagram(self, s, t):
        if len(s) != len(t):
            return False
        else:
            sChrCount = defaultdict(int)
            tChrCount = defaultdict(int)
            tempIdx = 0

            for chr in s:
                sChrCount[chr] += 1
            
            for chr in t:
                tChrCount[chr] += 1
            
            for chr in t:
                if sChrCount[chr] == tChrCount[chr]:
                    tempIdx += 1
            
            if tempIdx == len(s):
                return True
            else:
                return False

    def isAnagramOneLineSol(self, s, t):
        #return Counter(s) == Counter(t)

                # OR

        sChrCount = defaultdict(int)
        tChrCount = defaultdict(int)

        for chr in s:
            sChrCount[chr] += 1
        
        for chr in t:
            tChrCount[chr] += 1
        
        return sChrCount == tChrCount


if __name__ == "__main__":
    sol = Solution()

    s = input()
    t = input()

    t1 = time.time()
    print(sol.isAnagram(s, t))
    print('%.5f' % (time.time() - t1))

    t1 = time.time()
    print(sol.isAnagramOneLineSol(s, t))
    print('%.5f' % (time.time() - t1))