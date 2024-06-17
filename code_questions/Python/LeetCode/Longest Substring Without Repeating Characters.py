from collections import defaultdict

class WithoutRepeatingLetters:

    def lengthOfLongestSubstring(self, s):
        def defaultIndex():
            return -1

        maxLength, tempStr = 0, ''
        lastIndex = defaultdict(defaultIndex)

        for i in range(len(s)):
            if s[i] in tempStr:
                tempStr = s[lastIndex[s[i]] + 1:i + 1]
            else:
                tempStr += s[i]
                if len(tempStr) > maxLength:
                    maxLength = len(tempStr)

            lastIndex[s[i]] = i
            #print(tempStr, lastIndex, i, s, maxLength)
        
        return maxLength


if __name__ == "__main__":
    sol = WithoutRepeatingLetters()

    s = input()

    print(sol.lengthOfLongestSubstring(s))