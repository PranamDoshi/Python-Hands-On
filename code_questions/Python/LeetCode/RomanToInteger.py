from re import I


class RomanNumbders:

    def romantoInt(self, s):
        romanSymbols = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        intAns = 0

        for i in range(len(s)):
            if s[i] == 'I':
                
            elif s[i] == 'X':

            elif s[i] == 'C':
                
            else:
                intAns += romanSymbols[s[I]]
                i += 1


if __name__ == "__main__":
    sol = RomanNumbders()

    s = input()

    print(sol.romantoInt(s))