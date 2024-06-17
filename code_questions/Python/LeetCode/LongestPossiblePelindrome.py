from collections import defaultdict

class LongetsPelindrom:

    def longestPalindrome(self, s):
        charCounter = defaultdict(int)
        maxLength, SingleCharAvailable = 0, False

        for chr in s:
            charCounter[chr] += 1
        
        for chr, count in charCounter.items():
            if count > 1:
                if count & 1:
                    charCounter[chr] = 1
                    SingleCharAvailable = True
                    maxLength += count - 1
                else:
                    maxLength += count
            else:
                SingleCharAvailable = True
        
        if SingleCharAvailable:
            return maxLength + 1
        else:
            return maxLength            

    def longestPalidromicsubString(self, s):
        """
        https://www.youtube.com/watch?v=XYQecbcd6_c
        """
        ans, maxLength = '', 0

        for idx in range(len(s)):
            left, right = idx, idx
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if (right - left + 1) > maxLength:
                    ans = s[left:right + 1]
                    maxLength = right - left + 1
                left -= 1
                right += 1
            
            left, right = idx, idx + 1
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if (right - left + 1) > maxLength:
                    ans = s[left:right + 1]
                    maxLength = right - left + 1
                left -= 1
                right += 1
        
        return ans


if __name__ == "__main__":
    sol = LongetsPelindrom()

    s = input()

    print(sol.longestPalindrome(s))

    print(sol.longestPalidromicsubString(s))