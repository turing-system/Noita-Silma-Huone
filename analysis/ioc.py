# -*- coding: utf-8 -*-
""" A file to compute the Index of Coincidence [IoC]
as it will be use quite everywhere.
"""
import math
from collections import (
    defaultdict,
    deque,
)
from turtle import position

import numpy as np

from utils.binary import generator_bin_words


def ioc(array):
    """ Compute the Index of Coincidence
    
    Args:
        array (iterable[int]): the list of symbol as int to test.
    Return:
        (float) the Index of Coincidence
    """
    if len(array) == 0:
        raise ValueError("Can't compute IoC on an empty array")

    symbols = np.unique(array)
    cryptograph = array

    numerator = 0
    for s in symbols:
        count = cryptograph.count(s)
        numerator += count * (count-1)
    return numerator / len(cryptograph)

def reverse_ioc_generator(target_ioc: float, symbols_by_position:list[list]=None, symbols: list=None, message_length:int=None, delta=0) -> list:
    """ From the IoC target, build a generator that will yield 
    possible message for combining symbols.

    Args:
        target_ioc (float): the target IoC
        symbols_by_position (list[list]):
            List of symbol by position. Allow to only considerate a subset of
            all symbols for one or many positions.
            You should use it instead of `symbols` and `message_length`.
        symbols (list):
            List of plaintext symbols considerated.
            Optionnal if `symbols_by_position` given.
        message_length (int):
            List of symbols considerated.
            Optionnal if `symbols_by_position` given
        delta (float):
            Optionnal, the generator will seek IoC that is `target_ioc` more or
            less this value.
    Return:
        (list) Yield list of values
    """

    assert symbols_by_position is not None or (
        symbols is not None and message_length is not None
    )

    # Build symbols_by_position
    if symbols_by_position is None:
        symbols_by_position = []
        for _ in range(message_length):
            symbols_by_position = list(symbols)

    if message_length is None:
        message_length = len(symbols_by_position)

    # Compute denominator
    denominator = message_length * (message_length -1)

    # Get list of symbols
    all_symbols_ununique = sum(symbols_by_position, start=[])
    if symbols is None:
        symbols = np.unique(all_symbols_ununique)

    # Define max occurences of each
    max_count_all = 0
    for n in range(message_length):
        nominator = n*(n-1)
        if nominator/denominator < target_ioc + delta:
            max_count_all = n

    max_by_symbol = {
        s: min(max_count_all, all_symbols_ununique.count(s))
        for s in symbols
    }

    # Define amount of overlapping
    map_overlapping = {
        s: defaultdict(lambda: 0)
        for s in symbols
    }
    for position_n in symbols_by_position:
        for s1 in position_n:
            for s2 in position_n:
                if s1 != s2:
                    map_overlapping[s1][s2] += 1
    
    sorted_maxs = max_by_symbol.items()
    sorted_maxs.sort(key=lambda x: -x[1])

    # Build symbols -> possible position (perf purpose)
    symbol_to_positions = defaultdict(deque)
    for position, symbol in enumerate(symbols_by_position):
        symbol_to_positions[symbol].append(position)

    def _resurcive_stage_solution_generator(
        current_solution: list,
        solution_template: list,
        symbol_to_positions: dict[list],
        symbols_by_position: list[list],
        stage_deepness=0,
    ) -> list[int]:
        """ Avoid to generate the whole combinatory solution, but
        will only generate solutions that are possibles from the beginning
        to the end, by considerating it stage by stage, recursivly.

        For each unique of
        "number of symbols that repeat the same amount of times"
        Generate symbols candidate

        Args:
            * current_solution (list):
                The list of symbols selected by previous stages
            * solution_template (list[int]):
                List of the amount of occurence (value) per stage (position)
            * symbol_to_positions (dict[int, list(int)]):
                Reverse of `symbols_by_position`.
                An index of the list of available positions (value)
                by symbol (key), for the given current_solution.
            * symbols_by_position (list[list]):
                Reverse of `symbol_to_positions`.
                list of symbol (values) by position (key).
            * stage_deepness (int):
                Which stage we are, from the beginning
        Return:
            (list[int]) Yield solutions as list of symbols
        """
        # Note that `s1` and `s2` always refer to a symbol value

        # Default solution
        if current_solution is None:
            current_solution = [None] * len(solution_template)

        # stage_size (int): We want a symbol who is repeated
        #     `stage_size` times across the solution.
        stage_size = solution_template[stage_deepness]

        # Define compatible symbols
        stage_symbols = deque()
        for s1, positions in symbol_to_positions.items():
            if len(positions) >= stage_size:
                stage_symbols.append(s1)

        for s1 in stage_symbols:
            positions_availables = symbol_to_positions[s1]
            for stage_as_binary in generator_bin_words(
                words_length = len(positions_availables),
                bits_up_count = stage_size,
            ):
                # See the `stage_as_binary` as a number
                # where "0001100" mean the 3rd and 4th
                # "are in".

                # Break ref to reuse in next iteration
                next_solution = list(current_solution)
                next_symbol_to_positions = dict(symbol_to_positions)

                # Apply `stage_as_binary`, as it define new position for
                # the symbol `s1`
                for i in range(len(stage_symbols)):
                    if (1 << i & stage_as_binary) > 0:
                        next_solution[positions_availables[i]] = s1
                        # Update `next_symbol_to_positions`
                        for s2 in symbols_by_position[positions_availables[i]]:
                            next_symbol_to_positions[s2].remove(positions_availables[i])

                if stage_deepness == len(solution_template) -1:
                    # Tail behavior
                    yield next_solution
                else:
                    # Head/body behavior
                    yield from _resurcive_stage_solution_generator(
                        current_solution=next_solution,
                        solution_template=solution_template,
                        symbol_to_positions=next_symbol_to_positions,
                        symbols_by_position=symbols_by_position,
                        stage_deepness=stage_deepness +1,
                    )

    # Generate solutions templates
    # A solution template is just a list of number
    # Each number N represent a symbol repeated N times across the message
    # We iterate over a maximum first symbol occurence, that we lower until
    # no more solution are possible.
    for max_current in range(max_count_all, 0, -1):
        # TODO convert to recursive
        solution_template = [max_current]
        # Count solution message_length (for check < message message_length)
        solution_message_length += max_current
        # Compute nominator (IoC)
        nominator = max_current * (max_current-1)
        # Build a solution form this root
        for n in range(max_current, 0, -1):
            # Optimized, count number of symbol who can
            # be use `n` times
            max_message_length_for_n = 0
            previous_symbols = deque()
            for s1, m in sorted_maxs:
                # We considerate his max - greater symbol overlap
                s1_max = sum(
                    [-map_overlapping[s1][s2] for s2 in previous_symbols],
                    start=m,
                )
                if s1_max < n:
                    max_message_length_for_n +=1
                else:
                    break
                previous_symbols.append(s1)
            
            # Add until reach the limit
            while (
                (nominator + n*(n-1)) / denominator < target_ioc + delta
                and len(solution_template) < max_message_length_for_n
                and solution_message_length + n <= message_length
            ):
                # Increase the nominator
                nominator += n*(n-1)
                solution_template.append(n)
                solution_message_length += n

            if solution_message_length == message_length:
                break
        
        # If not reaching the minimal delta
        # No more solutions are possible
        if nominator / denominator < target_ioc - delta:
            break

        # Yield all solutions for this `solution_template`
        yield from _resurcive_stage_solution_generator(
            solution_template=solution_template,
            symbol_to_positions=symbol_to_positions,
            symbols_by_position=symbols_by_position,
        )


if __name__ == "__main__":
    """ Here a small script that is used to show the evolution of IoC
    in regard of the split of characters across a message.
    """
    import random

    import numpy as np
    from matplotlib import pyplot as plt

    symbols = list(range(83))

    iocs = []
    size_message = 83
    for split in range(1, size_message):
        # Rule is simple:
        # for a split 'n', the text will be compose to 'n' part
        # as close as possible to be equal in length.
        # Each part will only contain 1 defined char, unique across
        # split
        
        size_split_chunk = size_message // split
        size_padding = size_message - (split * size_split_chunk)

        # Generate the message
        iocs.append(ioc(
            sum(
                [[symbols[n]] * size_split_chunk for n in range(split)],
                start=[],
            ) + random.choices(symbols, k=size_padding)
        ))

    width = 0.3
    figure, axis = plt.subplots(1, 1)

    axis.bar(
        range(1, size_message),
        iocs,
    )
    axis.set_xlabel("Split")
    axis.set_ylabel("IoC")

    plt.show()