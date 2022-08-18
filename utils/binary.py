# -*- coding: utf-8 -*-
""" For binary specifics operations

Combinatories operations can often be simplify to n^m numbers to represent
all possibles combinations. As it's not native, we implement it here
"""

def generator_bin_words(words_length:int, bits_up_count:int):
    """ Generate all possibilities to a binary number with exactly
    `bits_up_count` bits up.
    
    Args:
        words_length (int): number of bits in the number
        bits_up_count (int) number of bits up in the number
    Return:
        (int) Yield each possibilities once (not ordered) 
    """

    def _recursive(from_bit=0, words_length=None, deepness=0):
        """ Recursivly generate a solution.
        
        Args:
            from_bit (int): from which bit he must build a solution.
            words_length (int): c.f. parent function
            deepness (int): recursive index, base 0
        Return:
            (int) solution from this point
        """
        for n in range(from_bit, words_length):
            if n == words_length-1:
                break
            if deepness == bits_up_count:
                return (1 << n)
            else:
                yield (1 << n) | _recursive(n+1, words_length, deepness=deepness+1)
    
    yield _recursive(0, words_length)