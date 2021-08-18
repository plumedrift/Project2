import hashlib
import datetime


class Block:

    def __init__(self, timestamp, data, previous_hash=0, next_block=None):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()
        self.next = next_block
        self.prev = None

    def calc_hash(self):
        sha = hashlib.sha256()

        hash_str = (self.data + ' ' + self.timestamp).encode('utf-8')

        sha.update(hash_str)

        return sha.hexdigest()


class Blockchain:

    def __init__(self, head=None):
        self.head = head
        self.tail = head

    def __str__(self):
        output = 'Blockchain Contents:\n'
        cur = self.head

        while cur:
            output += '({}, {}) : (prev: {})\n'.format(cur.data, cur.timestamp, cur.previous_hash)
            cur = cur.next

        return output

    def add_block(self, block):

        if not self.tail:
            self.head = block
            self.tail = block
            return

        block.prev = self.tail
        block.previous_hash = self.tail.hash

        self.tail.next = block
        self.tail = block


timestamp = 'Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
data = 'Testing1'
unit1 = Block(timestamp, data)

timestamp = 'Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
data = 'Testing2'
unit2 = Block(timestamp, data)

timestamp = 'Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
data = 'Testing3'
unit3 = Block(timestamp, data)

chain = Blockchain()

print(chain)  # expected: empty chain

chain.add_block(unit1)
chain.add_block(unit2)
chain.add_block(unit3)

print(chain)  # expected: 3 different blocks, even though timestamp is the same
