from multiprocessing.connection import answer_challenge


class Solution:

    def generate(self, numRows):
        answer = []
        step = 0

        while step < numRows:
            tempRow = []

            for i in range(step+1):
                if i == 0 or i == step:
                    tempRow.append(1)
                else:
                    tempRow.append(answer[step - 1][i] + answer[step - 1][i - 1])

            answer.append(tempRow)
            step += 1
        
        return answer


if __name__ == "__main__":
    sol = Solution()

    numRows = int(input())

    print(sol.generate(numRows))