"""Unit tests for the pure Dijkstra step generator (dijkstra_steps.py)."""
import random

import networkx as nx
import pytest

import dijkstra_steps
from dijkstra_steps import INF, dijkstra_steps as run

# The classic textbook example
EDGES = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]


def test_known_graph_distances_and_path():
    states, distances, previous = run(EDGES, 0, range(6))
    assert distances == {0: 0, 1: 3, 2: 1, 3: 4, 4: 7, 5: INF}
    assert dijkstra_steps.shortest_path(previous, 0, 4) == [0, 2, 1, 3, 4]
    assert dijkstra_steps.shortest_path(previous, 0, 5) == []
    assert dijkstra_steps.shortest_path(previous, 0, 0) == [0]
    # First state introduces the start, last state reports the unreachable node
    assert states[0][1].startswith("Start at node 0")
    assert "[5] cannot be reached" in states[-1][1]
    assert states[-1][2] == "0: 0   1: 3   2: 1   3: 4   4: 7   5: ∞"


def test_states_are_well_formed_and_settled_nodes_stay_green():
    states, distances, _ = run(EDGES, 0, range(6))
    settled_so_far = set()
    for colours, message, output in states:
        assert set(colours) == set(range(6))
        assert isinstance(message, str) and message
        assert isinstance(output, str) and output
        greens = {n for n, c in colours.items() if c == 'green'}
        assert settled_so_far <= greens | {n for n, c in colours.items() if c == 'orange'}
        settled_so_far |= greens
        assert list(colours.values()).count('orange') <= 1
        assert list(colours.values()).count('yellow') <= 1
    assert settled_so_far == {0, 1, 2, 3, 4}


def test_target_stops_early_and_highlights_path():
    states, distances, previous = run(EDGES, 0, range(6), target=3)
    assert "Reached node 3" in states[-1][1] and "0 -> 2 -> 1 -> 3" in states[-1][1]
    purple = {n for n, c in states[-1][0].items() if c == 'purple'}
    assert purple == {0, 2, 1, 3}
    assert distances[4] == INF  # never got to node 4


def test_unreachable_target():
    states, _, _ = run(EDGES, 0, range(6), target=5)
    assert "Node 5 is not reachable" in states[-1][1]


def test_messages_show_relaxation():
    states, _, _ = run(EDGES, 0, range(6))
    texts = [s[1] for s in states]
    assert any("Check neighbour 1: 0 + 4 = 4 is shorter than ∞" in t for t in texts)
    assert any("Check neighbour 1: 1 + 2 = 3 is shorter than 4" in t for t in texts)
    # Triangle where the long direct edge is checked after a shorter route is known
    states, _, _ = run([(0, 1, 1), (1, 2, 1), (0, 2, 5)], 0, range(3))
    texts = [s[1] for s in states]
    assert any("Check neighbour 2: 1 + 1 = 2 is shorter than 5" in t for t in texts)
    assert not any("is not shorter than" in t for t in texts)
    states, _, _ = run([(0, 1, 1), (1, 2, 5), (0, 2, 2)], 0, range(3))
    texts = [s[1] for s in states]
    assert any("Check neighbour 2: 1 + 5 = 6 is not shorter than 2, so keep 2." in t for t in texts)


@pytest.mark.parametrize("seed", range(25))
def test_matches_networkx_on_random_weighted_graphs(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 10)
    g = nx.gnp_random_graph(n, rng.uniform(0.2, 0.7), seed=seed)
    for u, v in g.edges():
        g[u][v]['weight'] = rng.randint(1, 20)
    start = rng.randrange(n)
    edges = [(u, v, g[u][v]['weight']) for u, v in g.edges()]
    _, distances, previous = run(edges, start, g.nodes())
    expected = nx.single_source_dijkstra_path_length(g, start)
    for node in g.nodes():
        assert distances[node] == expected.get(node, INF)
        if node in expected:
            path = dijkstra_steps.shortest_path(previous, start, node)
            assert path[0] == start and path[-1] == node
            assert sum(g[a][b]['weight'] for a, b in zip(path, path[1:])) == expected[node]


def test_single_node_and_input_untouched():
    edges = [(0, 1, 2)]
    states, distances, _ = run(edges, 0, [0, 1])
    assert edges == [(0, 1, 2)] and distances == {0: 0, 1: 2}
    states, distances, _ = run([], 7, [7])
    assert distances == {7: 0} and len(states) == 3


def test_format_distances():
    assert dijkstra_steps.format_distances({2: INF, 0: 0, 1: 5}) == "0: 0   1: 5   2: ∞"
