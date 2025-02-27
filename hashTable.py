#Creation of Hash Table STEP A1
#Hash Table created thanks to zybooks remember to cite correctly
#This hash table is based on the zybooks material for Hash tables...
#C 949: Data Structures and Algorithms I home > 15.10: Python: Hash tables
#Figure 15.10.2: ChainingHashTableItem and ChainingHashTable classes.
class HashTable:
    #Initialize the hash table with a capacity that covers what's needed in terms of amount of packages.
    def __init__(self, init_cap=45):
        self.table = []
        for i in range(init_cap):
            self.table.append([])

    def insertion(self, key, item):
        bucket_index = hash(key) % len(self.table)
        bucket_list = self.table[bucket_index]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                keyValue[1] = item
                return True

        new_key = [key, item]
        bucket_list.append(new_key)
        return True

    def delete(self, key):
        bucket_index = hash(key) % len(self.table)
        bucket_list = self.table[bucket_index]

        if key in bucket_list:
            bucket_list.remove(key)

    def lookup(self, key):
        bucket_index = hash(key) % len(self.table)
        bucket_list = self.table[bucket_index]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]
        return None