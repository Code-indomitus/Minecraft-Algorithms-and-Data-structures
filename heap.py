"""Max Heap implemented using an array"""
from __future__ import annotations
from typing import Generic
from referential_array import ArrayR, T

__author__ = "Brendon Taylor, modified by Jackson Goerner and Rachit Bhatia"
__docformat__ = 'reStructuredText'


class MaxHeap(Generic[T]):
    """
    Class consists of functions and attributes required for the setup of a Max Heap. 
    This class sets the Max Heap elements in a 'key, value' format where the keys are 
    used to organise the structure of the heap.
    """

    MIN_CAPACITY = 1

    def __init__(self, max_size: int, an_array : ArrayR[T] = None) -> None:
        """
        Creates a Max Heap object. If an array is passed as a parameter, a Bottom-up Max Heap is set up using the array.

        :param max_size: the number of nodes to be created in the heap
        :param an_array: the array of key, value pairs used for creation of a bottom-up heap
        :complexity: complexity for creating a Bottom-up heap: Best-case = Worst-case = O(max_size), where max_size 
                     will represent the number of nodes in the heap.
        """

        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)
        self.length = max_size

        if an_array is not None:

            # copy an_array to self.the_array (shift by 1)
            for i in range(self.length):    #complexity: O(max_size)
                self.the_array[i+1] = an_array[i]
                
            # heapify every parent
            for i in range(max_size//2,0,-1):   #complexity: O(max_size/2)
                self.sink(i)

            #total complexity: O(max_size + max_size/2) = O(max_size)

    def __len__(self) -> int:
        """
        Return the number of nodes in the heap.
        """
        return self.length

    def is_full(self) -> bool:
        """
        Return True if heap is full, False otherwise.
        """
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length

        :complexity: Best-case = O(1)*O(comparison) when the item is the smallest
                     Worst-case = O(log N)*O(comparison) where is N is the number of nodes in the heap. 
                                  This case will be when the item is the largest and needs to 
                                  be raised all the way to the top.
        """
        item = self.the_array[k]
        while k > 1 and item[0] > self.the_array[k // 2][0]:  #comparing element [0] since it is the key
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def add(self, element: T) -> bool:
        """
        Swaps elements while rising

        :complexity: same complexity as self.rise() since all other operations in this function are O(1) 
                     Best-case = O(1)*O(comparison) when the item is the smallest (same as self.rise() complexity)
                     Worst-case = O(log N)*O(comparison) where is N is the number of nodes in the heap. 
                                  This case will be when the item is the largest and needs to 
                                  be raised all the way to the top.
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.
        :pre: 1 <= k <= self.length // 2

        :complexity: Best-case = Worst-case = O(1)
        """
        
        if 2 * k == self.length or \
                self.the_array[2 * k][0] > self.the_array[2 * k + 1][0]: #comparing element [0] since it is the key
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position.
            :pre: 1 <= k <= self.length

            :complexity: Best-case = O(1)*O(comparison) when the element is greater than or equal to one of its children
                         Worst-case = O(log N)*O(comparison) where is N is the number of nodes in the heap. 
                                      This case will be when the element is the smallest and needs to 
                                      be pushed all the way to the bottom.
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            max_child = self.largest_child(k)
            if self.the_array[max_child][0] <= item[0]: #comparing element [0] since it is the key
                break
            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item
        
    def get_max(self) -> T:
        """ Remove (and return) the maximum element from the heap. 

            :complexity: same complexity as self.sink() since all other operations in this function are O(1) 
                         Best-case = O(1)*O(comparison) when the element is greater than or equal to one of its children
                         Worst-case = O(log N)*O(comparison) where is N is the number of nodes in the heap. 
                                      This case will be when the element is the smallest and needs to 
                                      be pushed all the way to the bottom.
        """
        if self.length == 0:
            raise IndexError

        max_elt = self.the_array[1]
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length+1]
            self.sink(1)
        return max_elt


if __name__ == '__main__':
    items = [ int(x) for x in input('Enter a list of numbers: ').strip().split() ]
    heap = MaxHeap(len(items))

    for item in items:
        heap.add(item)
        
    while(len(heap) > 0):
        print(heap.get_max())
