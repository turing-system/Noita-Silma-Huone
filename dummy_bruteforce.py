# -*- coding: utf-8 -*-
""" The Nollagames Noita masterpiece Noita include a very difficult enigm, the eyes enigma

And we will bruteforce like wild animals.

Things taken in consideration to automate the discriminate of results:
    * `letters_frequencies` is here to help to identify gibbrish from text [unimplemented]
    * `digrams_occurrence` (e.g. "th" "rd") is here to help to identify gibbrish from text [unimplemented]
    * We assume the first char is a number, and as it's likely to define the texts order,
        the `plain_alphabet` must include "123456789" as it is.

We're focusing on word E1, W1 and E2 as they start the same way, we decode E1, check if it's
non-sense or not, and if relevant, we decode W1 and E2 to validate.

In order to reduce the number of possible key, we're assuming there is few existing blocks:
  * "ABCDEFGHIJKMNLOPQRSTUVWXYZ" 
  * "abcdefghijkmnlopqrstuvwxyz"
  * "123456789" (c.f. rule above)

As the cipher is a set of 83 abstract symbole, we're defining them as ASCII+32[0:82]
  and only manipulate the `plain_alphabet`

The rest of `plain_alphabet` is filled with null, with the hope that it allow us to
identify some words.

The position of fillers are defined by `mask_filler`
"""
from collections import defaultdict
from tqdm import tqdm

from alberti import Alberti
from dictionnary_generator import get_words
from statics.message import (
    E1,
    E2,
    W1,
)
# from statistics import (
#     letters_frequencies,
#     digrams_occurrence,
# )

def numberToBase(n, b):
    # Convert n to a list of number to simulate a base b
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

THESHOLD_PERCENT_WORD_CHECK_AS_FOUND = 0.5

if __name__ == "__main__":

    number_of_unique_cipher = 83
    cipher_alphabet = ''.join([chr(i+32) for i in range(number_of_unique_cipher)])


    upper_alphabet = "ABCDEFGHIJKMNLOPQRSTUVWXYZ"
    lower_alphabet = "abcdefghijkmnlopqrstuvwxyz"
    number_alphabet = "123456789"
    
    mask_size = number_of_unique_cipher - (
        len(upper_alphabet) +
        len(lower_alphabet) +
        len(number_alphabet)
    )

    # In which order fixed part are  (3 possibility)
    # We're suppose we can read both caps and lower likely
    fixed_part_available = [
        (upper_alphabet, lower_alphabet, number_alphabet),
        (upper_alphabet, number_alphabet, lower_alphabet),
        (number_alphabet, upper_alphabet, lower_alphabet),
    ]

    def generator_plain_alphabet(i):
        """ This generator i → plain_alphabet allow
        to avoid to store the full plain_alphabet but i instead.

        Require less space on disk.
        """

        # Where are fillers (22^4 possibility)
        # Written as a base4 digit (as a list of int)
        mask_filler_unpadded = numberToBase(i, 4)[::-1]
        mask_filler = mask_filler_unpadded + [0] * (mask_size - len(mask_filler_unpadded))


        filler = defaultdict(lambda: 0)
        for d in mask_filler:
            filler[d] += 1

        fixed_pattern = fixed_part_available[(i // (mask_size**4)) % len(fixed_part_available)]

        # Note that filler are null in order to allow binary AND operator to ignore them
        # in the word check
        return ''.join([
            filler[0] * chr(0),
            fixed_pattern[0],
            filler[1] * chr(0),
            fixed_pattern[1],
            filler[2] * chr(0),
            fixed_pattern[2],
            filler[3] * chr(0),
        ])

    # Load main const

    E1_str = ''.join([chr(d+32) for d in E1])
    E2_str = ''.join([chr(d+32) for d in E2])
    W1_str = ''.join([chr(d+32) for d in W1])

    words_bytes = [bytearray(word, 'ascii') for word in get_words()]

    # ~ Main loop
    for i in tqdm(range( (mask_size**4) * len(fixed_part_available))):
    
        plain_alphabet = generator_plain_alphabet(i)

        # Someone notice that the shift should be around a multiple of 14
        # so I add 2. (yea, quite random, it's juste to avoid to pass too much time on it)
        max_shift_stall = 16
        max_shift_step = len(cipher_alphabet) -1

        cipher = Alberti(cipher_alphabet, plain_alphabet)

        for shift_stall in range(1, max_shift_stall):
            for shift_step in range(1, max_shift_step):
                for shift_initial in range(shift_stall):

                    e1_plain_candidate = cipher.decode(
                        cipher=E1_str,
                        shift_initial=shift_initial,
                        shift_step=shift_step,
                        shift_stall=shift_stall,
                    )

                    # If the first char isn't a number, skip to eco processor
                    if not 48 <= ord(e1_plain_candidate[0]) <= 57:
                        continue

                    e1_plain_candidate_bytes = bytearray(e1_plain_candidate, 'ascii')
                    
                    # We're counting how many word it may be in it
                    word_found_count = 0
                    for i, word_bytes in enumerate(words_bytes):
                        for bit_padding in range(len(e1_plain_candidate_bytes) - len(word_bytes)):
                            # Check if the word collide 
                            bit_colliding = (word_bytes << bit_padding) & e1_plain_candidate_bytes
                            if bit_colliding > 0:
                                # Check if at least half of bit(1) are colliding
                                bit_count_word = 0
                                bit_count_collide = 0
                                for in_word_bit_padding in range(word_bytes):
                                    if (1 << (in_word_bit_padding + bit_padding) and bit_colliding) > 1:
                                        bit_count_collide += 1
                                    if (1 << (in_word_bit_padding) and word_bytes) > 1:
                                        bit_count_word += 1

                                if bit_count_collide/bit_count_word > THESHOLD_PERCENT_WORD_CHECK_AS_FOUND:
                                    word_found_count += 1
                                    break
                    
                    # If there is no words in it, skip to eco processor
                    if word_found_count == 0:
                        continue

                    with open('output.dummy_bruteforce.txt', 'a') as f:
                        f.write(f"{i}\t{shift_initial}\t{shift_step}\t{shift_stall}\t{word_found_count}\n")
                    
