"""Shared hash function for the DSA Types Database.

The database (`DSA Types Database.txt`) is a fixed-size table of 500 lines,
one dict per line, placed by `hash_index(name)` with linear probing. The
same function is used by the generator script
(`making and testing hash with the database for dsa types.py`) to place
entries and by `Main.hashDataRetrieve` to find them again, so the two can
never drift apart.
"""
import ast
import math

TABLE_SIZE = 500


def hash_index(key):
    """Return the starting table index for `key` (the DSA's name)."""
    val = 1
    count = 1
    flip = True

    for letter in key:
        if flip:
            val *= (ord(letter) / 1.5)
        else:
            val += (ord(letter) * 2)
        flip = not flip
        count *= 2

    remainder = val % 3
    val = math.sqrt(val)
    val = round(val / count)

    return round(int(str(val)) * remainder)


def place_index(key, table):
    """Index at which to store `key` in `table` (list of 500 strings, "" = empty),
    probing linearly from `hash_index(key)` until a free slot is found."""
    index = hash_index(key)
    while table[index] != "":
        index += 1
    return index


def retrieve(key, database_lines):
    """Find the entry whose 'name' is `key` in the database lines (as read by
    `readlines()`), probing linearly from `hash_index(key)`.

    `ast.literal_eval()` turns the line's text into a dict; the trailing
    newline is stripped first.
    """
    index = hash_index(key)
    while ast.literal_eval(database_lines[index][:-1])["name"] != key:
        index += 1
    return ast.literal_eval(database_lines[index][:-1])
