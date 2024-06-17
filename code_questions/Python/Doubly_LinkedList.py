class node:
    def __init__(self, value):
        self.value = value
        self.ford = None
        self.prev = None

class LL:
    def __init__(self, head):
        self.head = head

    def insert_at_end(self, newValue):
        newNode = node(newValue)
        #print(newNode.value)
        current = self.head
        while current.ford != None:
            current = current.ford
        current.ford = newNode
        newNode.prev = current

    def insert_at_front(self, newValue):
        newNode = node(newValue)
        self.head.prev = newNode
        newNode.ford = self.head
        self.head = newNode

    def insert_after_node(self, newValue, nodeValue):
        newNode = node(newValue)
        current = self.head
        if current.ford != None:
            while current.ford != None:
                if current.value == nodeValue:
                    break
                else:
                    current = current.ford
                    if (current.ford == None) and (current.value != nodeValue):
                        print("That node doesn't exits.")
                        return
            if current.ford != None:
                temp = current.ford
                current.ford = newNode
                newNode.prev = current
                temp.prev = newNode
                newNode.ford = temp
            else:
                current.ford = newNode
                newNode.prev = current
        else:
            if current.value == nodeValue:
                current.ford = newNode
                newNode.prev = current
            else:
                print("That node doesn't exist.")
                return

    def insert_before_node(self, newValue, nodeValue):
        newNode = node(newValue)
        current = self.head
        if current.ford != None:
            while current.ford != None:
                if current.value == nodeValue:
                    break
                else:
                    current = current.ford
                    if (current.ford == None) and (current.value != nodeValue):
                        print("That node doesn't exist.")
            newNode.ford = current
            if current.prev == None:
                current.prev = newNode
            else:
                temp = current.prev
                current.prev = newNode
                temp.ford = newNode
                newNode.prev = temp
                newNode.ford = current
        else:
            if current.value == nodeValue:
                self.insert_at_front(newValue)
            else:
                print("That node doesn't exist.")
                return

    def delete(self, nodeValue):
        current = self.head
        if current.ford != None:
            while current.ford != None:
                if current.value == nodeValue:
                    break
                else:
                    current = current.ford
                    if (current.ford == None) and (current.value != nodeValue):
                        print("That node doesn't exist.")
                        return
            if current.ford != None:
                front = current.prev
                back = current.ford
                back.prev = front
                front.ford = back
            else:
                back = current.prev
                back.ford = None
        else:
            if current.value == nodeValue:
                self.head = None
                print("Linked list is empty now.")
            else:
                print("That node doesn't exist.")
                return

    def reverse(self):
        current = self.head
        while current.ford != None:
            temp = current.ford
            current.ford = current.prev
            current.prev = temp
            current = temp
        temp = current.ford
        current.ford = current.prev
        current.prev = temp
        self.head = current

    def display(self):
        current = self.head
        if current.ford != None:
            while current.ford != None:
                print(current.value, " -> ", end = ' ')
                current = current.ford
            print(current.value)
        else:
            print(current.value, " -> ", end = ' ')

head = node(int(input("Enter value for head: ")))
#print(head.value)
LinkedList = LL(head)
LinkedList.display()
ip = int(input("\nEnter values to add: "))
while(ip != -1):
    LinkedList.insert_at_end(ip)
    LinkedList.display()
    ip = int(input("\nEnter values to add: "))
    #print('here ', ip)
LinkedList.delete(int(input("\nDelete any number: ")))
LinkedList.display()
LinkedList.insert_at_front(int(input("\nEnter a number at front: ")))
LinkedList.display()
LinkedList.insert_after_node(int(input("\nEnter a number to add: ")), int(input("\nEnter a value to add it after: ")))
LinkedList.display()
LinkedList.insert_before_node(int(input("\nEnter a number to add: ")), int(input("\nEnter a value to add it before: ")))
LinkedList.display()
print("Reverse of given list is: ")
LinkedList.reverse()
LinkedList.display()
