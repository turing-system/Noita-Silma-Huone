# -*- coding: utf-8 -*-
""" This script is made up to build dictionnary file, based on wordnet one. """
from collections import deque
from nltk.corpus import wordnet


def get_words(only_range_len: "tuple[int, int]" = None):
    """ Get the list of words.
    
    Args:
        only_range_len (tuple(int, int)):
            A tuple of 2 values that define inclusive wanted word size.
            Let to None to avoid any filter.
    Return:
        (deque) list of strings
    """
    output = deque()
    # Add a word per line.
    # Wordnet include compose word with "_" instead of space.
    # Also include numbers and bullet standards
    # We're remove them.
    forbiden_chars = "_0123456789."
    words = wordnet.words()
    for word in words:
        # Filter by length
        if (
            only_range_len is not None
            and not only_range_len[0] < len(word) < only_range_len[1]
        ):
            continue

        # Filter by char
        is_found = False
        for forbinden_char in forbiden_chars:
            if forbinden_char in word:
                is_found = True
                break
        if is_found:
            continue

        # Valid word
        output.append(word)

    return output


if __name__ == "__main__":
    # Just write the output in the dict
    with open("./en_dict.txt", "w") as f:
        for word in get_words():
            f.write(word + "\n")
