from TreeFunctions import TreeNode, inOrderTraversal

class Solution:
    def invertTree(self, root):
        if not root:
            return root
        elif root.left or root.right:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
                    
        return root
    
if __name__ == "__main__":
    sol = Solution()

    root = TreeNode(1)
    root.left = TreeNode(2)

    traversalList = []
    inOrderTraversal(root, traversalList)
    print(traversalList)
    
    traversalList = []
    inOrderTraversal(sol.invertTree(root), traversalList)
    print(traversalList)