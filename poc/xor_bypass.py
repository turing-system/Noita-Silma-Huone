# -*- coding: utf-8 -*-
""" The Nollagames Noita masterpiece Noita include a very difficult enigm,
the eyes enigma.

And we will bruteforce like wild animals.

We will attempt to exploit here that a positionnal cipher use a xor
operation instead with the alphabet or a key.
And can be broke if the same key is used across multiple message.

If the above rule is true then E1 = (plain E1 XOR key)

We can demonstrate that as following:
(a XOR key) XOR (b XOR key) = (a XOR b) XOR (key XOR key) = (a XOR b)

As (a XOR b) XOR b = a, we have to find:
- or the key,
- or the plain version or b
to find a.

A plain text is easier to find than the key as plain text sentence are
rule by natural language.

We will compute the (a XOR b) for each message with E1 to have 9 XOR
message, then brute force message on E1 XOR E2.

The discriminate of the output will be done on digrams frequency check
of all 9 XOR messages.

======== Proof of concept ========
Fail, it's doesn't work with a non-XOR
usage. But the above prove is still valid
and may be quicker than other type of
bruteforce.
"""
from alberti import Alberti

plain_a = "ALSDKASDLKALKDSASDLKN"
plain_b = "NOWEQFBQWIBDSKFBAKSHD"

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

import random
cipher = Alberti(
    # Build random alphabet
    alphabet_cipher=''.join(random.sample(alphabet, len(alphabet))),
    alphabet_plain=''.join(random.sample(alphabet, len(alphabet))),
)

crypt_a = cipher.encode(plain_a)
crypt_b = cipher.encode(plain_b)

def xor_str(a, b):
    return ''.join([chr(ord(n) ^ ord(m)) for n, m in zip(a, b)])

assert xor_str(crypt_a, crypt_b) == xor_str(plain_a, plain_b)
assert xor_str(xor_str(crypt_a, crypt_b), plain_b) == plain_a