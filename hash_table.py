""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations
from primes import LargestPrimeIterator

__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, and Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'


from referential_array import ArrayR
from typing import TypeVar, Generic
T = TypeVar('T')


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def check_prime(self,num : int) -> bool:
        if num > 1:
        # Iterate from 2 to n / 2
            for i in range(2, int(num/2)+1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
                if (num % i) == 0:
                    return False
            else:
                return True
        else:
            return False


    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
        """
        self.count = 0
        self.tablesize = None

        if tablesize_override == -1 :
            if self.check_prime(expected_size) :
                self.tablesize = expected_size
            else :
                while not self.check_prime(expected_size):
                    expected_size += 1
                self.tablesize = expected_size    
        else : 
            self.tablesize = tablesize_override
        
        self.table = ArrayR(self.tablesize)


        self.conflict = 0   
        self.total_distance_probed = 0
        self.length_longest_probe = 0
        self.rehashing_count = 0


    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
        """
        value = 0
        a = 31415
        b = 27183
        for char in key:
            value = (ord(char) + a*value) % self.tablesize
            a = a*b %(self.tablesize-1)

    def statistics(self) -> tuple:
        return (self.conflict,self.total_distance_probed,self.length_longest_probe,self.rehashing_count)

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        conflict_counted = False

        distance_probed_current = 0

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                if is_insert :
                    if conflict_counted == False :
                        self.conflict += 1
                        conflict_counted = True

                    self.total_distance_probed += 1
                    distance_probed_current += 1

                    if distance_probed_current > self.length_longest_probe :
                        self.length_longest_probe = distance_probed_current

                position = (position + 1) % len(self.table)

        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
        """

        if self.count > ( self.tablesize // 2):
            self._rehash()
        
        position = self._linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1

        self.table[position] = (key, data)

    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values
        """
        self.rehashing_count += 1
        self.count = 0

        prime_iterator = LargestPrimeIterator(self.tablesize,2)

        next_1 = next(prime_iterator)
        new_table_size = next(prime_iterator)

        new_table = ArrayR(new_table_size)
        
        temp = []

        for item in self.table:
            if item is not None:
                temp.append(item)

        self.table = new_table

        for data in temp :
            if data is not None:
                self[data[0]] = data[1]

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
