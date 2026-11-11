"""Validates every question in the quiz pool (Quiz.question_pool)."""
import pytest

import Quiz

# Topic names the quiz checkboxes use (kept in sync with Main.DSAs_array;
# listed here so this test doesn't need tkinter to import Main).
KNOWN_TOPICS = ['Array', 'Queue', 'Stack', 'Graph', 'Tree', 'Linked List', 'Sorting', 'Searching']

POOL = Quiz.question_pool
IDS = [f"q{i}" for i in range(len(POOL))]


def test_pool_is_not_empty():
    assert len(POOL) > 0


@pytest.mark.parametrize("q", POOL, ids=IDS)
def test_answer_is_one_of_the_options(q):
    assert q.answer_position in q.options, (
        f"{q.question_text!r}: answer {q.answer_position!r} not in {q.options}")


@pytest.mark.parametrize("q", POOL, ids=IDS)
def test_options_are_distinct_and_at_least_two(q):
    assert len(q.options) >= 2, q.question_text
    assert len(set(q.options)) == len(q.options), f"{q.question_text!r}: duplicate options"


@pytest.mark.parametrize("q", POOL, ids=IDS)
def test_difficulty_is_1_to_3(q):
    assert q.difficulty in (1, 2, 3), f"{q.question_text!r}: difficulty {q.difficulty!r}"


@pytest.mark.parametrize("q", POOL, ids=IDS)
def test_topics_are_known_dsa_names(q):
    assert q.topics, f"{q.question_text!r} has no topics"
    unknown = [t for t in q.topics if t not in KNOWN_TOPICS]
    assert not unknown, f"{q.question_text!r}: unknown topics {unknown}"


def test_question_texts_are_unique():
    texts = [q.question_text for q in POOL]
    dupes = {t for t in texts if texts.count(t) > 1}
    assert not dupes, f"duplicate questions: {dupes}"
