from multiprocessing.connection import answer_challenge
from numpy import character


class Solution:

    def firstUniqueChar(self, s):
        characterCount = {}
#        ansIdx = 0
        
        for i in range(len(s)):
            if s[i] in characterCount:
                characterCount[s[i]] += 1
            else:
                characterCount[s[i]] = 1
            
            # if characterCount[s[ansIdx]] > 1:
            #     ansIdx += 1

        for idx, chr in enumerate(list(s)):
            if characterCount[chr] == 1:
                return idx
        
        return -1
        # if ansIdx >= len(s):
        #     return -1
        # else:
        #     return ansIdx


if __name__ == "__main__":
    sol = Solution()

    s = input()

    print(sol.firstUniqueChar(s))