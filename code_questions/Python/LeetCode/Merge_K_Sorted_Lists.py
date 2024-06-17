"""
https://leetcode.com/problems/merge-k-sorted-lists/
"""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self) -> str:
        return f"{self.val}_{self.next.__str__() if self.next is not None else ''}"

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

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:

    def mergeKLists(self, lists: list[ListNode]) -> ListNode:
        lists = [lst for lst in lists if lst]
        if (not lists) or (lists and not lists[0]):
            return None

        merged_root = ListNode(val=None)

        while True:
            values=[]
            for node in lists:
                print(node)
                if (node is not None) and (node.val is not None):
                    values.append(node.val)
                else:
                    values.append(99999)

            min_value, min_index = 99999, -1
            for idx, val in enumerate(values):
                if val < min_value:
                    min_value=val
                    min_index = idx

            if min_index != -1:
                if merged_root.val is None:
                    merged_root.val = min_value
                elif merged_root.next == None:
                    tempNode = ListNode(min_value)
                    merged_root.next = tempNode
                else:
                    tempNode.next = ListNode(min_value)
                    tempNode = tempNode.next

                lists[min_index] = lists[min_index].next

            else:
                break

        return merged_root


class Solution2:

    def mergeKLists(self, lists: list[ListNode]) -> ListNode:
        lists = [lst for lst in lists if lst]
        if (not lists) or (lists and not lists[0]):
            return None

        merged_list = []
        for lstNode in lists:

            while lstNode is not None:
                if lstNode.val is not None:
                    merged_list.append(lstNode.val)
                lstNode = lstNode.next

        merged_list = sorted(merged_list)
        root = ListNode(val=None)
        for i in merged_list:
            if root.val is None:
                root.val = i
            elif root.next == None:
                tempNode = ListNode(i)
                root.next = tempNode
            else:
                tempNode.next = ListNode(i)
                tempNode = tempNode.next

        return root

if __name__ == "__main__":
    # lists = [[1,4,5],[1,3,4],[2,6]]
    lists = [[0,2,5]]
    # lists = [[], [1]]
    lists = [createLinkedList(lst) for lst in lists]
    for lst in lists:
        printLinkedList(lst)

    printLinkedList(Solution2().mergeKLists(lists))
