"""Unit tests for the pure sorting step generators (sorting_steps.py)."""
import random

import pytest

import sorting_steps

ALGORITHMS = [
    sorting_steps.bubble_sort_steps,
    sorting_steps.insertion_sort_steps,
    sorting_steps.merge_sort_steps,
]

random.seed(2024)
DATASETS = (
    [[random.randint(10, 100) for _ in range(20)] for _ in range(10)]
    + [[], [5], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2, 1], [7, 7, 7]]
)


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("data", DATASETS, ids=[f"d{i}" for i in range(len(DATASETS))])
def test_final_state_is_sorted_permutation(algorithm, data):
    states = algorithm(data)
    final_data, final_colours, final_text = states[-1]
    assert final_data == sorted(data)
    assert final_colours == ['green'] * len(data)
    assert final_text.startswith("Data has been sorted with")


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("data", DATASETS, ids=[f"d{i}" for i in range(len(DATASETS))])
def test_states_are_well_formed(algorithm, data):
    states = algorithm(data)
    assert len(states) >= 1
    for snapshot, colours, text in states:
        assert len(snapshot) == len(data)
        assert len(colours) == len(data)
        assert isinstance(text, str) and text


@pytest.mark.parametrize("algorithm", ALGORITHMS[:2], ids=lambda f: f.__name__)
@pytest.mark.parametrize("data", DATASETS, ids=[f"d{i}" for i in range(len(DATASETS))])
def test_swap_based_sorts_keep_every_step_a_permutation(algorithm, data):
    # Bubble and insertion sort only ever swap/shift, so every snapshot holds the
    # same multiset. (Merge sort writes the merged values back over the working
    # array while they are held in temporary halves, so its snapshots don't.)
    for snapshot, _, _ in algorithm(data):
        assert sorted(snapshot) == sorted(data), "a step lost or invented a value"


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
def test_input_is_not_modified(algorithm):
    data = [9, 4, 7, 1]
    algorithm(data)
    assert data == [9, 4, 7, 1]


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
def test_snapshots_are_independent_copies(algorithm):
    states = algorithm([3, 1, 2])
    states[0][0][0] = -999
    assert states[-1][0] == [1, 2, 3]


def test_bubble_sort_step_count():
    # n-1 passes, each comparing n-i-1 pairs, plus the final "sorted" state
    n = 6
    assert len(sorting_steps.bubble_sort_steps(list(range(n, 0, -1)))) == n * (n - 1) // 2 + 1


def test_insertion_sort_on_sorted_input_takes_no_shifts():
    states = sorting_steps.insertion_sort_steps([1, 2, 3, 4])
    assert not any("Shift" in text for _, _, text in states)


def test_step_functions_table_matches_dropdown_names():
    assert list(sorting_steps.STEP_FUNCTIONS) == ["Bubble Sort", "Insertion Sort", "Merge Sort"]
