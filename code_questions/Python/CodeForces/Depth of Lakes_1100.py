""" https://codeforces.com/problemset/problem/1829/E """

import pprint

""" 
Input Foramt:
1) The first line contains a single integer t (1≤t≤104) — the number of test cases.
2) The first line of each test case contains two integers n,m (1≤n,m≤1000) — the number of rows and columns of the grid, respectively.
3) Then n lines follow each with m integers ai,j (0≤ai,j≤1000) — the depth of the water at each cell.
Sample Input:
5
3 3
1 2 0
3 4 0
0 0 5
1 1
0
3 3
0 1 1
1 0 1
1 1 1
5 5
1 1 1 1 1
1 0 0 0 1
1 0 5 0 1
1 0 0 0 1
1 1 1 1 1
5 5
1 1 1 1 1
1 0 0 0 1
1 1 4 0 1
1 0 0 0 1
1 1 1 1 1
"""

def find_lake_volume(matrix: list[list], volume: int = 0, x: int = 0, y: int = 0, visited: set = set())-> int:
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return 0

    if x < len(matrix) and y < len(matrix[0]):

        if matrix[x][y] > 0:
            if (x, y) not in visited:
                volume += matrix[x][y]
                visited.add((x, y))
                print(f"Visited {visited} locations, volume is {volume}.")

            if x+1<len(matrix) and y+1<len(matrix[0]):
                return find_lake_volume(matrix, volume, x+1, y, visited) + find_lake_volume(matrix, volume, x, y+1, visited)
            
            elif x+1<len(matrix):
                return find_lake_volume(matrix, volume, x+1, y, visited)

            elif y+1<len(matrix[0]):
                return find_lake_volume(matrix, volume, x, y+1, visited)

            return volume

        return 0

    return 0

if __name__ == "__main__":
    inputFile = open('input.txt')

    test_cases = int(inputFile.readline())
    for case in range(test_cases):
        m, n = list(map(int, inputFile.readline().split()))
        matrix = []
        for n_value in range(n):
            matrix.append(list(map(int, inputFile.readline().split())))

        pprint.pprint(matrix, indent=3)
        print(f"Maximum volume is: {find_lake_volume(matrix)}")
