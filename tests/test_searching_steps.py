"""Unit tests for the pure searching step generators (searching_steps.py)."""
import random

import pytest

import searching_steps

random.seed(2024)
DATASETS = (
    [[random.randint(10, 100) for _ in range(20)] for _ in range(10)]
    + [[5], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2, 1], [7, 7, 7]]
)
TARGETS = [3, 55, 200]  # plus one present value per dataset (see cases())


def cases():
    for data in DATASETS:
        for target in TARGETS + [data[0], data[-1]]:
            yield data, target


CASES = list(cases())
IDS = [f"c{i}" for i in range(len(CASES))]


def assert_well_formed(states, data):
    assert states, "at least one state"
    for colours, text in states:
        assert len(colours) == len(data)
        assert set(colours) <= {'grey', 'orange', 'red', 'green'}
        assert isinstance(text, str) and text


# --- linear search ---------------------------------------------------------

@pytest.mark.parametrize("data,target", CASES, ids=IDS)
def test_linear_final_state_marks_every_match(data, target):
    states = searching_steps.linear_search_steps(data, target)
    assert_well_formed(states, data)
    final_colours, final_text = states[-1]
    expected = [i for i, v in enumerate(data) if v == target]
    assert [i for i, c in enumerate(final_colours) if c == 'green'] == expected
    if expected:
        assert final_text == "Matches found at indexes: " + str(expected)[1:-1] + "."
    else:
        assert final_text == f"{target} does not exist."


@pytest.mark.parametrize("data,target", CASES, ids=IDS)
def test_linear_one_state_per_element_plus_summary(data, target):
    states = searching_steps.linear_search_steps(data, target)
    assert len(states) == len(data) + 1
    for i, (colours, text) in enumerate(states[:-1]):
        assert colours[i] in ('orange', 'green')
        assert all(c == 'grey' for c in colours[i + 1:])
        assert text.startswith("MATCH found!") == (data[i] == target)


# --- binary search ---------------------------------------------------------

@pytest.mark.parametrize("data,target", CASES, ids=IDS)
def test_binary_finds_target_iff_present(data, target):
    data = sorted(data)
    states = searching_steps.binary_search_steps(data, target)
    assert_well_formed(states, data)
    final_colours, final_text = states[-1]
    if target in data:
        greens = [i for i, c in enumerate(final_colours) if c == 'green']
        assert len(greens) == 1 and data[greens[0]] == target
        assert final_text.endswith(f"Value found at index: {greens[0]}.")
    else:
        assert final_colours == ['grey'] * len(data)
        assert final_text == f"{target} does not exist."


@pytest.mark.parametrize("data,target", CASES, ids=IDS)
def test_binary_takes_logarithmic_steps(data, target):
    data = sorted(data)
    states = searching_steps.binary_search_steps(data, target)
    compare_states = [s for s in states if s[1].startswith("Compare the middle")]
    assert 1 <= len(compare_states) <= len(data).bit_length() + 1


@pytest.mark.parametrize("algorithm", [searching_steps.linear_search_steps,
                                       searching_steps.binary_search_steps],
                         ids=lambda f: f.__name__)
def test_input_not_modified(algorithm):
    data = [10, 20, 30, 40, 50]
    original = list(data)
    algorithm(data, 30)
    assert data == original


def test_binary_empty_data():
    assert searching_steps.binary_search_steps([], 1) == [[[], "1 does not exist."]]


def test_linear_empty_data():
    assert searching_steps.linear_search_steps([], 1) == [[[], "1 does not exist."]]
