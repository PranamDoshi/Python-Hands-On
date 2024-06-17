from LinkdedListFunctions import ListNode, printLinkedList, insertElement, createLinkedList
class Solution:

    def removeElements(self, head, value):
        while head !=  None and head.val == value:
            matchingNode = head
            head = head.next
            del matchingNode
        
        temp = head

        if temp != None:
            answerHead = temp
            while temp.next:
                # printLinkedList(temp)
                # print(temp.val, temp.next.val)
                if temp.next.val == value:
                    matchingNode = temp.next
                    temp.next = temp.next.next
                    del matchingNode
                    
                    while temp.val == value:
                        matchingNode = temp
                        temp = temp.next
                        del matchingNode
                        if temp == None:
                            break
                else:
                    temp = temp.next
                    
                if temp.val == value:
                    matchingNode = temp
                    temp = None
                    del matchingNode

            return answerHead
        else:
            return None
        

if __name__ == "__main__":
    sol = Solution()

    LinkedList = list(map(int, input().split()))
    value = int(input())
    head = createLinkedList(LinkedList)

    printLinkedList(sol.removeElements(head, value))