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

    # Auto-fill `symbols_by_position``
    if symbols_by_position is None:
        symbols_by_position = []
        for _ in range(message_length):
            symbols_by_position = list(symbols)

    # Auto-fill `message_length`
    if message_length is None:
        message_length = len(symbols_by_position)

    # Auto-fill `symbols`
    all_symbols_ununique = sum(symbols_by_position, start=[])
    if symbols is None:
        symbols = np.unique(all_symbols_ununique)

    # Compute denominator
    denominator = message_length * (message_length -1)

    # Define max overall occurences of a single symbol
    max_global = 0
    for n in range(message_length):
        nominator = n*(n-1)
        if nominator/denominator < target_ioc + delta:
            max_global = n
        else:
            break

    # Build symbols -> possible position (perf purpose)
    symbol_to_positions = defaultdict(deque)
    for position, symbol in enumerate(symbols_by_position):
        symbol_to_positions[symbol].append(position)

    def _resurcive_stage_solution_generator(
        current_max: int,
        current_nominator: float,
        current_slot_consume: int,
        current_solution: list,
        target_range_ioc: tuple,
        symbol_to_positions: dict[list],
        symbols_by_position: list[list],
        stage_deepness=0,
    ) -> list[int]:
        """ Avoid to generate the whole combinatory solution, but
        will only generate solutions that are possibles from the beginning
        to the end, by considerating it stage by stage, recursivly.

        This function is call for each "stage"
        A "stage" is a number that define how much a given symbol will repeat.

        Exemple, 5 mean we have a symbol which is selected to be repeated 5
        times.

        For a given stage, all possibles symbols availables for this stage are
        considerated and we compute all solutions for each of them.

        This heuristic process allow us to not event try to compute all 
        possibilities, and drop a minimal of invalid solutions on the way.

        Args:
            * current_max (int):
                We can't add a symbol `current_max` times at this stage.
            * current_solution (list):
                The list of symbols selected by previous stages
            * current_nominator (float):
                Value IoC value for `current_solution`
            * current_slot_consume (int):
                Number of slot used in the `current_solution`.
                Equal to `len(current_solution) - current_solution.count(None)`
            * target_range_ioc (tuple[int, int]):
                Tuple of size 2, that is compose of the `(min, max)` of the
                targer IoC range.
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
        TODO:
            * `stage_sizes` compute can be better, I think we can pre-compute
                in which range we the current stage size can be to be in the
                target IoC range.
                All ideas are welcome.
        """
        # Note that `s1` and `s2` always refer to a symbol value

        # Default solution
        if current_solution is None:
            current_solution = [None] * len(symbols_by_position)

        solution_length = len(symbols_by_position)
        ioc_denominator = solution_length*(solution_length-1)

        # Compute all possibles stages sizes from this point
        stage_sizes = []
        for n in range(current_max, 0, -1):
            # Skip no-fit in the remains slot
            if n > (solution_length-current_slot_consume):
                continue
            
            # Filter if the max possible IoC can't reach the minimal target IoC
            # Note that we don't considerate any symbols slots combination here.
            forecast_slot_consume = current_slot_consume
            forecast_nominator = current_nominator
            for m in range(n, 0, -1):
                # Will pass at least once, due to above condiiton (↑ ~6 lines)
                while m <= (solution_length-forecast_slot_consume):
                    forecast_nominator += m*(m-1)
                    forecast_slot_consume += m
            
            if forecast_nominator/ioc_denominator >= target_range_ioc[0]:
                stage_sizes.append(n)

        # For each stage size at this position, compute all reals combinations
        # possible, that take in accuont the 
        for stage_size in stage_sizes:
            # Define compatible symbols
            stage_symbols = deque()
            for s1, positions in symbol_to_positions.items():
                if len(positions) >= stage_size and s1 not in current_solution:
                    stage_symbols.append(s1)
            # Define next nominator
            forecast_nominator = current_nominator + stage_size*(stage_size-1)

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

                    if stage_deepness == len(symbols_by_position) -1:
                        # Tail behavior
                        yield next_solution
                    else:
                        # Head/body behavior
                        yield from _resurcive_stage_solution_generator(
                            current_max=stage_size,
                            current_nominator=forecast_nominator,
                            current_slot_consume=current_slot_consume+stage_size,
                            current_solution=next_solution,
                            target_range_ioc=target_range_ioc,
                            symbol_to_positions=next_symbol_to_positions,
                            symbols_by_position=symbols_by_position,
                            stage_deepness=stage_deepness +1,
                        )

    # Yield all solutions for this `solution_template`
    yield from _resurcive_stage_solution_generator(
        current_max=max_global,
        symbol_to_positions=symbol_to_positions,
        symbols_by_position=symbols_by_position,
        target_range_ioc=(target_ioc-delta, target_ioc+delta)
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