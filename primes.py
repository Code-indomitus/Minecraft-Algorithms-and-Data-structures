"""
An iterator of the largest prime number to find the next greatest prime under a bound.
"""

from __future__ import annotations

__author__ = 'Shyam Kamalesh Borkar'
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    """ Iterator to find the next largest prime smaller than an upper bound."""

    def __init__(self, upper_bound: int, factor: int) -> None:
        """ Initialise the iterator object.
        :param upper_bound: the upper_bound under which the largest prime is found
        :praram factor: the factor that is used to update the upper_bound every call
        :complexity: Best and worst case O(1)
        """
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self):
        """Magic method to make class iterable
        :complexity: Best and worst case O(1)
        """
        return self
    
    def __next__(self):
        """Magic method to get the next item in the iterable object
        :complexity: Best and worst case O(1)
        """
        new_prime = self.largest_prime(self.upper_bound)
        self.upper_bound = new_prime * self.factor
        
        return new_prime


    def largest_prime(self, number: int) -> int:
        """ Using the sieve of eratosthenes get the largest prime number under bound
        :param number: the bound under which the list of prime numbers are generated
        :returns: the largest prime under the bound
        :complexity: Best and worst case O(n^2) where n is number, the upper bound
        """

        numbers = list(range(2, number))

        for prime_candidate in numbers:
            trial_prime = prime_candidate * prime_candidate
            while trial_prime <= number:

                if trial_prime in numbers:
                    numbers.remove(trial_prime)
                
                trial_prime += prime_candidate
        
        return numbers[-1]
