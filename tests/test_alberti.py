# -*- coding: utf-8 -*-
from unittest import TestCase

from alberti import Alberti


class AlbertiTestCase(TestCase):
    """ Test that the Alberti implementation encode/decode properly """

    def setUp(self) -> None:
        super().setUp()
        self.cipher = Alberti("GHIJKLMNOPQRSTUVWXYZ0123456789ABCDEF", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_symetry(self):
        plain = "ALSKDJLOWIJHLDSA143KFNPOEIHSLDFJNDS354LFKJPQWIFJSDLGJBN354SKFJELOIFJSLFKSDLJGNLSDKF"
        shift_initial=4
        shift_stall=4
        shift_step=7

        self.assertEqual(
            plain,
            self.cipher.decode(
                cipher=self.cipher.encode(
                    plain=plain,
                    shift_initial=shift_initial,
                    shift_stall=shift_stall,
                    shift_step=shift_step,
                ),
                shift_initial=shift_initial,
                shift_stall=shift_stall,
                shift_step=shift_step,
            )
        )