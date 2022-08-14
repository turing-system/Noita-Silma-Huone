# -*- coding: utf-8 -*-
from unittest import TestCase

from cipher.alberti import Alberti


class AlbertiTestCase(TestCase):
    """ Test that the Alberti implementation encode/decode properly """

    def setUp(self) -> None:
        super().setUp()
        self.cipher = Alberti("GHIJKLMNOPQRSTUVWXYZ0123456789ABCDEF", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_symetry(self):
        plain = "ALSKDJLOWIJHLDSA143KFNPOEIHSLDFJNDS354LFKJPQWIFJSDLGJBN354SKFJELOIFJSLFKSDLJGNLSDKF"
        shifts_def = [
            (0,4),
        ]
        for i in range(1, 20):
            shifts_def.append((i*4, 7,))

        self.assertEqual(
            plain,
            self.cipher.decode(
                cipher=self.cipher.encode(
                    plain=plain,
                    shift_definitions=shifts_def,
                ),
                shift_definitions=shifts_def,
            )
        )