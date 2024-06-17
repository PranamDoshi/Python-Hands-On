class MaxArea:

    def recursiveChecker(self, grid, i, j, seenIndexes, area = 1):
        if i > 0 and grid[i-1][j] == 1 and (i-1, j) not in seenIndexes:
            seenIndexes.add((i-1, j))
            area = self.recursiveChecker(grid, i-1, j, seenIndexes, area + 1)
        if j > 0 and grid[i][j-1] == 1 and (i, j-1) not in seenIndexes:
            seenIndexes.add((i, j-1))
            area = self.recursiveChecker(grid, i, j-1, seenIndexes, area + 1)
        if i < len(grid) - 1 and grid[i+1][j] == 1 and (i+1, j) not in seenIndexes:
            seenIndexes.add((i+1, j))
            area = self.recursiveChecker(grid, i+1, j, seenIndexes, area + 1)
        if j < len(grid[0]) - 1 and grid[i][j+1] == 1 and (i, j+1) not in seenIndexes:
            seenIndexes.add((i, j+1))
            area = self.recursiveChecker(grid, i, j+1, seenIndexes, area + 1)
        
        return area

    def maxAreaOfIsland(self, grid):
        maxArea, seenIndexes = 0, set()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1 and (i, j) not in seenIndexes:
                    #print(i, j, grid[i][j], seenIndexes)
                    seenIndexes.add((i, j))
                    area = self.recursiveChecker(grid, i, j, seenIndexes)
                    if area > maxArea:
                        maxArea = area
        #print(seenIndexes)
        return maxArea
"""
0,0,1,0,0,0,0,1,0,0,0,0,0
0,0,0,0,0,0,0,1,1,1,0,0,0
0,1,1,0,1,0,0,0,0,0,0,0,0
0,1,0,0,1,1,0,0,1,0,1,0,0
0,1,0,0,1,1,0,0,1,1,1,0,0
0,0,0,0,0,0,0,0,0,0,1,0,0
0,0,0,0,0,0,0,1,1,1,0,0,0
0,0,0,0,0,0,0,1,1,0,0,0,0
"""

if __name__ == "__main__":
    sol = MaxArea()

    numRows = int(input())
    grid = []
    for row in range(numRows):
        grid.append(list(map(int, input().split(','))))

    print(sol.maxAreaOfIsland(grid))