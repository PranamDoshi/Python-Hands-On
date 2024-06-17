from TreeFunctions import TreeNode

class Solution:

    def preOrderTraversal(self, root):
        travrsalList = []

        preOrderTraversal(root, travrsalList)

        return travrsalList

def preOrderTraversal(root, traveersalList = []):
    if root:
        traveersalList.append(root.val)
        preOrderTraversal(root.left, traveersalList)
        preOrderTraversal(root.right, traveersalList)


if __name__ == "__main__":
    sol = Solution()

    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)

    print(sol.preOrderTraversal(root))