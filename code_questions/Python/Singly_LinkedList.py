class node:
    def __init__(self, name, next = None):
        self.name = name
        self.next = next

class LinkedList():
    def __init__(self, node):
        self.head = node

    def insert(self, name):
        newNode = node(name)
        current = self.head
        while(current.next):
            current = current.next
        current.next = newNode

    def print(self):
        current = self.head
        while(current.next):
            print(current.name, ' => ', end = '')
            current = current.next

head = node(input("Enter Name: "))
LL = LinkedList(head)
while(int(input('Do you want to add another node?')) == 1):
    LL.insert(input("Enter Name: "))
LL.print()
