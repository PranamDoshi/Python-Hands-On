from TreeFunctions import TreeNode

class Solution:

    def isSymmetric(self, root):
        levelNode = [root]

        while levelNode:
            nextLevel = []
            nextLevelValues = []
            for i in range(len(levelNode)):
                nodeUnderConsideration = levelNode[i]

                if nodeUnderConsideration.left:
                    nextLevel.append(nodeUnderConsideration.left)
                    nextLevelValues.append(nodeUnderConsideration.left.val)
                else:
                    nextLevelValues.append('No')
                
                if nodeUnderConsideration.right:
                    nextLevel.append(nodeUnderConsideration.right)
                    nextLevelValues.append(nodeUnderConsideration.right.val)
                else:
                    nextLevelValues.append('No')

            if len(nextLevelValues) and list(reversed(nextLevelValues)) != nextLevelValues:
                return False

            levelNode = nextLevel
        
        return True


if __name__ == "__main__":
    sol = Solution()

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(2)
    #root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    #root.right.left = TreeNode(4)
    root.right.right = TreeNode(4)

    print(sol.isSymmetric(root))