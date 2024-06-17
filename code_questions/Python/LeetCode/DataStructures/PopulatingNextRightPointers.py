from distutils.util import change_root
from TreeFunctions import TreeNode, levelOrderTraversal

class NextPointerinTree:

    def connect(self, root):
        if not root or (not root.left and not root.right):
            return root
        
        # levels = [root]

        # while levels:
        #     tempLevels = []
        #     for i in range(len(levels)):
        #         if levels[i].left:
        #             tempLevels.append(levels[i].left)
        #         if levels[i].right:
        #             tempLevels.append(levels[i].right)
                
        #         if i < len(levels) - 1:
        #             levels[i].next = levels[i+1]
            
        #     levels = tempLevels

        root.left.next = root.right
        if root.next:
            root.right.next = root.next.left
        
        self.connect(root.left)
        self.connect(root.right)

        return root


if __name__ == "__main__":
    sol = NextPointerinTree()

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    print(list(levelOrderTraversal(root))[0])

    changedRoot = sol.connect(root)

    print(list(levelOrderTraversal(changedRoot))[0])