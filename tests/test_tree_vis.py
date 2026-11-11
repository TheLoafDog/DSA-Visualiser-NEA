"""GUI tests for the tree visualiser's BST tab (skipped without a display)."""
import customtkinter as ctk
import pytest


@pytest.fixture
def bst_tab(display):
    import tree_vis

    root = ctk.CTk()
    try:
        vis = tree_vis.BinarySearchTreeVisualiser(root)
        vis.pack()
        vis.reset_animation_variables()
        vis.setVis()
        vis.clear_graph()
        root.update()
        yield vis
    finally:
        root.destroy()


def test_tree_page_has_three_tabs(display):
    import tree_vis

    root = ctk.CTk()
    try:
        tree_vis.main(root, root)
        root.update()
        tabview = [w for w in root.winfo_children() if isinstance(w, ctk.CTkTabview)][0]
        assert tabview._name_list == ["Basic Tree", "Binary Tree", "Binary Search Tree"]
    finally:
        root.destroy()


def test_insert_and_search_build_states_and_mirror_the_tree(bst_tab):
    vis = bst_tab
    for value in (50, 30, 70):
        vis.add_node(str(value))
        vis.cancel_animation()
    assert set(vis.graph.nodes()) == {50, 30, 70}
    assert {frozenset(e) for e in vis.graph.edges()} == {frozenset((50, 30)), frozenset((50, 70))}
    assert set(vis.pos) == {50, 30, 70}

    vis.add_node("40")
    # states[0] is the pre-animation snapshot, then compare 50, compare 30, placed
    assert len(vis.states) == 4
    assert vis.states[3][0][40] == 'green'
    assert vis.bst.right[30] == 40
    vis.cancel_animation()

    vis.search_value("60")
    assert "NOT in the tree" in vis.states[len(vis.states) - 1][1]
    vis.cancel_animation()

    # Bad input is reported and does not change the tree
    vis.add_node("abc")
    vis.add_node("150")
    vis.add_node("40")
    assert "already in the tree" in vis.message_label.cget("text")
    assert len(vis.bst) == 4


def test_random_tree_and_traversal(bst_tab):
    vis = bst_tab
    vis.generate_random_tree(6)
    assert len(vis.graph.nodes()) == 6
    vis.tree_traversal(None, "in")
    assert len(vis.states) == 7
    assert vis.states[6][2] == f"Visited: {sorted(vis.graph.nodes())}"
    vis.cancel_animation()
