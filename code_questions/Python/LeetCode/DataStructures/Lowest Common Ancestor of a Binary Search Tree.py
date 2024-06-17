from TreeFunctions import TreeNode

class CommonAncestor:

    def lowestCommonAncestor(self, root, p, q):
        if not root:
            return root
        elif p.val <= root.val <= q.val or p.val >= root.val >= q.val:
            return root
        elif p.val > root.val < q.val:
            return self.lowestCommonAncestor(root.right, p, q)
        else:
            return self.lowestCommonAncestor(root.left, p, q)
        


if __name__ == '__main__':
    sol = CommonAncestor()

    # root = TreeNode(5)
    # root.left = TreeNode(3)
    # root.right = TreeNode(6)
    # root.left.left = TreeNode(2)
    # root.left.right = TreeNode(4)
    # root.right.right = TreeNode(7)
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)

    p = TreeNode(1)
    q = TreeNode(3)

    ansNode = sol.lowestCommonAncestor(root, p, q)
    if ansNode:
        print(ansNode.val)
    else:
        print('Empty Tree')