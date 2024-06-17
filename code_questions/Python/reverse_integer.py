"""
https://leetcode.com/problems/reverse-integer/
"""
import math

class Solution:
    def reverse(self, x: int) -> int:
        maximum = 2 ** 31
        
        """ Apporach 1 """
        # if x >= 0:
        #     output = int(''.join(reversed(list(str(x)))))

        # else:
        #     output = -int(''.join(reversed(list(str(abs(x))))))

        """ 
        Approach 2:
        123, 0 ==>
        123 % 10 = 3
        = (3+0)*10
        = (123 - 3) % 10
        12, 30 ==>
        120 % 10 = 2        
        = (30+2)*10 = 320
        = (12-2)%10
        1, 320 ==>
        = 320 + 1
        """
        output, is_negative = 0, True if x < 0 else False
        x = abs(x)
        while True:

            temp = x % 10
            
            x -= temp
            x //= 10

            if x == 0:
                output += temp
                break

            else:
                output += temp
                output *= 10

        if abs(output) >= maximum:
            return 0
        return -output if is_negative else output

sol = Solution()
print(sol.reverse(int(input())))
