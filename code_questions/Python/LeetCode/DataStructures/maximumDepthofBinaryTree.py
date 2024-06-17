from tkinter.tix import Tree
from TreeFunctions import TreeNode

class Solution:

    def maxDepth(self, root):
        if not root:
            return 0
        elif not root.left and not root.right:
            return 1
        else:
            depth = 1
            depth += max(self.maxDepth(root.left), self.maxDepth(root.right))
            return depth


if __name__ == "__main__":
    sol = Solution()

    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    print(sol.maxDepth(root))