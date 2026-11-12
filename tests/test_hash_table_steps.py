"""Unit tests for hash_table_steps (pure insert/search with linear probing)."""
import random

import pytest

import hash_table_steps as hts


def check_states(states, size):
    assert states, "no states produced"
    for table, colours, text in states:
        assert len(table) == size
        assert len(colours) == size
        assert isinstance(text, str) and text
        assert all(c in (hts.EMPTY, hts.EXAMINE, hts.COLLISION, hts.FOUND, hts.NOT_FOUND, hts.TOMBSTONE) for c in colours)


def test_hash_index_is_key_mod_size():
    assert hts.hash_index(7, 10) == 7
    assert hts.hash_index(17, 10) == 7
    assert hts.hash_index(0, 10) == 0
    assert hts.hash_index(99, 10) == 9


def test_insert_without_collision_goes_to_home_slot():
    table = [None] * 10
    states = hts.insert_steps(table, 23)
    check_states(states, 10)
    assert table[3] == 23
    assert sum(1 for s in table if s is not None) == 1
    last_table, last_colours, last_text = states[-1]
    assert last_colours[3] == hts.FOUND
    assert "no collision" in last_text
    assert len(states) == 3  # hash, check home, place


def test_insert_with_collision_probes_linearly():
    table = [None] * 10
    hts.insert_steps(table, 3)
    hts.insert_steps(table, 13)
    states = hts.insert_steps(table, 23)
    check_states(states, 10)
    assert table[3:6] == [3, 13, 23]
    # red on the two occupied slots that were passed, green where it landed
    assert states[-1][1][3] == hts.COLLISION
    assert states[-1][1][4] == hts.COLLISION
    assert states[-1][1][5] == hts.FOUND
    assert "2 probes" in states[-1][2]


def test_insert_wraps_round_to_the_start():
    table = [None] * 5
    hts.insert_steps(table, 4)
    hts.insert_steps(table, 9)   # home 4 taken -> wraps to 0
    assert table == [9, None, None, None, 4]


def test_insert_duplicate_changes_nothing():
    table = [None] * 10
    hts.insert_steps(table, 42)
    before = list(table)
    states = hts.insert_steps(table, 42)
    assert table == before
    assert "already in the table" in states[-1][2]


def test_insert_into_full_table_fails_gracefully():
    table = [None] * 4
    for key in (0, 1, 2, 3):
        hts.insert_steps(table, key)
    before = list(table)
    states = hts.insert_steps(table, 8)
    check_states(states, 4)
    assert table == before
    assert "full" in states[-1][2]


def test_search_finds_key_after_probing():
    table = [None] * 10
    for key in (3, 13, 23):
        hts.insert_steps(table, key)
    before = list(table)
    states = hts.search_steps(table, 23)
    check_states(states, 10)
    assert table == before  # search never modifies the table
    assert states[-1][1][5] == hts.FOUND
    assert "Found 23 at index 5" in states[-1][2]


def test_search_stops_at_first_empty_slot():
    table = [None] * 10
    hts.insert_steps(table, 3)
    states = hts.search_steps(table, 13)
    check_states(states, 10)
    # home slot 3 holds 3 (mismatch), slot 4 empty -> not found after 2 slots
    assert states[-1][1][3] == hts.COLLISION
    assert states[-1][1][4] == hts.NOT_FOUND
    assert "not in the table" in states[-1][2]
    assert "2 slots" in states[-1][2]


def test_search_in_full_table_without_key_checks_every_slot():
    table = [None] * 4
    for key in (0, 1, 2, 3):
        hts.insert_steps(table, key)
    states = hts.search_steps(table, 7)
    check_states(states, 4)
    assert all(c == hts.COLLISION for c in states[-1][1])
    assert "Every slot" in states[-1][2]


def test_load_factor():
    table = [None] * 10
    assert hts.load_factor(table) == 0
    hts.insert_steps(table, 1)
    hts.insert_steps(table, 2)
    assert hts.load_factor(table) == pytest.approx(0.2)


