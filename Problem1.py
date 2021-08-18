import collections

class LRU_Cache(object):

    def __init__(self, capacity):
        self.cache = collections.OrderedDict()
        self.max_entries = capacity

    def __str__(self):
        string = 'Cache Contents: \n===============\n'
        index = 1

        for (key, value) in self.cache.items():
            string += '[{}] {} : {}\n'.format(index, key, value)
            index += 1

        return string

    def get(self, key):
        # Retrieve item from provided key. Return None if nonexistent.
        result = self.cache.pop(key, None)

        if result is None:
            return -1
        else:
            self.cache[key] = result
            return result

    def set(self, key, value):
        # Set the value if the key is not present in the cache.
        # If the cache is at capacity remove the oldest item, before proceeding
        # to update key's value.
        result = self.get(key)

        if self.max_entries > 0:
            if result == -1:
                # adding in a new key,value pair to the dictionary, check if capacity is reached
                if len(self.cache.items()) == self.max_entries:
                    self.cache.pop(next(iter(self.cache)))

            self.cache[key] = value
        else:
            print("Cache does not have a valid size.")




our_cache = LRU_Cache(5)

our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(3, 3)
our_cache.set(4, 4)


print(our_cache.get(1))
# expected:  1
print(our_cache.get(2))
# expected:  2
print(our_cache.get(9))
# expected: -1

our_cache.set(5, 5)
our_cache.set(6, 6)
our_cache.set(-1, -1)

print(our_cache.get(3))
# expected: -1 because the cache reached it's capacity and 3 was the LRU

print(our_cache)

small_cache = LRU_Cache(-1)

small_cache.set(1, 1)
# expected: Cache does not have a valid size.

large_cache = LRU_Cache(1000000000000000000000000000000000000000000000000000000)

large_cache.set(1, 1)

print()
print(large_cache)
# expected: [1] 1 : 1
