# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, val=0, next=None):

        self.val = val
        self.next = next


# [2,4,3]
# [5,6,4]

# [7,0,8]


def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:

    return func2(l1, l2)


def func1(l1: ListNode, l2: ListNode) -> ListNode:
    list1 = []
    list2 = []

    first_node = l1
    while first_node != None:
        list1.append(first_node.val)
        first_node = first_node.next

    second_node = l2
    while second_node != None:
        list2.append(second_node.val)
        second_node = second_node.next

    min_length = len(list2) if len(list1) > len(list2) else len(list1)
    max_length = len(list1) if len(list1) > len(list2) else len(list2)

    def next(index, carry):

        next_carry = 0
        if index < min_length:
            v = list1[index] + list2[index] + carry
            if v / 10 > 0:
                next_carry = 1
                v = v % 10
        else:

            if index >= max_length:
                if carry > 0:
                    v = carry
                else:
                    return
            else:
                if max_length == len(list1):
                    v = list1[index] + carry
                else:
                    v = list2[index] + carry
                if v / 10 > 0:
                    next_carry = 1
                    v = v % 10

        node = ListNode(v)
        next_node = next(index + 1, next_carry)
        node.next = next_node

        return node

    result = next(0, 0)
    return result


def func2(l1: ListNode, l2: ListNode) -> ListNode:

    new_node = ListNode()
    result = new_node
    carry = 0
    while l1 or l2:

        new_node.next = ListNode()
        new_node = new_node.next

        if l1:
            new_node.val += l1.val
            l1 = l1.next
        if l2:
            new_node.val += l2.val
            l2 = l2.next

        new_node.val += carry
        carry = new_node.val // 10
        if carry:
            new_node.val = new_node.val % 10
    else:
        if carry:
            new_node.next = ListNode(carry)

    return result.next


def test():

    l1 = ListNode(2)
    l1_1 = ListNode(4)
    l1.next = l1_1
    l1_2 = ListNode(3)
    l1_1.next = l1_2

    l2 = ListNode(5)
    l2_1 = ListNode(6)
    l2.next = l2_1
    l2_2 = ListNode(4)
    l2_1.next = l2_2

    return addTwoNumbers(l1, l2)
