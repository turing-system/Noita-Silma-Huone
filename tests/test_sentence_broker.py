# -*- coding: utf-8 -*-
from io import StringIO
from unittest import TestCase

from sentence_broker import count_words_occurrence


class SentenceBrokerTestCase(TestCase):
    """ Test that the sentence broker is not broken (very funny) """

    def setUp(self) -> None:
        super().setUp()

        self.fake_file = StringIO(
            "The banana is yellow.\n"
            "The banana is blue.\n"
        )
        self.maxDiff = None

    def test_count(self):
        """ Test the output format and that count well """
        output = count_words_occurrence([self.fake_file])
        self.assertEqual(
            output["the"][0],
            2,
            "Didn't count well the 'the'"
        )
        self.assertEqual(
            output["the"][1]["banana"][0],
            2,
            "Didn't count well the 'banana'"
        )
        self.assertEqual(
            output["the"][1]["banana"][1]["is"][0],
            2,
            "Didn't count well the 'is'"
        )
        self.assertEqual(
            output["the"][1]["banana"][1]["is"][1]["yellow"][0],
            1,
            "Didn't count well the 'yellow'"
        )
        self.assertEqual(
            output["the"][1]["banana"][1]["is"][1]["yellow"][1]["."][0],
            1,
            "Didn't count well the '.' of yellow"
        )
        self.assertEqual(
            output["the"][1]["banana"][1]["is"][1]["blue"][0],
            1,
            "Didn't count well the 'blue'"
        )
        self.assertEqual(
            output["the"][1]["banana"][1]["is"][1]["blue"][1]["."][0],
            1,
            "Didn't count well the '.' of yellow"
        )