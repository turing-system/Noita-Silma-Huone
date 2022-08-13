# -*- coding: utf-8 -*-
""" May the message can be cipher using a polyalphabetic cipher
that use 2 cipher alphabet alternativly that allow no double in
the output.
"""
from collections import defaultdict
from constants.message import (
    E1,
)

dict_count = defaultdict(lambda: [0, 0])
for i, trigram in enumerate(E1):
    if i % 2 == 0:
        dict_count[trigram][0] = 1
    else:
        dict_count[trigram][1] = 1

import pprint
pprint.pprint(dict_count)

print(f"Even: {sum([v[0] for v in dict_count.values()])/len(dict_count)}")
print(f"Odd: {sum([v[1] for v in dict_count.values()])/len(dict_count)}")