# -*- coding: utf-8 -*-
from unittest import TestCase

from utils.binary import (
    generator_bin_words,
)

class BinaryWordsGeneratorTestCase(TestCase):
    """ Test the bits words generator """

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None
        
    def test_generator_1_on_4(self):
        """ Test the output of a simple case """

        self.assertListEqual(
            list(generator_bin_words(words_length=4, bits_up_count=1)),
            [
                1,
                2,
                4,
                8,
            ]
        )
    
    def test_generator_2_on_4(self):
        """ Test the output of a simple case (that use recursive) """

        self.assertListEqual(
            list(generator_bin_words(words_length=4, bits_up_count=2)),
            [
                3,
                5,
                9,
                6,
                10,
                12,
            ]
        )

generator_bin_words