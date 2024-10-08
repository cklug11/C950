import csv

class ChainingHashTable:

    # initialize the hash table with empty bucket list entries.
    def __init__(self, initial_capacity=20):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def lookup(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]


        # search for the key in the bucket list
        for key_value in bucket_list:
            #print (key_value)
            if key_value[0] == key:
                return key_value[1] # value
        return None

    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present
        for key_value in bucket_list:
            #print (key_value)
            if key_value[0] == key:
                bucket_list.remove([key_value[0],key_value[1]])

