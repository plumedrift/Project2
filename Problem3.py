import sys


class Node:

    def __init__(self, character='', frequency=0, ht=None):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None
        self.huffman = ht

    def __str__(self):
        return '({}, {})'.format(self.character, self.frequency)


class minHeap:

    def __init__(self):
        self.root = None
        self.size = 0

    def recursive_print(self, node):
        if node:
            output = node.__str__()
            if node.left:
                output = self.recursive_print(node.left) + ' <- ' + output
            if node.right:
                output += ' -> ' + self.recursive_print(node.right)
            return output
        return ""

    def __str__(self):
        node = self.root

        return self.recursive_print(node)

    def swap(self, node1, node2):
        temp_char = node2.character
        temp_freq = node2.frequency
        temp_ht = node2.huffman

        node2.character = node1.character
        node2.frequency = node1.frequency
        node2.huffman = node1.huffman

        node1.character = temp_char
        node1.frequency = temp_freq
        node1.huffman = temp_ht

    def percolate_up(self, path_to_parent, child):
        parent = self.root

        if child == self.root:
            return

        for digit in path_to_parent:
            if digit == '0':
                parent = parent.left
            else:
                parent = parent.right

        if child.frequency < parent.frequency:
            self.swap(parent, child)
            self.percolate_up(path_to_parent[:-1], parent)

    def add_node(self, child):
        if not self.root:
            self.root = child
            self.size = 1
            return

        self.size += 1

        """Calculate location of next node by converting the new size to a binary representation.
            bin(num) returns a string starting in "0b" and the first digit after that is unused"""
        path = bin(self.size)[3:]
        parent = self.root

        for digit in path[:-1]:     # Stop on the last level
            if digit == '0':
                parent = parent.left
            else:
                parent = parent.right

        if path[-1] == '0':
            parent.left = child
        else:
            parent.right = child

        if child.frequency < parent.frequency:
            self.percolate_up(path[:-1], child)

    def pop_min(self):
        """Calculate location of next node by converting the new size to a binary representation.
            bin(num) returns a string starting in "0b" and the first digit after that is unused"""
        path_to_latest_child = bin(self.size)[3:]
        min = Node(self.root.character, self.root.frequency, self.root.huffman)
        explorer = self.root
        parent = self.root

        if self.size == 1:
            self.root = None
        else:
            for digit in path_to_latest_child:
                parent = explorer
                if digit == '0':
                    explorer = explorer.left
                else:
                    explorer = explorer.right

            # Remove what will be the root(lowest node) after swap on line 118
            if str(path_to_latest_child)[-1] == '0':
                parent.left = None
            else:
                parent.right = None

            self.swap(self.root, explorer)

            # Heapify: make sure the heap retains its properties, now that we have swapped a new node
            #   to the root
            node = self.root
            while node:
                if node.left and node.frequency > node.left.frequency:
                    self.swap(node, node.left)
                    node = node.left
                elif node.right and node.frequency > node.right.frequency:
                    self.swap(node, node.right)
                    node = node.right
                else:
                    break

        self.size -= 1

        return min


class huffman_Tree:

    def __init__(self, root=None):
        self.root = root
        self.left_child = None
        self.right_child = None

    def add_children(self, first, second):
        self.left_child = first
        self.right_child = second

    def gen_cipher_recursive(self, node, cipher, path):
        char = node.character
        if char:
            cipher[char] = path
        else:
            self.gen_cipher_recursive(node.huffman.left_child, cipher, path + "0")
            self.gen_cipher_recursive(node.huffman.right_child, cipher, path + "1")

        return

    """ Recursively fill a dictionary(cipher) with the codes as we traverse the huffman tree"""
    def gen_cipher(self, cipher):
        if self.left_child and self.right_child:
            self.gen_cipher_recursive(self.left_child, cipher, "0")
            self.gen_cipher_recursive(self.right_child, cipher, "1")
        else:
            return dict()


def huffman_encoding(data):
    output = ''
    min_heap = minHeap()
    freqs = dict()

    for char in data:
        if char not in freqs:
            freqs[char] = 1
        else:
            freqs[char] += 1

    for (key, value) in freqs.items():
        cur = Node(key, value)
        min_heap.add_node(cur)

    while min_heap.size > 1:  # while there are at least two elements in minHeap
        first = min_heap.pop_min()
        second = min_heap.pop_min()

        tree = huffman_Tree()
        tree.root = Node(frequency=first.frequency + second.frequency, ht=tree)

        tree.add_children(first, second)

        min_heap.add_node(tree.root)

    cipher = freqs.copy()
    tree = min_heap.root
    if tree:
        if tree.huffman:
            tree.huffman.gen_cipher(cipher)
        else:
            for key in cipher:
                cipher[key] = "0"

    for char in data:
        output += cipher.get(char)

    return output, tree


def huffman_decoding(data, tree):
    output = ''
    cur = tree

    if cur and cur.huffman:
        for bit in data:
            if bit == '0':
                cur = cur.huffman.left_child
            else:
                cur = cur.huffman.right_child

            if cur and cur.character:
                output += cur.character
                cur = tree
    else:  # there is no huffman tree, because there is only one letter
        if cur:
            for bit in data:
                output += cur.character


    return output


if __name__ == "__main__":
    test = "AAAAAAABBBCCCCCCCDDEEEEEE"

    encoded_data, tree = huffman_encoding(test)

    a_great_sentence = "The bird is the word"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))
    print("===================================================================================")

    a_smaller_sentence = ""

    print("The size of the data is: {}\n".format(sys.getsizeof(a_smaller_sentence)))
    print("The content of the data is: {}\n".format(a_smaller_sentence))

    encoded_data, tree = huffman_encoding(a_smaller_sentence)

    #print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))
    print("===================================================================================")

    the_greatest_sentence = "The important thing is not to stop questioning. Curiosity has its own reason for existing. One cannot help but be in awe when one contemplates the mysteries of eternity, of life, of the marvellous structure of reality."

    print("The size of the data is: {}\n".format(sys.getsizeof(the_greatest_sentence)))
    print("The content of the data is: {}\n".format(the_greatest_sentence))

    encoded_data, tree = huffman_encoding(the_greatest_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))
    print("===================================================================================")


    an_edgy_sentence = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    print("The size of the data is: {}\n".format(sys.getsizeof(an_edgy_sentence)))
    print("The content of the data is: {}\n".format(an_edgy_sentence))

    encoded_data, tree = huffman_encoding(an_edgy_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))
    print("===================================================================================")
