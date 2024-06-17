class node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
        self.height = 1

class AVL:
    def __init__(self, root = None):
        self.root = root

    def minNode(self, root):
        while root.left != None:
            root = root.left
        return root

    def CalHeight(self, root):
        if root == None:
            return 0
        return root.height

    def left_rotate(self, root):
        temp = root.right
        temp2 = temp.left
        root.right = temp2
        temp.left = root
        root.height = 1 + max(self.CalHeight(root.left), self.CalHeight(root.right))
        temp.height = 1 + max(self.CalHeight(temp.left), self.CalHeight(temp.right))
        return temp

    def right_rotate(self, root):
        temp = root.left
        temp2 = temp.right
        root.left = temp2
        temp.right = root
        root.height = 1 + max(self.CalHeight(root.left), self.CalHeight(root.right))
        temp.height = 1 + max(self.CalHeight(temp.left), self.CalHeight(temp.right))
        return temp

    def insert(self, root, value):
        if root == None:
            return node(value)
        elif root.value < value:
            root.right = self.insert(root.right, value)
        elif root.value > value:
            root.left = self.insert(root.left, value)
        else:
            print("Node with this value already exist.")
            return root
        root.height = 1 + max(self.CalHeight(root.left), self.CalHeight(root.right))
        balance = self.CalHeight(root.left) - self.CalHeight(root.right)
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)
        elif balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        elif balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        elif balance > 1 and value < root.left.value:
            return self.right_rotate(root)
        else:
            return root

    def delete(self, value, root):
        if root == None:
            print("Tree is empty.")
            return root
        elif value < root.value:
            root.left = self.delete(value, root.left)
        elif value > root.value:
            root.right = self.delete(value, root.right)
        else:
            if root.left == None or root.right == None:
                temp = root.left if root.left != None else root.right
                if temp == None:
                    root = None
                else:
                    root = temp
            else:
                temp =  self.minNode(root.right)
                root.value = temp.value
                root.right = self.delete(root.value, root.right)
        if root == None:
            return root
        root.height = 1 + max(self.CalHeight(root.left), self.CalHeight(root.right))
        balance = self.CalHeight(root.left) - self.CalHeight(root.right)
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)
        elif balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        elif balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        elif balance > 1 and value < root.left.value:
            return self.right_rotate(root)
        else:
            return root

def Preorder(root):
    if root != None:
        print(root.value, end = ' ')
        Preorder(root.left)
        Preorder(root.right)

root = None
Tree = AVL()
ip = int(input("Enter first value: "))
while ip != -1:
    root = Tree.insert(root, ip)
    Preorder(root)
    ip = int(input("\nEnter next value: "))

ip = int(input("Delete a value: "))
while ip != -1:
    root = Tree.delete(ip, root)
    Preorder(root)
    ip = int(input("\nDelete a value: "))