@pytest.mark.parametrize("seed", range(20))
def test_random_inserts_then_every_key_is_found(seed):
    rng = random.Random(seed)
    size = rng.randint(3, 12)
    table = [None] * size
    keys = rng.sample(range(100), rng.randint(1, size))
    for key in keys:
        hts.insert_steps(table, key)
    assert sorted(k for k in table if k is not None) == sorted(keys)
    for key in keys:
        states = hts.search_steps(table, key)
        assert states[-1][1][table.index(key)] == hts.FOUND
    # a key that was never inserted is never "found"
    missing = next(k for k in range(100, 200) if k not in keys)
    assert hts.FOUND not in hts.search_steps(table, missing)[-1][1]


# --- delete (tombstones) ------------------------------------------------------

def test_delete_leaves_a_tombstone():
    table = [None] * 10
    hts.insert_steps(table, 3)
    states = hts.delete_steps(table, 3)
    check_states(states, 10)
    assert table[3] is hts.DELETED
    assert states[-1][1][3] == hts.TOMBSTONE
    assert "deleted marker" in states[-1][2]
    assert str(hts.DELETED) == "X"


def test_delete_missing_key_changes_nothing():
    table = [None] * 10
    hts.insert_steps(table, 3)
    before = list(table)
    states = hts.delete_steps(table, 13)  # home slot 3 holds 3, slot 4 empty
    assert table == before
    assert states[-1][1][4] == hts.NOT_FOUND
    assert "Nothing to delete" in states[-1][2]


def test_search_probes_past_a_tombstone():
    table = [None] * 10
    for key in (3, 13, 23):
        hts.insert_steps(table, key)      # slots 3, 4, 5
    hts.delete_steps(table, 13)           # slot 4 becomes a tombstone
    states = hts.search_steps(table, 23)
    check_states(states, 10)
    assert states[-1][1][4] == hts.TOMBSTONE
    assert states[-1][1][5] == hts.FOUND
    assert "Found 23 at index 5" in states[-1][2]
    # and the deleted key itself is no longer found
    assert hts.FOUND not in hts.search_steps(table, 13)[-1][1]


def test_insert_reuses_the_first_tombstone_but_checks_for_duplicates_first():
    table = [None] * 10
    for key in (3, 13, 23):
        hts.insert_steps(table, key)      # slots 3, 4, 5
    hts.delete_steps(table, 13)           # tombstone at 4
    # 23 is still in the table past the tombstone: no duplicate is added
    states = hts.insert_steps(table, 23)
    assert table[4] is hts.DELETED and table[5] == 23
    assert "already in the table" in states[-1][2]
    # a new key that probes past the tombstone is placed into it
    states = hts.insert_steps(table, 33)
    assert table[4] == 33
    assert states[-1][1][4] == hts.FOUND
    assert "deleted slot" in states[-1][2]


def test_insert_into_table_full_of_keys_and_tombstones_reuses_tombstone():
    table = [None] * 3
    for key in (0, 1, 2):
        hts.insert_steps(table, key)
    hts.delete_steps(table, 1)
    states = hts.insert_steps(table, 7)   # home 1 is the tombstone; 2 and 0 are keys
    assert table[1] == 7
    assert "deleted slot" in states[-1][2]


def test_is_key_and_load_factor_with_tombstones():
    table = [None] * 4
    hts.insert_steps(table, 1)
    hts.insert_steps(table, 2)
    hts.delete_steps(table, 1)
    assert [hts.is_key(s) for s in table] == [False, False, True, False]
    assert hts.load_factor(table) == pytest.approx(0.5)  # tombstone still counts


@pytest.mark.parametrize("seed", range(20))
def test_random_insert_delete_mix_matches_a_set(seed):
    rng = random.Random(seed)
    size = rng.randint(4, 12)
    table = [None] * size
    live = set()
    for _ in range(40):
        key = rng.randrange(50)
        if rng.random() < 0.6 and len(live) < size:
            hts.insert_steps(table, key)
            live.add(key)
        else:
            hts.delete_steps(table, key)
            live.discard(key)
        assert sorted(k for k in table if hts.is_key(k)) == sorted(live)
        for k in live:
            assert hts.FOUND in hts.search_steps(table, k)[-1][1]
        absent = rng.randrange(50)
        if absent not in live:
            assert hts.FOUND not in hts.search_steps(table, absent)[-1][1]
