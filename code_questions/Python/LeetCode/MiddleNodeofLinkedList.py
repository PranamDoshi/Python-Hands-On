from DataStructures.LinkdedListFunctions import ListNode, createLinkedList, printLinkedList
class MiddleNode:
    
    def middleNode(self, head):
        if not head or not head.next:
            return head
        else:
            seenNodes = []
            temp, nodeCounter = head, 0
            
            while temp.next:
                print(temp.val, nodeCounter, len(seenNodes))
                nodeCounter += 1
                seenNodes.append(temp)
                temp = temp.next
            
            print(temp.val, nodeCounter, len(seenNodes))
            nodeCounter += 1
            seenNodes.append(temp)
            print(temp.val, nodeCounter, len(seenNodes))
            
            return seenNodes[nodeCounter // 2]


if __name__ == "__main__":
    sol = MiddleNode()

    lst = [1, 2, 3, 4, 5]
    head = createLinkedList(lst)

    printLinkedList(head)
    printLinkedList(sol.middleNode(head))