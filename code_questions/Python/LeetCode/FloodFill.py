class FloodFill:

    def recursiveChecker(self, image, sr, sc, newColor, seenIndexes):
        if sr > 0 and image[sr][sc] == image[sr-1][sc] and (sr-1, sc) not in seenIndexes:
            seenIndexes.add((sr-1, sc))
            self.recursiveChecker(image, sr-1, sc, newColor, seenIndexes)
        if sc > 0 and image[sr][sc] == image[sr][sc-1] and (sr, sc-1) not in seenIndexes:
            seenIndexes.add((sr, sc-1))
            self.recursiveChecker(image, sr, sc-1, newColor, seenIndexes)
        if sr < len(image) - 1 and image[sr][sc] == image[sr+1][sc] and (sr+1, sc) not in seenIndexes:
            seenIndexes.add((sr+1,sc))
            self.recursiveChecker(image, sr+1, sc, newColor, seenIndexes)
        if sc < len(image[0]) - 1 and image[sr][sc] == image[sr][sc+1] and (sr, sc+1) not in seenIndexes:
            seenIndexes.add((sr, sc+1))
            self.recursiveChecker(image, sr, sc+1, newColor, seenIndexes)
        
        image[sr][sc] = newColor

    def floodfill(self, image, sr, sc, newColor):
        seenIndexes = set()
        seenIndexes.add((sr, sc))
        self.recursiveChecker(image, sr, sc, newColor, seenIndexes)
        # for point in seenIndexes:
        #     image[point[0]][point[1]] = newColor
        return image


if __name__ == "__main__":
    sol = FloodFill()

    numRows = int(input())
    image = []
    for r in range(numRows):
        image.append(list(map(int, input().split())))
    sr, sc, newColor = list(map(int, input().split()))
    
    print()

    for row in image:
        print(' '.join(map(str, row)))
    
    print()

    sol.floodfill(image, sr, sc, newColor)
    for row in image:
        print(' '.join(map(str, row)))