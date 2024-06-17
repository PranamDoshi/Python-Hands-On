from Merge2SortedLinkedList import ListNode, createLinkedList

class Solution:

    def hasCycle(self, head):
        if head == None or head.next == None:
            return False
        else:
            temp = head
            nodesVisited = {}
            
            while temp.next:
                if temp in nodesVisited:
                    return True
                nodesVisited[temp] = temp.next
                try:
                    temp = temp.next
                except AttributeError:
                    break
            
            return False

    def hasCycle2(self, head):
        """
        Take 2 pointers, move them through the linked list at different speeds.
        If there is a loop they will meet at some node, otherwise faster pointer will reach the end of the loop.
        """

        if head == None or head.next == None:
            return False
        else:
            fast = head
            slow = head
            
            while fasr != None and fasr.next != None:
                fasr = fasr.next.next
                slow = slow.next

                if fasr == slow:
                    return True
            
            return False


if __name__ == "__name__":
    sol = Solution()

    linkedList = list(map(int, input().split()))
    head = createLinkedList(linkedList)

    print(sol.hasCycle(head))