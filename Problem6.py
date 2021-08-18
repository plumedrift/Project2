class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string

    # updated to O(1) run-time with tail reference
    def append(self, value):

        if self.head is None:
            self.head = Node(value)
            self.tail = self.head
            self.size = 1
            return

        node = self.tail
        node.next = Node(value)
        self.tail = self.tail.next
        self.size += 1

    def contains(self, key):
        cur = self.head

        while cur:
            if cur.value == key:
                return True
            cur = cur.next

        return False


def union(llist_1, llist_2):
    union_list = LinkedList()

    cur = llist_1.head
    while cur:
        if not union_list.contains(cur.value):  # ensure uniqueness
            union_list.append(cur.value)  # O(1) with tail reference

        cur = cur.next

    cur = llist_2.head
    while cur:
        if not union_list.contains(cur.value):  # ensure uniqueness
            union_list.append(cur.value)  # O(1) with tail reference

        cur = cur.next

    if union_list.size == 0:  # guard the edge case
        return None

    return union_list


def intersection(llist_1, llist_2):
    intersect_list = LinkedList()

    # Find the smaller list - O(1) with size reference
    if llist_1.size <= llist_2.size:
        iter_list = llist_1
        searched_list = llist_2
    else:
        iter_list = llist_2
        searched_list = llist_1

    cur = iter_list.head
    while cur:
        if searched_list.contains(cur.value) \
                and not intersect_list.contains(cur.value):  # ensure uniqueness
            intersect_list.append(cur.value)  # O(1) with tail reference

        cur = cur.next

    if intersect_list.size == 0:  # guard the edge case
        return None

    return intersect_list


# Test case 1

linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3, 2, 4, 35, 6, 65, 6, 4, 3, 21]
element_2 = [6, 32, 4, 9, 6, 1, 11, 21, 1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

print(union(linked_list_1, linked_list_2))
# expected: 3 -> 2 -> 4 -> 35 -> 6 -> 65 -> 21 -> 32 -> 9 -> 1 -> 11 ->
print(intersection(linked_list_1, linked_list_2))
# expected: 6 -> 4 -> 21 ->
print()

# Test case 2

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3, 2, 4, 35, 6, 65, 6, 4, 3, 23]
element_2 = [1, 7, 8, 9, 11, 21, 1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print(union(linked_list_3, linked_list_4))
# expected: 3 -> 2 -> 4 -> 35 -> 6 -> 65 -> 23 -> 1 -> 7 -> 8 -> 9 -> 11 -> 21 ->
print(intersection(linked_list_3, linked_list_4))
# expected: None
print()

# Test case 3

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = []
element_2 = [9999999999, 999999999, 99999999]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print(union(linked_list_3, linked_list_4))
# expected: 9999999999 -> 999999999 -> 99999999 ->
print(intersection(linked_list_3, linked_list_4))
# expected: None
print()

# Test case 4

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = []
element_2 = []

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print(union(linked_list_3, linked_list_4))
# expected: None
print(intersection(linked_list_3, linked_list_4))
# expected: None
