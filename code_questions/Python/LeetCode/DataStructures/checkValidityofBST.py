from TreeFunctions import TreeNode, checkValidity

class ValidBST:

    def isValidBST(self, root):
        return checkValidity(root, minNode = None, maxNode = None)


if __name__ == '__main__':
    sol = ValidBST()

    root = TreeNode(5)
    root.left = TreeNode(1)
    root.right = TreeNode(6)
    root.right.left = TreeNode(3)
    root.right.right = TreeNode(7)

    print(sol.isValidBST(root))