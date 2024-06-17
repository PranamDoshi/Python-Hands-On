from turtle import right


class Containers:

	def maxArea(self, height):
		leftSide, rightSide = 0, len(height) - 1
		maxArea = 0
		Area = lambda leftSide, rightSide: min(height[leftSide], height[rightSide])*(rightSide-leftSide)
    	
		while leftSide < rightSide:
			tempArea = Area(leftSide, rightSide)
			# print(height[leftSide], height[rightSide], tempArea, maxArea)
			if tempArea > maxArea:
				maxArea = tempArea
			
			if height[leftSide] >= height[rightSide]:
				rightSide -= 1
			else:
				leftSide += 1

		return maxArea


if __name__ == "__main__":
	sol = Containers()

	height = list(map(int, input().split(',')))

	print(sol.maxArea(height))