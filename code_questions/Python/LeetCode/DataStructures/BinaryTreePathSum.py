from TreeFunctions import TreeNode

class Solution:

    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        elif root.val == targetSum and (not root.left and not root.right):
            return True
        else:
            return self.hasPathSum(root.left, targetSum - root.val) or self.hasPathSum(root.right, targetSum - root.val)


if __name__ == "__main__":
    sol = Solution()

    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left = TreeNode(7)
    root.left.left.right = TreeNode(2)
    root.right.left = TreeNode(13)
    root.right.right = TreeNode(4)
    root.right.right.right = TreeNode(1)

    targetSum = int(input())

    print(sol.hasPathSum(root, targetSum))