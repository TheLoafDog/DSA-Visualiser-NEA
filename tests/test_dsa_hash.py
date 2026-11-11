"""Unit tests for the shared hash module (dsa_hash.py)."""
import ast

import pytest

import dsa_hash

NAMES = ['Array', 'Queue', 'Stack', 'Graph', 'Tree', 'Linked List', 'Sorting', 'Searching']


def _database_lines():
    with open("DSA Types Database.txt", "r", encoding="utf-8") as f:
        return f.readlines()


@pytest.mark.parametrize("name", NAMES)
def test_hash_index_is_a_valid_table_slot(name):
    index = dsa_hash.hash_index(name)
    assert isinstance(index, int)
    assert 0 <= index < dsa_hash.TABLE_SIZE


def test_hash_index_is_deterministic():
    assert [dsa_hash.hash_index(n) for n in NAMES] == [dsa_hash.hash_index(n) for n in NAMES]


@pytest.mark.parametrize("name", NAMES)
def test_committed_database_matches_hash_with_linear_probing(name):
    """Each entry sits at, or linearly after, its hash index — so `retrieve`
    (which probes forward from the hash) always finds it."""
    lines = _database_lines()
    positions = [i for i, line in enumerate(lines)
                 if line.strip() and ast.literal_eval(line.rstrip("\r\n"))["name"] == name]
    assert len(positions) == 1, f"{name} appears {len(positions)} times"
    assert positions[0] >= dsa_hash.hash_index(name)
    assert dsa_hash.retrieve(name, lines)["name"] == name


def test_place_index_probes_to_next_empty_slot():
    table = [""] * dsa_hash.TABLE_SIZE
    first = dsa_hash.place_index("Array", table)
    assert first == dsa_hash.hash_index("Array")
    table[first] = "taken"
    assert dsa_hash.place_index("Array", table) == first + 1


def test_retrieve_unknown_key_raises():
    with pytest.raises((IndexError, KeyError, SyntaxError, ValueError)):
        dsa_hash.retrieve("Not A DSA", _database_lines())
