class SmallestSubsequence:

    def smallestSubsequence(self, s):
        # AllElements, idx = set(s), 0
        # ansFrame = ''

        # while idx <= len(s) - len(AllElements):
        #     frame = ''.join(s[idx:idx+len(AllElements)])
        #     print(frame, ansFrame)
        #     tempFlag = True
        #     for element in AllElements:
        #         if element not in frame:
        #             tempFlag = False
            
        #     if tempFlag and len(ansFrame) and frame < ansFrame:
        #         ansFrame = frame
        #     elif tempFlag and not len(ansFrame):
        #         ansFrame = frame
            
        #     idx += 1

        # return ansFrame

        AllElements, lastIndex = set(s), {}

        for idx in range(len(s)):
            lastIndex[s[idx]] = idx
        
        ansFrame = ''

        print(lastIndex)
        stack = []
        for idx in range(len(s)):
            print(stack, s[idx], idx)
            if s[idx] in stack:
                continue

            while stack and stack[-1] > s[idx] and lastIndex[stack[-1]] > idx:
                stack.pop()
            
            stack.append(s[idx])
            
            if len(stack) == len(AllElements):
                if (len(ansFrame) and ansFrame > ''.join(stack)) or (not len(ansFrame)):
                    ansFrame = ''.join(stack)

        return ansFrame


if __name__ == "__main__":
    sol = SmallestSubsequence()

    s = input()

    print(sol.smallestSubsequence(s))