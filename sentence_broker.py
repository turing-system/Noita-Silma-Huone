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
import os
import time
from tqdm import tqdm
from collections import deque

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


def sentence_generator(stream, stop_above: int = 3000) -> str:
    """ Memory efficient large text file that yield sentence to sentence
    
    Args:
        stream (io.IOBase): Any stream like a FileStream, StringStream.
        stop_above (int):
            If the function found a sentence above this number, it's stopping himself.
            Set to 0 or lower to disable this feature. (default: 3000)
    Yield:
        (str) sentences one by one, and None once reach the end of the stream. 
    """
    next_line = stream.readline()
    buffer = ""
    while len(next_line):
        buffer += next_line
        
        if not len(buffer) or (stop_above and len(buffer) > stop_above):
            # Handle 2 cases:
            #   * Don't treat if too long phrases (there is book that only include numbers)
            #   * End of the file
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


def count_words_occurrence(
    list_of_filepath = [],
    max_words: int = 0,
    max_chars: int = 0,
    quiet: bool = True
) -> None:
    """ Take a list of txt files and count each words relative to his position
    and from the previous words.
    
    Note that we condiderate poncturation as words.
    
    Args:
        list_of_filepath (iterable[str]): list of path to text files.
        quiet (bool): if true, enable a progress display (to stdout)
        max_words (int):
            Sentence with more words than this number are ignored.
            Set to 0 or lower to disable this feature. (default: 0)
        max_chars (int):
            Sentence with more chars than this number are ignored.
            Set to 0 or lower to disable this feature. (default: 0)
    """
    if not quiet:
        list_of_filepath = tqdm(list_of_filepath)

    perf_sum_sentence_time = 0.0
    perf_sum_merge_time = 0.0

    output_statistics = []
    for n, filepath in enumerate(list_of_filepath):
        if not quiet:
            list_of_filepath.set_description(
                f"{filepath} (avg: text: "
                f"{perf_sum_sentence_time/n:.4f}; "
                f"merge: {perf_sum_merge_time/n:.4f})"
            )

        perf_sentence_start_time = time.time()
        # Buffer for the whole file
        # Will contain tuple as (previous word, next word, position of the previous word)
        buffer_sentences_statistics = deque()
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                for sentence in sentence_generator(file):
                    if not sentence:
                        break

                    sentence = sentence.strip().lower()
                    if max_chars > 0 and len(sentence) > max_chars:
                        continue

                    words = sentence.split()

                    # separate the ponctuation
                    ponctuation = words[-1][-1]
                    words[-1] = words[-1][:-1]
                    words.append(ponctuation)

                    if max_words > 0 and len(words) > max_words:
                        continue

                    for i in range(len(words) -1):
                        buffer_sentences_statistics.append((words[i], words[i+1], i, 1))
        except UnicodeDecodeError:
            pass
        perf_sentence_end_time = time.time()

        perf_merge_start_time = time.time()
        # Merge both by optimizing the memory usage and speed
        # Done after each file in order to reduce the number of lines
        # and memory consumption
        output_statistics = list(buffer_sentences_statistics) + output_statistics
        output_statistics.sort(key = lambda x: f"{x[2]}{x[0]}||{x[1]}")
        next_output = deque()
        cursor = 0
        for _ in range(len(output_statistics)):
            cursor += 1

            # Merge is done
            if len(output_statistics) <= cursor:
                break

            previous = output_statistics[cursor-1]
            current = output_statistics[cursor]

            # When different, output_statistics[:cursor] are the same type of
            # occurences, and can be sum. 
            if (previous[2] != current[2]
                or previous[1] != current[1]
                or previous[0] != current[0]
            ):
                next_output.append((previous[0], previous[1], previous[2], sum([line[3] for line in output_statistics[:cursor]])))
                output_statistics = output_statistics[cursor:]
                cursor = 0

        # Set all back to `output_statistics` and adding remains equals
        output_statistics = list(next_output) + output_statistics
        perf_merge_end_time = time.time()

        # Performance compute
        perf_sum_sentence_time += perf_sentence_end_time - perf_sentence_start_time
        perf_sum_merge_time += perf_merge_end_time - perf_merge_start_time


    return output_statistics


if __name__ == "__main__":
    import os

    parent_dirpath = './references/gutenberg'
    books_filepaths = [
        os.path.join(parent_dirpath, filename)
        for filename in os.listdir('./references/gutenberg')
    ]

    list_occurences = count_words_occurrence(books_filepaths, quiet=False)
    with open("./references/gutenberg.stats.txt", 'w') as file:
        for occurence_tuple in list_occurences:
            file.write("\t".join([str(o) for o in occurence_tuple])+"\n")


