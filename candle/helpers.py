#This file contains helper functions

from typing import Dict
from collections import OrderedDict


def get_ordered_dict(d: Dict) -> OrderedDict:
    """Returns the dict (OrderedDict) ordered by the Slovak alphabet."""
    alphabet = "a b c d e f g h ch i j k l m n o p q r s t u v w x y z Ostatné" # TODO improve it
    alphabet = alphabet.split(' ')
    order: Dict = {i: alphabet.index(i) for i in alphabet}
    sorted_items = sorted(d.items(), key=lambda t: order.get(get_category(t[0])))
    return OrderedDict(sorted_items)


def get_category(input: str) -> str:
    """E.g. for 'F1' returns 'f', for 'Ch1' returns 'ch', for 'Ostatné' returns 'Ostatné'"""
    if input == "Ostatné":
        return "Ostatné"
    elif string_starts_with_ch(input):
        return "ch"
    else:
        return input[0].lower()


def string_starts_with_ch(prefix: str) -> bool:
    """Returns true if string starts with 'ch'."""
    if prefix.lower()[:2] == "ch":
        return True
    return False