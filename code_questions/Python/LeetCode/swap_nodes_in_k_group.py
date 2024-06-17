"""
https://leetcode.com/problems/reverse-nodes-in-k-group/description/
"""
from DataStructures.LinkdedListFunctions import printLinkedList, createLinkedList
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Stack_Data:

    def __init__(self) -> None:
        self.stack = list()

    def push(self, item: any):
        self.stack.append(item)

    def pop(self)-> any:
        if self.stack:
            return self.stack.pop()
        return None
    
    def size(self):
        return self.stack.__len__()

class Solution:

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode|None:
        if (not head) or (not head.next) or k <= 1:
            return head

        prev = None
        curr = head

        stack = Stack_Data()
        while curr:

            if stack.size() < k:
                stack.push(curr)
                curr = curr.next
                # print([node.val for node in stack.stack])

            else:
                temp_node, temp_head = None, None
                while stack.size():
                    if not temp_head:
                        temp_head = stack.pop()
                    elif not temp_node:
                        temp_head.next = stack.pop()
                        temp_node = temp_head.next
                    else:
                        temp_node.next = stack.pop()
                        temp_node = temp_node.next
                # print(temp_head.val)
                # print(temp_node.val)

                if prev:
                    prev.next = temp_head
                else:
                    head = temp_head
                
                temp_node.next = curr
                prev = temp_node
                # print(prev.val)
                # print(head.val)
                # print(temp_node.val)

        if stack.size() == k:
            temp_node, temp_head = None, None
            while stack.size():
                if not temp_head:
                    temp_head = stack.pop()
                elif not temp_node:
                    temp_head.next = stack.pop()
                    temp_node = temp_head.next
                else:
                    temp_node.next = stack.pop()
                    temp_node = temp_node.next
            # print(temp_head.val)
            # print(temp_node.val)

            if prev:
                prev.next = temp_head
            else:
                head = temp_head
            
            temp_node.next = curr
            prev = temp_node
            # print(prev.val)
            # print(head.val)
            # print(temp_node.val)

        return head

if __name__ == "__main__":
    head=[1,2,3,4,5,6,7]
    k=2

    head=createLinkedList(head)

    printLinkedList(Solution().reverseKGroup(head, k))
