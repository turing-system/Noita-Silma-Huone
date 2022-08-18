# -*- coding: utf-8 -*-
""" Monoalphabetical cipher analysis

The first thing we find is the eye enigma isn't a
simple monoalphabetical cipher, as the index of
coincidance [IoC] is the same than random values.

We use here the first cryptography manual of Friedman
as main reference for terms and methodology:
https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/military-cryptanalysis/mil_crypt_I.pdf

But IoC work in following cases:
    * Simple subsitution (1p:1c),
    * Simple transposition (= suffle the cryptograph)
    * polyliteral monoalphabetical ciphers (1p:Nc). Require considerate group of
        size N as single symbole.
And doesn't work on following cases:
    * polygraph monoalphabetical ciphers (Np:1c)

We will test the following:
    1. Confirm that IoC work for simple polyliteral monoalphabetical
        over large alphabet (1p:Nc).
        Result : It does
    2. Confirm that IoC work for polygraph monoalphabetical cipher (Mp:Nc).
        Result : It doesn't
"""
import random

import numpy as np
from matplotlib import pyplot as plt

from constant.message import eyes_messages_as_whole

from analysis.ioc import ioc

if __name__ == "__main__":
    # Here is a small plaintext that will be used as control element
    plain_control = None
    with open("./analysis/control.txt", "r", encoding="utf-8") as control_file:
        plain_control = control_file.read().lower()


    # [1. Confirm that IoC work for simple substitution over large alphabet.]
    symbols = list(range(83))

    # Build random ioc
    crypto_random = random.choices(symbols, k=len(plain_control))
    ioc_random = ioc(crypto_random)

    # Build control ioc
    plaintext_alphabet = np.unique(list(plain_control))
    assert len(symbols) > len(plaintext_alphabet)
    map_plain_to_crypto = {
        plaintext_alphabet[i % len(plaintext_alphabet)]: symbol
        for i, symbol in enumerate(symbols)
    }
    crypto_control = [map_plain_to_crypto[plain_chr] for plain_chr in plain_control]
    ioc_control = ioc(crypto_control)

    # Build Eyes ioc
    ioc_eyes = ioc(eyes_messages_as_whole)

    # Display results
    print("Monoalphabetical cipher profile")
    print(f"\tioc_random = {ioc_random}")
    print(f"\tioc_control = {ioc_control}")
    print(f"\tioc_eyes = {ioc_eyes}")
    print(f"\tioc_control/ioc_random = {ioc_control/ioc_random}")
    print(f"\tioc_eyes/ioc_random = {ioc_eyes/ioc_random}")


    # [2. Confirm that IoC work for polygraph monoalphabetical cipher. (Mp:Nc)]
    possibles_pair = []
    for i in range(len(plain_control)//2):
        if len(plain_control) -1 == i:
            possibles_pair.append(plain_control[i] + " ")
        else:
            possibles_pair.append(plain_control[i] + plain_control[i+1])
    plaintext_alphabet = np.unique(possibles_pair)
    symbols = list(range(83))
    assert len(symbols) <= len(plaintext_alphabet)
    map_plain_to_crypto = {
        alpha: symbols[i % len(symbols)]
        for i, alpha in enumerate(plaintext_alphabet)
    }
    crypto_control = []
    for i in range(len(plain_control)//2):
        if len(plain_control) -1 == i:
            crypto_control.append(map_plain_to_crypto[plain_control[i] + " "])
        else:
            crypto_control.append(map_plain_to_crypto[plain_control[i] + plain_control[i+1]])
    ioc_control = ioc(crypto_control)

    # Display result
    print("Polygraph monoalphabetical cipher profile")
    print(f"\tlen(plaintext_alphabet) = {len(plaintext_alphabet)}")
    print(f"\tlen(symbols) = {len(symbols)}")
    print(f"\tioc_control = {ioc_control}")
    print(f"\tioc_control/ioc_random = {ioc_control/ioc_random}")

    # Compare sorted count of symbols
    figure, axis = plt.subplots(1, 1)

    eye_bins = np.bincount(eyes_messages_as_whole, minlength=83)
    eye_binsort = np.argsort(eye_bins)
    eye_x = eye_bins[eye_binsort].nonzero()[0]

    control_bins = np.bincount(crypto_control, minlength=83)
    control_binsort = np.argsort(control_bins)
    control_x = control_bins[control_binsort].nonzero()[0]

    random_bins = np.bincount(crypto_random, minlength=83)
    random_binsort = np.argsort(random_bins)
    random_x = random_bins[random_binsort].nonzero()[0]

    width = 0.3

    axis.bar(
        eye_x + width * 1,
        eye_bins[eye_binsort][eye_x],
        width=width,
        label = "Eye",
    )
    axis.bar(
        random_x + width * 2,
        random_bins[random_binsort][random_x],
        width=width,
        label="Random",
    )
    axis.bar(
        control_x + width * 3, 
        control_bins[control_binsort][control_x],
        width=width,
        label="Control (Polygraph monoalphabetical cipher)",
    )
    axis.set_xlabel("Order by count")
    axis.set_ylabel("Count")

    axis.legend()

    plt.show()