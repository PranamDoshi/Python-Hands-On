from LinkdedListFunctions import insertElement, createLinkedList, printLinkedList

class Solution:

    def addTwoNumbers(self, l1, l2):
        carryValue = 0
        carryFlag = False
        ansHead = None
        ansTemp = None

        while l1 and l2:
            if l1 and l2:
                if carryFlag:
                    addValue = l1.val + l2.val + carryValue
                    carryFlag = False
                else:
                    addValue = l1.val + l2.val
            elif not l1 and l2:
                if carryFlag:
                    addValue = l2.val + carryValue
                    carryFlag = False
                else:
                    addValue = l2.val
            elif not l2 and l1:
                if carryFlag:
                    addValue = l1.val + carryValue
                    carryFlag = False
                else:
                    addValue = l1.val
            if addValue > 9:
                carryFlag = True
                carryValue = addValue // 10
                addValue = addValue - (carryValue*10)
            
            ansHead, ansTemp = insertElement(ansHead, ansTemp, addValue)
            l1 = l1.next
            l2 = l2.next
        
        while l1:
            if carryFlag:
                addValue = l1.val + carryValue
                carryFlag = False
            else:
                addValue = l1.val
            
            if addValue > 9:
                carryFlag = True
                carryValue = addValue // 10
                addValue = addValue - (carryValue*10)

            ansHead, ansTemp = insertElement(ansHead, ansTemp, addValue)
            l1 = l1.next

        while l2:
            if carryFlag:
                addValue = l2.val + carryValue
                carryFlag = False
            else:
                addValue = l2.val
            
            if addValue > 9:
                carryFlag = True
                carryValue = addValue // 10
                addValue = addValue - (carryValue*10)
            
            ansHead, ansTemp = insertElement(ansHead, ansTemp, addValue)
            l2 = l2.next
            
        if carryFlag:
            carryFlag = False
            ansHead, ansTemp = insertElement(ansHead, ansTemp, carryValue)

        return ansHead


if __name__ == "__main__":
    sol = Solution()

    LinkedList1 = list(map(int, input().split()))
    head1 = createLinkedList(LinkedList1)

    LinkedList2 = list(map(int, input().split()))
    head2 = createLinkedList(LinkedList2)

    printLinkedList(sol.addTwoNumbers(head1, head2))