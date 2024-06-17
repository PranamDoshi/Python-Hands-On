all = ['preOrderTraversal', 'postOrderTraversal', 'inOrderTraversal', 'levelOrderTraversal', 'invertTree', 'hasPathSum']

class TreeNode:

    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def preOrderTraversal(root, traversalList = []):
    if root:
        traversalList.append(root.val)
        preOrderTraversal(root.left, traversalList)
        preOrderTraversal(root.right, traversalList)

def inOrderTraversal(root, traversalList = []):
    if root:
        inOrderTraversal(root.left, traversalList)
        traversalList.append(root.val)
        inOrderTraversal(root.right, traversalList)

def postOrderTraversal(root, traversalList = []):
    if root:
        postOrderTraversal(root.left, traversalList)
        postOrderTraversal(root.right, traversalList)
        traversalList.append(root.val)

def levelOrderTraversal(root):
    if not root:
        return root
    else:
        levels = []
        levelsByValues = []
        levelNodes = [root]
        nextLevelValues = [root.val]
        levels.append(nextLevelValues)
        levelsByValues.extend(nextLevelValues)

        while levelNodes:
            nextLevel = []
            nextLevelValues = []
            for i in range(len(levelNodes)):
                if levelNodes[i].left:
                    nextLevelValues.append(levelNodes[i].left.val)
                    nextLevel.append(levelNodes[i].left)
                if levelNodes[i].right:
                    nextLevelValues.append(levelNodes[i].right.val)
                    nextLevel.append(levelNodes[i].right)
            
            levelNodes = nextLevel
            if len(nextLevelValues):
                levels.append(nextLevelValues)
                levelsByValues.extend(nextLevelValues)
    
        return levels, levelsByValues

def invertTree(root):
    if not root:
        return root
    elif root.left or root.right:
        root.left, root.right = invertTree(root.right), invertTree(root.left)
                
    return root

def hasPathSum(root, targetSum):
    if not root:
        return False
    elif root.val == targetSum and (not root.left and not root.right):
        return True
    else:
        return hasPathSum(root.left, targetSum - root.val) or hasPathSum(root.right, targetSum - root.val)
