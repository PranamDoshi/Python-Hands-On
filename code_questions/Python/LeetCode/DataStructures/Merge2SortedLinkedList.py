class ListNode:

    def __init__(self, val = 0, next = None):
        self.val = val
        self.next = next


class Solution:

    def mergeTwoLists(self, list1, list2):
        if list1 == None:
            return list2
        elif list2 == None:
            return list1
        elif list1 == None and list2 == None:
            return ListNode()
        else:
            iNode, jNode = list1, list2
            output = []

            while iNode != None and jNode != None:                
                if iNode.val <= jNode.val:
                    output.append(iNode.val)
                    iNode = iNode.next
                    if iNode == None:
                        break
                else:
                    output.append(jNode.val)
                    jNode = jNode.next
                    if jNode == None:
                        break
            
            while iNode:
                output.append(iNode.val)
                iNode = iNode.next
                if iNode == None:
                    break
            
            while jNode:
                output.append(jNode.val)
                jNode = jNode.next
                if jNode == None:
                    break

            return createLinkedList(output)


class Solution1:

    def mergeTwoLists(cls, list1, list2):
        if list1 == None:
            return list2
        elif list2 == None:
            return list1
        elif list1 == None and list2 == None:
            return ListNode()
        else:
            if list1.val <= list2.val:
                list1.next = cls.mergeTwoLists(list1.next, list2)
                return list1
            else:
                list2.next = cls.mergeTwoLists(list2.next, list1)
            return list2


class Solution2:

    def mergerTwoLists(self, list1, list2):
        temp = ListNode()
        ansHead = temp

        while list1 and list2:
            if list1.val <= list2.val:
                temp.next = list1
                list1, temp = list1.next, list1
            else:
                temp.next = list2
                list2, temp = list2.next, list2
            
        if list1 or list2:
            temp.next = list1 if list1 else list2
        
        return ansHead.next


def createLinkedList(lst):
    root = ListNode()
    for i in lst:
        if root.val == 0:
            root.val = i
        elif root.next == None:
            tempNode = ListNode(i)
            root.next = tempNode
        else:
            tempNode.next = ListNode(i)
            tempNode = tempNode.next
    
    return root

if __name__ == "__main__":
    list1 = list(map(int, input().split()))
    list2 = list(map(int, input().split()))

    sol = Solution1()
    answer = sol.mergeTwoLists(createLinkedList(list1), createLinkedList(list2))

    #print Solution
    while answer:
        print(answer.val, end = ' ')
        answer = answer.next
        if answer == None:
            break