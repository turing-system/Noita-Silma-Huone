# -*- coding: utf-8 -*-
from io import StringIO
from unittest import TestCase

from sentence_broker import count_words_occurrence


class SentenceBrokerTestCase(TestCase):
    """ Test that the sentence broker is not broken (very funny) """

    def setUp(self) -> None:
        super().setUp()
        self.maxDiff = None

    def test_count(self):
        """ Test the output format and that count well """
        output = count_words_occurrence(["./tests/test_sentence_broker.1.txt"])
        self.assertListEqual(
            output,
            [
                ("the", "banana", 0, 2),
                ("banana", "is", 1, 2),
                ("is", "blue", 2, 1),
                ("is", "yellow", 2, 1),
                ("blue", ".", 3, 1),
                ("yellow", ".", 3, 1),
            ],
            "`count_words_occurrence` didn't count well"
        )