from LinkdedListFunctions import ListNode, printLinkedList, createLinkedList

class RemoveFromEnd:

    def removeNthFromEnd(self, head, n):
        if not head or (not head.next and n == 1):
            return None
        elif not head.next and n > 1:
            return head
        else:
            seenNode = []
            temp = head

            while temp.next:
                seenNode.append(temp)
                temp = temp.next
            seenNode.append(temp)

            if n > len(seenNode):
                return head
            elif n == len(seenNode):
                return head.next
            else:
                if -n + 1 < 0:
                    seenNode[-n - 1].next = seenNode[-n+1]
                else:
                    seenNode[-n - 1].next = None
                return head


if __name__ == "__main__":
    sol = RemoveFromEnd()

    LinkedList = list(map(int, input().split()))
    head = createLinkedList(LinkedList)
    n = int(input())

    printLinkedList(sol.removeNthFromEnd(head, n))