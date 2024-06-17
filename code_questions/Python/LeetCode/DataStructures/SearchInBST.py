from TreeFunctions import TreeNode, inOrderTraversal

class SearchInBST:

    def searchBST(self, root, val):
        if not root:
            return root
        else:
            if root.val == val:
                return root
            elif root.val < val:
                return self.searchBST(root.right, val)
            elif root.val > val:
                return self.searchBST(root.left, val)


if __name__ == "__main__":
    sol = SearchInBST()

    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(7)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)

    val = int(input())

    
    traversalList = []
    inOrderTraversal(root, traversalList)
    print(traversalList)

    traversalList = []
    inOrderTraversal(sol.searchBST(root, val), traversalList)
    print(traversalList)