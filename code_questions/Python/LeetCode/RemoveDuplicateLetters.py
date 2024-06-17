class RemoveDuplicates:

    def removeDuplicateLetters(self, s):
        lastIdx = {}
        stack = []
        visited = set()

        for i in range(len(s)):
            lastIdx[s[i]] = i
        
        for i in range(len(s)):
            if s[i] not in visited:
                while (stack and stack[-1] > s[i]) and lastIdx[stack[-1]] > i:
                    visited.remove(stack.pop())
                
                stack.append(s[i])
                visited.add(s[i])
            
            # print(s[i])
            # print(''.join(stack))
            # print(visited)
        
        return ''.join(stack)


if __name__ == '__main__':
    sol = RemoveDuplicates()

    s = input()

    print(sol.removeDuplicateLetters(s))