from LinkdedListFunctions import ListNode, createLinkedList, printLinkedList
import time

class Solution:

    def reverseLinkedList(self, head):
        """
        Reverse entire LL
        """
        if head == None:
            return None
        elif head.next == None:
            return head
        else:
            prevNode = None
            nextNode = head.next
            temp = head

            while 1:
                temp.next = prevNode
                prevNode = temp
                temp = nextNode
                if nextNode == None:
                    break
                else:
                    nextNode = nextNode.next
            
            return prevNode
    
    def reverseLinkedList2(self, head):
        """
        Reverse entire LL
        """
        if head == None:
            return None
        elif head.next == None:
            return head
        else:
            prevNode = None
            nextNode = None
            temp = head

            while temp != None:
                nextNode = temp.next
                temp.next = prevNode
                prevNode = temp
                temp = nextNode

            return prevNode

    def reverseLinkedListInGivenPortion(self, head, left, right):
        """
        Reverse LL from given starting and ending nodes
        """
        if not head or not head.next or left == right:
            return head
        else:
            startNode, endNode, NodeBeforeStart, NodeAfterEnd = None, None, None, None
            temp, prevNode, nextNode = head, None, head.next
            counter = 1

            while True:
                if counter == left and not startNode:
                    startNode = temp
                    NodeBeforeStart = prevNode
                    temp = temp.next
                    counter += 1
                    prevNode = startNode
                    if nextNode:
                        nextNode = nextNode.next
                    else:
                        break
                elif startNode:
                    if counter == right and not endNode:
                        endNode = temp
                        NodeAfterEnd = temp.next
                        temp.next = prevNode
                        if NodeBeforeStart:
                            NodeBeforeStart.next = endNode
                        startNode.next = NodeAfterEnd
                        break
                    else:
                        temp.next = prevNode
                        prevNode = temp
                        temp = nextNode
                        counter += 1
                        if nextNode:
                            nextNode = nextNode.next
                        else:
                            if NodeBeforeStart:
                                NodeBeforeStart.next = prevNode
                            startNode.next = temp    
                            break
                else:
                    prevNode = temp
                    temp = nextNode
                    counter += 1
                    if nextNode:
                        nextNode = nextNode.next
                    else:
                        break
                    
            if startNode == head:
                return endNode
            else:
                return head


if __name__ == "__main__":
    sol = Solution()

    LinkedList = list(map(int, input().split()))
    left, right = list(map(int, input().split()))
    head = createLinkedList(LinkedList)
    #printLinkedList(head)
    t1 = time.time()
    printLinkedList(sol.reverseLinkedListInGivenPortion(head, left, right))
    print("%.6f" % (time.time() - t1))

    # LinkedList = list(map(int, input().split()))
    # head = createLinkedList(LinkedList)
    # t1 = time.time()
    # printLinkedList(sol.reverseLinkedList2(head))
    # print("%.6f" % (time.time() - t1))