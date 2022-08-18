# -*- coding: utf-8 -*-
""" For human in middle of a script

When script is more than 10 hour long, it's cool to have something
that ping you.
"""
import time

def beep(morse = ".", frequency = 200, duration = 100) -> None:
    """  Use the system to beep a sound on standard sound output
    
    Args:
        morse (str):
            A string of ' ' (sleep), '.' and '_' for short and long beep.
            (default '.', exemple '.. .._')
        frequency (int):
            Frequency of the beep in Hz.
            (default 200)
        duration (int):
            Duration of the '.' beep in ms 
            (default 100)
    """
    try:
        import winsound
        for symbol in list(morse):
            symbol_duration = duration
            if symbol == "_":
                symbol_duration *= 2
            
            if symbol == " ":
                time.sleep(duration/1000)
            else:
                winsound.Beep(frequency, symbol_duration)
    except Exception:
        pass  # May don't work outside of Windows