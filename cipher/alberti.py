# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import deque


class Alberti():
    """ Alberti Cipher Encoder/Decoder
    
    Features:
        * alphabet_plain may include multiple time the same char, in that case
            it's mean the same char can have multiple output.
        * `process()` can handle different shift rotation.

    Args:
        alphabet_cipher (str):
            The list of output symbol, must be of the same length than `alphabet_plain`.
            Is the key. Each char must be unique in the string
        alphabet_plain (str):
            The list of input symbol, must be of the same length than `alphabet_plain`.
    """

    def __init__(self, alphabet_cipher, alphabet_plain):
        assert isinstance(alphabet_cipher, str)
        assert isinstance(alphabet_plain, str)
        assert len(alphabet_cipher) == len(alphabet_plain)
        assert len(set(alphabet_cipher)) == len(alphabet_cipher)  # unique check
        self.alphabet_cipher = alphabet_cipher
        self.alphabet_plain = alphabet_plain

    def build_encode_dict(self, shift=0):
        """ Build a dict as plain char → [possible cipher char] """
        convert_dict = defaultdict(list)
        
        for i, char in enumerate(self.alphabet_plain):
            convert_dict[char].append(self.alphabet_cipher[(i+shift) % len(self.alphabet_cipher)])

        return dict(convert_dict)

    def build_decode_dict(self, shift=0):
        """ Build a dict as cipher char → plain char """
        convert_dict = defaultdict(list)
        
        for i, char in enumerate(self.alphabet_plain):
            convert_dict[self.alphabet_cipher[(i+shift) % len(self.alphabet_cipher)]] = char

        return dict(convert_dict)

    def encode(self, plain, shift_definitions:"list[tuple[int, int]]"=[]):
        """ Encode plain text to cipher text

        Args:
            * plain (str): the plain string to treat
            * shift_definitions (list[tuple[int, int]]):
                list of tuple as following: first element is the position
                where occurs the shift, the second one is how long the
                shift is.
                First element of each tuple must be unique.
        Return:
            (str) cipher string
        """

        output = deque()
        encode_dict = self.build_encode_dict(0)

        shifts = sorted(shift_definitions, key=lambda t: t[0])
        shifts_cursor = sum(shift_def[0] < 0 for shift_def in shift_definitions)
        current_shift = 0

        # Build a cursor for each plain text in order to use variant output char
        # evenly
        cursor_dict = { k:0 for k in encode_dict }
        for i, char in enumerate(plain):

            # Find next shift
            if (shifts_cursor < len(shifts) 
                and shifts[shifts_cursor][0] == i
            ):
                current_shift += shifts[shifts_cursor][1]
                encode_dict = self.build_encode_dict(current_shift)
                shifts_cursor += 1

            output.append(encode_dict[char][cursor_dict[char] % len(encode_dict[char])])
            cursor_dict[char] += 1

        return ''.join(output)

    def decode(self, cipher, shift_definitions:"list[tuple[int, int]]"=[]):
        """ Decode cipher text to plain text

        Args:
            * cipher (str): the plain string to treat
            * shift_definitions (list[tuple[int, int]]):
                list of tuple as following: first element is the position
                where occurs the shift, the second one is how long the
                shift is.
                First element of each tuple must be unique.
        Return:
            (str) plain string
        """

        output = deque()
        decode_dict = self.build_decode_dict(0)

        shifts = sorted(shift_definitions, key=lambda t: t[0])
        shifts_cursor = sum(shift_def[0] < 0 for shift_def in shift_definitions)
        current_shift = 0

        for i, char in enumerate(cipher):
            # Find next shift
            if (shifts_cursor < len(shifts) 
                and shifts[shifts_cursor][0] == i
            ):
                current_shift += shifts[shifts_cursor][1]
                decode_dict = self.build_decode_dict(current_shift)
                shifts_cursor += 1
            
            output.append(decode_dict[char])

        return ''.join(output)