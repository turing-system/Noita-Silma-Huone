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

    def encode(self, plain, shift_initial=0, shift_stall=1, shift_step=1):
        """ Encode plain text to cipher text

        Args:
            * plain (str): the plain string to treat
            * shift_initial (int): Initial shift of the cipher alphabet
            * shift_stall (int): Number of char convert without shift
            * shift_step (int): How much the cipher alphabet is shifted after stall
        Return:
            (str) cipher string
        """
        assert shift_initial >= 0
        assert shift_stall >= 1
        assert shift_step >= 1

        output = deque()

        current_shift = shift_initial
        encode_dict = self.build_encode_dict(current_shift)

        # Build a cursor for each plain text in order to use variant output char
        # evenly
        cursor_dict = { k:0 for k in encode_dict }

        for i, char in enumerate(plain):
            output.append(encode_dict[char][cursor_dict[char] % len(encode_dict[char])])
            cursor_dict[char] += 1

            if i % shift_stall == 0 and i > 0:
                current_shift += shift_step
                encode_dict = self.build_encode_dict(current_shift)

        return ''.join(output)

    def decode(self, cipher, shift_initial=0, shift_stall=1, shift_step=1):
        """ Decode cipher text to plain text

        Args:
            * cipher (str): the plain string to treat
            * shift_initial (int): Initial shift of the cipher alphabet
            * shift_stall (int): Number of char convert without shift
            * shift_step (int): How much the cipher alphabet is shifted after stall
        Return:
            (str) plain string
        """
        assert shift_initial >= 0
        assert shift_stall >= 1
        assert shift_step >= 1

        output = deque()

        current_shift = shift_initial
        decode_dict = self.build_decode_dict(current_shift)

        for i, char in enumerate(cipher):
            output.append(decode_dict[char])

            if i % shift_stall == 0 and i > 0:
                current_shift += shift_step
                decode_dict = self.build_decode_dict(current_shift)

        return ''.join(output)