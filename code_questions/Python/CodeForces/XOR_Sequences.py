"""
https://codeforces.com/problemset/problem/1979/B
"""
from pprint import pprint

class Solution:

    def __init__(self):
        pass

    def read_input(self):
        """
        Sample:
        4
        0 1
        12 4
        57 37
        316560849 14570961

        returns:
        [(0, 1), (12, 4), (57, 37), (316560849, 14570961)]
        """
        num_test_cas = int(input())
        inputs = [tuple(map(int, input().split())) for _ in range(num_test_cas)]
        return inputs
    
    def xor(self, x, y):
        """
        Sample:
        x=6 (110), y=1 (001)
        returns:
        7 (111)
        """
        # return x ^ y
        return f"{bin(x)[2:]} ^ {bin(y)[2:]}"
    
    def get_binary_string(self, integer):
        return bin(integer)[2:]

    def main(self, inputs):
        # return [
        #     [[self.xor(x, index+1) for index in range(10)], [self.xor(y, index+1) for index in range(10)]]
        #     for x, y in inputs 
        # ]
        def calculate_maximum_matching_suffix(bin_str1, bin_str2):
            def get_value_at_index(string, index):
                if index >= 0:
                    if index < len(string)-1:
                        return string[index]
                else:
                    if index >= -len(string):
                        return string[index]
                return '0'
    
            index = -1
            while index >= -max(len(bin_str1), len(bin_str2)):
                if get_value_at_index(bin_str1, index) != get_value_at_index(bin_str2, index):
                    break
                index -= 1

            # print(f"For {bin_str1} and {bin_str2} --> {bin_str1[index:] if len(bin_str1) <= len(bin_str2) else bin_str2[index:]}")
            return abs(index)-1
        
        return [
            2 ** calculate_maximum_matching_suffix(self.get_binary_string(x), self.get_binary_string(y))
            for x, y in inputs
        ]

if __name__ == "__main__":
    [print(result) for result in Solution().main(Solution().read_input())]
