from email import header
from TreeFunctions import TreeNode, inOrderTraversal, preOrderTraversal

class insertInBST:

    def insert(self, root, val):
        if not root:
            return TreeNode(val)
        else:
            temp = root
            parentNode = None
            toLeft, toRight = False, False

            while True:
                if temp and temp.val < val:
                    parentNode = temp
                    temp = temp.right
                    toLeft, toRight = False, True
                elif temp and temp.val > val:
                    parentNode = temp
                    temp = temp.left
                    toLeft, toRight = True, False
                else:
                    if not temp and toLeft:
                        parentNode.left = TreeNode(val)
                        break
                    elif not temp and toRight:
                        parentNode.right = TreeNode(val)
                        break

            return root


if __name__ == "__main__":
    sol = insertInBST()

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
    inOrderTraversal(sol.insert(root, val), traversalList)
    print(traversalList)