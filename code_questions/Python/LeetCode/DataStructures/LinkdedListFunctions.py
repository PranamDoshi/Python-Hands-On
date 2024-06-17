class ListNode:

    def __init__(self, val = 0, next = None):
        self.val = val
        self.next = next

def createLinkedList(lst):
    root = ListNode(val=None)
    for i in lst:
        if root.val is None:
            root.val = i
        elif root.next == None:
            tempNode = ListNode(i)
            root.next = tempNode
        else:
            tempNode.next = ListNode(i)
            tempNode = tempNode.next
    
    return root

def printLinkedList(head):
    temp = head
    if temp == None:
        print("Empty list")
    else:
        while temp.next:
            print(temp.val, end = ' ')
            temp = temp.next
        print(temp.val)

def insertElement(head, temp, value):
    if not head:
        head = ListNode(value)
    elif not head.next:
        temp = ListNode(value)
        head.next = temp
    else:
        temp.next = ListNode(value)
        temp = temp.next
    
    return head, temp
