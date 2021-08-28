'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

def string_starts_with_ch(prefix: str) -> bool:
    """Return  true if string starts with 'ch'."""
    if prefix.lower()[:2] == "ch":
        return True
    return False
