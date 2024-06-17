"""
https://leetcode.com/problems/swap-nodes-in-pairs/
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self) -> str:
        return f"{self.val}_{self.next.val if self.next else 'None'}"

class Solution:

    def swapPairs(self, head: ListNode) -> ListNode:
        """
        1 -> 2 -> 3 -> 4
        head=1 ==>
        --- Sample Iteraton
        next = head.next - 2
        head = next - 1
        next_to_next = next.next - 3
        next.next = head - 2 -> 1
        head.next = next_to_next - 1 -> 3
        2 -> 1 -> 3 -> 4
        ---
        while next_to_next:
            #iterate
        """
        if (not head) or (not head.next):
            return head

        temp = ListNode(0, head)
        prev = temp
        curr = head

        print(temp)
        print(prev)
        print(curr)

        while curr and curr.next:
            """
            1 -> 2
            prev=0,curr=1 ==>
            next_node=2
            curr.next=None
            next_node.next=1

            """
            print("---------------")
            next_node = curr.next
            print(next_node)
            curr.next = next_node.next
            print(curr)
            next_node.next = prev.next
            print(next_node)
            prev.next = next_node
            print(prev)

            if curr:
                print(prev)
                prev = curr
                print(curr)
                curr = curr.next
                print(curr)
            else:
                break

            print_linked_list(temp.next)

        return temp.next

def prep_linked_list(lst: list):
    if not lst:
        return None

    head = ListNode(lst[0])
    idx = 1
    temp_node = head
    while idx < len(lst):
        temp_node.next = ListNode(lst[idx])
        temp_node = temp_node.next
        idx += 1

    return head

def print_linked_list(head: ListNode):
    if not head:
        return
    
    temp = head
    while temp:
        print(temp.val, end=' ')
        if temp.next:
            print('->', end=' ')
            temp = temp.next

        else:
            break

    print()

if __name__ == "__main__":
    head = prep_linked_list([1,2,3,4,5])
    print_linked_list(head)

    sol = Solution()
    print_linked_list(sol.swapPairs(head))
