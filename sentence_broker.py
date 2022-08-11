# -*- coding: utf-8 -*-
""" We're probably seeking English or Finnish sentence,
So knowing the frequency of:
    * words by their position in a sentence,
    * words by the previous words
    * words above conditions
may help us to priorize keys to check, especially in a heuristic process.

As it's a quite difficult ressources to get at all and qualified, we
will built it.
"""
import re
from collections import defaultdict

SENTENCE_PATTERN = re.compile(r"^\s*([A-Za-z,;'\"]\s?)+[.?!]", flags=re.MULTILINE)


def index_of_one_of(string, seeked_chrs: str = ""):
    """ Speed efficient str.index() for multiple chr
    
    Args:
        string (str): In what we look at.
        seeked_chrs (str):
            List of char we're looking for.
    Return:
        -1 if not found, else the index of the first char that is in `seeked_chrs`
    """
    # Skip dummy call
    if not seeked_chrs:
        return -1

    for i, char in enumerate(string):
        if char in seeked_chrs:
            return i
    return -1


def sentence_generator(stream):
    """ Memory efficient large text file that yield sentence to sentence
    
    Args:
        stream (io.IOBase): Any stream like a FileStream, StringStream.
    Yield:
        (str) sentences one by one, and None once reach the end of the stream. 
    """
    next_line = stream.readline()
    buffer = ""
    while len(next_line):
        buffer += next_line
        if not len(buffer):
            # End of the file
            return

        index_next_ponctuation = index_of_one_of(buffer, ".?!")
        if -1 != index_next_ponctuation:
            # There is a sentence, we're removing it from the buffer
            sentence_candidate, ponctuation, buffer = buffer.partition(
                buffer[index_next_ponctuation]
            )
            match = SENTENCE_PATTERN.search(sentence_candidate + ponctuation)

            if match:
                yield match.group(0)

        next_line = stream.readline()


def count_words_occurrence(iterable_streams, quiet: bool = True):
    """ Take a list of txt files and count each words relative to his position
    and from the previous words.
    
    Note that we condiderate poncturation as words.
    
    Args:
        iterable_streams (iterable[io.IOBase]): list of stream to text files.
        quiet (bool): if true, enable a progress display (to stdout)
    Returns:
        (dict) a recursive dict as key → tuple(occurrence_count, dict_next_word)
        and as `dict_next_word` having the same structure that the first one.
    """

    # We build a the recursive dict (c.f. 'Returns' section of the docstring)
    def recursive_default():
        return [0, defaultdict(recursive_default)]

    index_occurrence = defaultdict(recursive_default)

    # Loop over files and count (only for quiet = False).
    count_done = 0
    for file in iterable_streams:
        if not quiet:
            print(f"Files processed : {count_done}", end='\r')

        try:
            for sentence in sentence_generator(file):
                if not sentence:
                    break

                words = sentence.strip().lower().split()

                # separate the ponctuation
                ponctuation = words[-1][-1]
                words[-1] = words[-1][:-1]
                words.append(ponctuation)

                current_index = index_occurrence

                for word in words:
                    current_index[word][0] += 1
                    current_index = current_index[word][1]
        except UnicodeDecodeError:
            pass
        
        count_done += 1
    
    if not quiet:
        print()  # Force new line

    return index_occurrence


if __name__ == "__main__":
    import json
    from gutenberg_pooler import generator_book_file_stream
    from os import rename, remove
    from os.path import isfile


    output = count_words_occurrence(generator_book_file_stream(), quiet=False)
    # Build a backup
    try:
        if isfile("./output.sentence_broker.json"):
            if isfile("./output.sentence_broker.bak.json"):
                remove("./output.sentence_broker.bak.json")
            rename("./output.sentence_broker.json", "./output.sentence_broker.bak.json")
    except Exception:
        pass

    with open("./output.sentence_broker.json", "w") as f:
        json.dump(output, f)

