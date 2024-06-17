from TreeFunctions import TreeNode, levelOrderTraversal

if __name__ == "__main__":

    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    print(levelOrderTraversal(root))