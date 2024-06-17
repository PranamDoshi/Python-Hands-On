from Merge2SortedLinkedList import createLinkedList, ListNode
from RemoveLinkedListElements import printLinkedList
from collections import defaultdict

class Solution:

    def deleteDuplicates(self, head):
        """
        Delete all duplicate values
        """
        temp = head

        if head == None or head.next == None:
            return head
        else:
            while temp.next:
                if temp.next.val == temp.val:
                    temp.next = temp.next.next
                else:
                    temp = temp.next

            return head

    def deleteDuplicates2(self, head):
        """
        Delete all repeating values
        """
        if not head or not head.next:
            return head
        else:
            removableValue = defaultdict(int)
            ansHead, ansTemp = None, None
            temp = head
            while temp.next:
                if ansHead and ansHead.next:
                    print(ansTemp.val)
                
                if temp.val == temp.next.val:
                    removableValue[temp.val] += 2
                elif removableValue[temp.val] > 0:
                    removableValue[temp.val] += 1
                else:
                    if not ansHead:
                        ansHead = ListNode(temp.val)
                    elif not ansHead.next:
                        ansTemp = ListNode(temp.val)
                        ansHead.next = ansTemp
                    else:
                        ansTemp.next = ListNode(temp.val)
                        ansTemp = ansTemp.next
                
                temp = temp.next
                
            if not removableValue[temp.val]:
                if not ansHead:
                    ansHead = ListNode(temp.val)
                elif not ansHead.next:
                    ansTemp = ListNode(temp.val)
                    ansHead.next = ansTemp
                else:
                    ansTemp.next = ListNode(temp.val)
                    ansTemp = ansTemp.next
            
            return ansHead


if __name__ == "__main__":
    sol = Solution()

    LinkedList = list(map(int, input().split()))
    head = createLinkedList(LinkedList)

    printLinkedList(head)
    printLinkedList(sol.deleteDuplicates2(head))