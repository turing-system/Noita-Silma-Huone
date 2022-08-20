# -*- coding: utf-8 -*-
from unittest import TestCase

from analysis.ioc import (
    ioc,
    reverse_ioc_generator,
)

class ReversedIoCGeneratorTestCase(TestCase):
    """ Test the reverse IoC generator """

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None
        
    def test_generator(self):
        """ Test the output of a simple case """

        sentence_to_seek = "the horse kebab"
        output = next(reverse_ioc_generator(
            target_ioc=ioc(list(sentence_to_seek)),
            delta=0,
            symbols_by_position=[
                ["a", "t", "c", "d", "e"],
                ["a", "h", "c", "d", "e"],
                ["a", "e", "c", "d", "f"],
                ["a", " ", "c", "d", "e"],
                ["a", "h", "c", "d", "e"],
                ["a", "o", "c", "d", "e"],
                ["a", "r", "c", "d", "e"],
                ["a", "s", "c", "d", "e"],
                ["a", "e", "c", "d", "f"],
                ["a", " ", "c", "d", "e"],
                ["a", "k", "c", "d", "e"],
                ["a", "e", "c", "d", "f"],
                ["a", "b", "c", "d", "e"],
                ["b", "a", "c", "d", "e"],
                ["a", "b", "c", "d", "e"],
            ]
        ))

        self.assertListEqual(
            output,
            [
                ["t", "h", "e", " ", "h", "o", "r", "s", "e", " ", "i", "s",
                " ", "d", "o", "i", "n", "g", " ", "k", "e", "b", "a", "b"]
            ]
        )