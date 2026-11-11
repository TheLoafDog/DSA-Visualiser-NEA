"""Unit tests for the pure binary search tree logic (bst_steps.py)."""
import random

import pytest

import bst_steps
from bst_steps import BST

random.seed(99)
VALUE_SETS = [random.sample(range(1, 100), random.randint(1, 12)) for _ in range(15)] + [
    [50, 30, 70, 20, 40, 60, 80],
    [1, 2, 3, 4, 5],       # degenerate (all right children)
    [5, 4, 3, 2, 1],       # degenerate (all left children)
]


def check_bst_property(tree, node=None, low=float("-inf"), high=float("inf")):
    if node is None:
        node = tree.root
        if node is None:
            return
    assert low < node < high
    if tree.left[node] is not None:
        assert tree.parent[tree.left[node]] == node
        check_bst_property(tree, tree.left[node], low, node)
    if tree.right[node] is not None:
        assert tree.parent[tree.right[node]] == node
        check_bst_property(tree, tree.right[node], node, high)


@pytest.mark.parametrize("values", VALUE_SETS, ids=[f"v{i}" for i in range(len(VALUE_SETS))])
def test_insert_keeps_bst_property_and_inorder_is_sorted(values):
    tree = BST(values)
    check_bst_property(tree)
    assert tree.inorder() == sorted(values)
    assert len(tree) == len(values)
    assert sorted(tree.preorder()) == sorted(values)
    assert sorted(tree.postorder()) == sorted(values)
    assert tree.root == values[0]


def test_known_shape():
    tree = BST([50, 30, 70, 20, 40, 60, 80])
    assert tree.left[50] == 30 and tree.right[50] == 70
    assert tree.left[30] == 20 and tree.right[30] == 40
    assert tree.preorder() == [50, 30, 20, 40, 70, 60, 80]
    assert tree.postorder() == [20, 40, 30, 60, 80, 70, 50]
    assert tree.height() == 3
    assert set(tree.edges()) == {(50, 30), (50, 70), (30, 20), (30, 40), (70, 60), (70, 80)}


def test_duplicate_insert_is_ignored():
    tree = BST([5, 3])
    assert tree.insert_steps(3) is None
    assert tree.insert(3) is False
    assert len(tree) == 2


@pytest.mark.parametrize("values", VALUE_SETS, ids=[f"v{i}" for i in range(len(VALUE_SETS))])
def test_search_steps_find_present_values_and_reject_absent_ones(values):
    tree = BST(values)
    for value in values:
        states = tree.search_steps(value)
        colours, message, output = states[-1]
        assert "FOUND" in message
        assert colours[value] == 'green'
        # Comparisons equal the depth of the node + 1
        assert len(states) == tree.depth(value) + 1
    for value in (0, 100):
        states = tree.search_steps(value)
        colours, message, output = states[-1]
        assert "NOT in the tree" in message and "Not found" in output
        assert 'red' in colours.values()
    # Searching never changes the tree
    assert tree.inorder() == sorted(values)


def test_search_empty_tree():
    states = BST().search_steps(7)
    assert len(states) == 1 and "empty" in states[0][1]


def test_insert_steps_show_comparison_path():
    tree = BST([50, 30, 70])
    states = tree.insert_steps(40)
    # Compare with 50 (go left), compare with 30 (go right, empty -> placed), final placed state
    assert len(states) == 3
    assert states[0][0][50] == 'orange' and states[0][0][40] == 'white'
    assert "go left" in states[0][1]
    assert states[1][0][30] == 'orange' and "placed there" in states[1][1]
    assert states[2][0][40] == 'green' and "right child of 30" in states[2][1]
    assert tree.right[30] == 40
    # Every state colours exactly the nodes that exist after the insert
    for colours, _, _ in states:
        assert set(colours) == {50, 30, 70, 40}


def test_insert_into_empty_tree_makes_root():
    tree = BST()
    states = tree.insert_steps(9)
    assert tree.root == 9 and len(states) == 1 and states[0][0] == {9: 'green'}


@pytest.mark.parametrize("kind, method", [("pre", "preorder"), ("in", "inorder"), ("post", "postorder")])
def test_traversal_steps_follow_the_traversal_order(kind, method):
    tree = BST([50, 30, 70, 20, 40, 60, 80])
    states = tree.traversal_steps(kind)
    order = getattr(tree, method)()
    assert [int(s[1].split("Visiting node: ")[1]) for s in states] == order
    assert states[-1][2] == f"Visited: {order}"
    # Visited nodes stay coloured, the rest are the base colour
    for i, (colours, _, _) in enumerate(states):
        coloured = {n for n, c in colours.items() if c != bst_steps.BASE_COLOUR}
        assert coloured == set(order[:i + 1])


@pytest.mark.parametrize("values", VALUE_SETS, ids=[f"v{i}" for i in range(len(VALUE_SETS))])
def test_layout_orders_x_by_value_and_y_by_depth(values):
    tree = BST(values)
    pos = tree.layout()
    assert set(pos) == set(values)
    ordered = sorted(values)
    xs = [pos[v][0] for v in ordered]
    assert xs == sorted(xs)
    for v in values:
        assert 0 <= pos[v][0] <= 1 and 0 <= pos[v][1] <= 1
        if tree.parent[v] is not None:
            assert pos[v][1] < pos[tree.parent[v]][1]
    assert pos[tree.root][1] == 1.0
    assert BST().layout() == {}


def test_random_bst_uses_distinct_values_in_range():
    rng = random.Random(1)
    for _ in range(20):
        tree = bst_steps.random_bst(rng=rng)
        assert 5 <= len(tree) <= 8
        assert all(1 <= v <= 99 for v in tree.inorder())
        assert len(set(tree.inorder())) == len(tree)
    assert len(bst_steps.random_bst(3, rng=rng)) == 3
