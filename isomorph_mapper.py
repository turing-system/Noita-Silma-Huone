# -*- coding: utf-8 -*-
""" In our analysis, we need to map isomorphs.

Isomorphs are a pair or more of one or more elements
that respect a positionnal pattern over ciphers messages.

We will considerate two type of isomorph:
-   horizontal, who are patterns across the same message;
-   vertical, who are patterns across two or more messages;

When we can, we simplify isomorph to keep minimum of them.
Exemple: a..aa.......b.bb is a single isomorph of 3 elements,
we don't considerate included isomorphs of 2 elements.

But we're accepting that isomorph may overlap
"""
from statics.message import (
    E1,
    W1,
    E2,
    W2,
    E3,
    W3,
    E4,
    W4,
    E5,
)

def find_isomorphs(messages=[E1,W1,E2,W2,E3,W3,E4,W4,E5,]):
    """ Find isomorphs in messages
    
    Args:
        messages (list[list(int)]): message to seek in, Noita's eye message by default.
    Returns:
        (list[list[tuple]]) The representation of each isomorph, both vertical and horizontal.
    """
    pass

