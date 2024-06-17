"""
grid(M✕N) =
. . . . .
* * . * *
. # # # .
. . . . .

. . . . .
. . . . .
. . . . .
. . . . .

* = wall, # = doors, . = no obstacle

1st process can pass through doors and 2nd process can pass through walls
Find minimum time required to reach from (0, 0) to (M-1,N-1)
"""

class minimumTimeRequired:

    def forProcess1(self, grid, i, j, time, visited):
        # Can pass through doors (#)
        if i == len(grid) - 1 and j == len(grid[0]) - 1:
            return time
        visited.add((i, j))
        times = set()
        if i < len(grid) - 1 and grid[i+1][j] in ['.', '#'] and (i+1, j) not in visited:
            times.add(self.forProcess1(grid, i+1, j, time+1, visited))
        if j < len(grid[0]) - 1 and grid[i][j+1] in ['.', '#'] and (i, j+1) not in visited:
            times.add(self.forProcess1(grid, i, j+1, time+1, visited))
        if i > 0 and grid[i-1][j] in ['.', '#'] and (i-1, j) not in visited:
            times.add(self.forProcess1(grid, i-1, j, time+1, visited))
        if j > 0 and grid[i][j-1] in ['.', '#'] and (i, j-1) not in visited:
            times.add(self.forProcess1(grid, i, j-1, time+1, visited))
        # print(times, visited, i, j, grid[i][j])

        min = float('inf')
        for t in list(times):
            if t >= 0 and t < min:
                min = t
        
        if min == float('inf'):
            return -1
        else:
            return min
    
    def forProcess2(self, grid, i, j, time, visited):
        # Can pass through walls (*)
        if i == len(grid) - 1 and j == len(grid[0]) - 1:
            return time
        visited.add((i, j))
        times = set()
        if i < len(grid) - 1 and grid[i+1][j] in ['.', '*'] and (i+1, j) not in visited:
            times.add(self.forProcess2(grid, i+1, j, time+1, visited))
        if j < len(grid[0]) - 1 and grid[i][j+1] in ['.', '*'] and (i, j+1) not in visited:
            times.add(self.forProcess2(grid, i, j+1, time+1, visited))
        if i > 0 and grid[i-1][j] in ['.', '*'] and (i-1, j) not in visited:
            times.add(self.forProcess2(grid, i-1, j, time+1, visited))
        if j > 0 and grid[i][j-1] in ['.', '*'] and (i, j-1) not in visited:
            times.add(self.forProcess2(grid, i, j-1, time+1, visited))
        # print(times, visited, i, j, grid[i][j])
        
        min = float('inf')
        for t in list(times):
            if t >= 0 and t < min:
                min = t
        
        if min == float('inf'):
            return -1
        else:
            return min


if __name__ == "__main__":
    sol = minimumTimeRequired()

    grid = []
    rows = int(input())
    for r in range(rows):
        grid.append(list(input().split()))
    
    print()
    for row in grid:
        print('-'.join(row))
    print()

    visited = set()
    print(sol.forProcess1(grid, 0, 0, 0, visited))
    visited.clear()
    print(sol.forProcess2(grid, 0, 0, 0, visited))

"""
4
. . . . .
* * . * *
. # # # .
. . . . .

.-.-.-.-.
*-*-.-*-*
.-#-#-#-.
.-.-.-.-.

{9} {(0, 1), (2, 4), (1, 2), (0, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 2 4 .
{9} {(0, 1), (2, 4), (1, 2), (0, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 2 3 #
{9, 7} {(0, 1), (2, 4), (1, 2), (0, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 3 3 .
set() {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 3 0 .
{-1} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 2 0 .
{-1} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 2 1 #
{-1} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 3 1 .
{-1, 7} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 3 2 .
{7} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 2 2 #
{7} {(0, 1), (2, 4), (1, 2), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 1 2 .
set() {(0, 1), (2, 4), (1, 2), (0, 4), (2, 1), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 0 4 .
{-1} {(0, 1), (2, 4), (1, 2), (0, 4), (2, 1), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 0 3 .
{-1, 7} {(0, 1), (2, 4), (1, 2), (0, 4), (2, 1), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 0 2 .
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (2, 1), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 0 1 .
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (2, 1), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)} 0 0 .
7
{7} {(0, 0), (3, 1), (2, 0), (3, 0), (3, 3), (1, 0), (3, 2)} 3 3 .
{7} {(0, 0), (3, 1), (2, 0), (3, 0), (3, 3), (1, 0), (3, 2)} 3 2 .
{7} {(0, 0), (3, 1), (2, 0), (3, 0), (3, 3), (1, 0), (3, 2)} 3 1 .
{7} {(0, 0), (3, 1), (2, 0), (3, 0), (3, 3), (1, 0), (3, 2)} 3 0 .
{7} {(0, 0), (3, 1), (2, 0), (3, 0), (3, 3), (1, 0), (3, 2)} 2 0 .
{7} {(2, 4), (1, 2), (0, 0), (3, 1), (1, 1), (2, 0), (1, 4), (3, 0), (3, 3), (1, 0), (3, 2), (1, 3)} 2 4 .
set() {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 0 1 .
{-1} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 0 2 .
{-1} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 0 3 .
{-1} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 0 4 .
{-1, 7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 1 4 *
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 1 3 *
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 1 2 .
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 1 1 *
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 1 0 *
{7} {(0, 1), (2, 4), (1, 2), (0, 4), (0, 0), (3, 1), (1, 1), (0, 3), (2, 0), (1, 4), (3, 0), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)} 0 0 .
7
"""