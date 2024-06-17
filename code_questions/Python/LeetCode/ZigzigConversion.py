class ZigzagString:

    def convert(self, s, numRows):
        if numRows == 1:
            return s
        
        zigzagMatrix = []

        for idx in range(numRows):
            zigzagMatrix.append([])
            tempIdx = idx
            while tempIdx < len(s):
                zigzagMatrix[idx].append(s[tempIdx])
                zigzagMatrix[idx].extend([' ']*(numRows - 2))
                tempIdx += (2*numRows - 2)
        
        ansString = ''
        ansString += ''.join(zigzagMatrix[0]).replace(' ', '')

        offset = numRows - 3
        for idx in range(1, numRows - 1):
            tempIdx = 1 + offset
            strIdx = (2*(numRows - 1) - idx)
            while strIdx < len(s):
                zigzagMatrix[idx][tempIdx] = s[strIdx]
                tempIdx += (numRows - 1)
                strIdx += (2*numRows - 2)
            ansString += ''.join(zigzagMatrix[idx]).replace(' ', '')
            offset -= 1
        
        ansString += ''.join(zigzagMatrix[numRows-1]).replace(' ', '')
        # for row in zigzagMatrix:
        #     print(row, end = '\n')

        # ansString = ''
        # for row in zigzagMatrix:
        #     ansString += ''.join(row)
        
        # return ansString.replace(' ', '')
        return ansString

    def convert(self, s, numRows):
        if numRows == 1:
            return s
        
        ansRows = ['' for i in range(numRows)]
        rowIdx, goDown = 0, True

        for idx in range(len(s)):
            ansRows[rowIdx] += s[idx]

            if rowIdx == numRows - 1:
                goDown = False
            elif rowIdx == 0:
                goDown = True

            if goDown:
                rowIdx += 1
            else:
                rowIdx -= 1
        
        return ''.join(ansRows)


if __name__ == "__main__":
    sol = ZigzagString()

    s = input()
    numRows = int(input())

    print(sol.convert(s, numRows))