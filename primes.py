""""""

from __future__ import annotations

__author__ = ''
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():

    def __init__(self, upper_bound: int, factor: int) -> None:
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self):
        return self
    
    def __next__(self):
        new_prime = self.largest_prime(self.upper_bound)
        self.upper_bound = new_prime * self.factor
        
        return new_prime


    def largest_prime(self, number: int) -> int:
        """ Using the sieve of eratosthenes """

        numbers = list(range(2, number))

        for prime_candidate in numbers:
            trial_prime = prime_candidate * prime_candidate
            while trial_prime <= number:

                if trial_prime in numbers:
                    numbers.remove(trial_prime)
                
                trial_prime += prime_candidate
        
        return numbers[-1]
