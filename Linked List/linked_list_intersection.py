# Intersection point of two Linked Lists
# https://www.geeksforgeeks.org/dsa/write-a-function-to-get-the-intersection-point-of-two-linked-lists/
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def getIntersectionNode(headA, headB):
    if not headA or not headB:
        return None

    # Find the length of both lists
    lenA = 0
    current = headA
    while current:
        lenA += 1
        current = current.next

    lenB = 0
    current = headB
    while current:
        lenB += 1
        current = current.next

    # Align the starting points of both lists
    diff = abs(lenA - lenB)
    if lenA > lenB:
        for _ in range(diff):
            headA = headA.next
    else:
        for _ in range(diff):
            headB = headB.next

    # Traverse both lists simultaneously until intersection is found or end is reached
    while headA and headB:
        if headA == headB:
            return headA
        headA = headA.next
        headB = headB.next

    return None


# execute this script to test the function 
if __name__ == "__main__":
    # Create nodes for list A
    a1 = ListNode(3)
    a2 = ListNode(2)
    a3 = ListNode(4)
    a1.next = a2
    a2.next = a3

    # Create nodes for list B
    b1 = ListNode(6)
    b2 = ListNode(5)
    b1.next = b2
    # Make list B intersect with list A at node a2
    b2.next = a2

    # Find intersection
    intersection_node = getIntersectionNode(a1, b1)

    if intersection_node:
        print("Intersection found at node with value:", intersection_node.val)
    else:
        print("No intersection found.")
