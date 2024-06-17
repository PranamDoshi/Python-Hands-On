from DataStructures.TreeFunctions import TreeNode, levelOrderTraversal
from DataStructures.BSTtreeFunctions import searchBST

class SumInBST:

    def findTarget(self, root, k):
        if not root and not k:
            return True
        elif not root and k:
            return False
        else:
            levelNodes = [root]
            seenValues = set()
            while levelNodes:
                temp = levelNodes.pop(0)
                for s in seenValues:
                    print(s, end = ' ')
                print(temp.val)
                if k - temp.val in seenValues:
                    return True
                seenValues.add(temp.val)
                if temp.left:
                    levelNodes.append(temp.left)
                if temp.right:
                    levelNodes.append(temp.right)
            
            return False
        

if __name__ == '__main__':
    sol = SumInBST()

    # root = TreeNode(5)
    # root.left = TreeNode(3)
    # root.right = TreeNode(6)
    # root.left.left = TreeNode(2)
    # root.left.right = TreeNode(4)
    # root.right.right = TreeNode(7)
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)

    k = int(input())

    print(sol.findTarget(root, k))