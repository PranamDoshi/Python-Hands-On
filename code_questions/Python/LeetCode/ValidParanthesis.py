from turtle import st


class Solution:

    def isValid(self, s):
        stack = []
        bracketsToClose = {'(':')', '{':'}', '[':']'}

        for chr in s:
            if chr in ['{', '(', '[']:
                stack.append(chr)
            elif len(stack) and bracketsToClose[stack[-1]] == chr:
                stack.pop()
            else:
                return False
        
        return not stack


if __name__ == "__main__":
    sol = Solution()

    s = input()

    print(sol.isValid(s))