all = ['TreeNode', 'insert', 'searchBST', 'checkValidity']

class TreeNode:

    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def insert(root, val):
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

def searchBST(root, val):
    if not root:
        return root
    else:
        if root.val == val:
            return root
        elif root.val < val:
            return searchBST(root.right, val)
        elif root.val > val:
            return searchBST(root.left, val)

def checkValidity(root, minNode = None, maxNode = None):
    if not root:
        return True
    elif minNode and minNode.val >= root.val:
        return False
    elif maxNode and maxNode.val <= root.val:
        return False
    else:
        return checkValidity(root.left, minNode, root) and checkValidity(root.right, root, maxNode)