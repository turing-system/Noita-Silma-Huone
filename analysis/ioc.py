# -*- coding: utf-8 -*-
""" A file to compute the Index of Coincidence [IoC]
as it will be use quite everywhere.
"""
import numpy as np

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