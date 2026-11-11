"""GUI tests for the graph visualiser's Dijkstra button (skipped without a display)."""
import customtkinter as ctk
import pytest


@pytest.fixture
def graph(display):
    import graph_vis

    root = ctk.CTk()
    try:
        vis = graph_vis.GraphVisualiser(root)
        vis.pack()
        vis.reset_animation_variables()
        vis.setVis()
        vis.clear_graph()
        root.update()
        yield vis
    finally:
        root.destroy()


def build_square(vis):
    # 0 - 1 - 2 - 3 with a shortcut 0 - 3
    for node in (0, 1, 2, 3):
        vis.add_node(str(node))
    for a, b in ((0, 1), (1, 2), (2, 3), (0, 3)):
        vis.add_edge(str(a), str(b))
    vis.is_weighted.set(True)
    vis.toggle_weights()
    for a, b in ((0, 1), (1, 2), (2, 3)):
        vis.graph[a][b]['weight'] = 1
    vis.graph[0][3]['weight'] = 10


def test_dijkstra_needs_weights_and_valid_nodes(graph):
    vis = graph
    vis.add_node("0")
    assert vis.dijkstra_button.cget("state") == "disabled"
    vis.visualize_dijkstra("0", "")
    assert "Weighted Graph" in vis.message_label.cget("text")
    vis.is_weighted.set(True)
    vis.toggle_weights()
    assert vis.dijkstra_button.cget("state") == "normal"
    vis.visualize_dijkstra("x", "")
    assert "valid node" in vis.message_label.cget("text")
    vis.visualize_dijkstra("5", "")
    assert "not in the graph" in vis.message_label.cget("text")


def test_dijkstra_animation_states_and_distances(graph):
    vis = graph
    build_square(vis)
    vis.visualize_dijkstra("0", "")
    last = vis.states[len(vis.states) - 1]
    assert last[2] == "0: 0   1: 1   2: 2   3: 3"
    assert all(c == 'green' for c in last[0].values())
    vis.cancel_animation()

    vis.visualize_dijkstra("0", "3")
    last = vis.states[len(vis.states) - 1]
    assert "0 -> 1 -> 2 -> 3" in last[1]
    vis.cancel_animation()
