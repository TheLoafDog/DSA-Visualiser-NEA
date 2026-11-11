"""Pure Dijkstra's shortest path for the graph visualiser (no UI).

``dijkstra_steps(edges, start, nodes, target=None)`` takes undirected weighted
edges as ``(u, v, weight)`` triples and returns ``(states, distances, previous)``.
Each state is ``[node_colours, message, output]`` — exactly what
``graph_vis.GraphVisualiser.run_animation`` draws. Nothing is modified.

Colour meanings (shared with graph_vis):
  lightblue - not yet reached
  orange    - node being settled (smallest tentative distance in the queue)
  yellow    - neighbour whose distance is being checked / updated
  green     - settled: its shortest distance is final
  purple    - the shortest path to the target, shown at the end
"""
import heapq
import math

BASE_COLOUR = 'lightblue'
INF = math.inf


def _adjacency(edges, nodes):
    adj = {node: {} for node in nodes}
    for u, v, weight in edges:
        adj.setdefault(u, {})[v] = weight
        adj.setdefault(v, {})[u] = weight
    return adj


def format_distances(distances):
    """Compact one-line table: '0: 0   1: 4   2: ∞'."""
    return "   ".join(f"{node}: {'∞' if d == INF else d}" for node, d in sorted(distances.items()))


def shortest_path(previous, start, target):
    """Path from start to target using the ``previous`` map, or [] if unreachable."""
    if target not in previous and target != start:
        return []
    path = [target]
    while path[-1] != start:
        path.append(previous[path[-1]])
    return path[::-1]


def dijkstra_steps(edges, start, nodes=(), target=None):
    adj = _adjacency(edges, nodes)
    if start not in adj:
        adj[start] = {}

    distances = {node: INF for node in adj}
    distances[start] = 0
    previous = {}
    settled = set()
    states = []

    def colours(current=None, neighbour=None):
        c = {node: BASE_COLOUR for node in adj}
        for node in settled:
            c[node] = 'green'
        if current is not None:
            c[current] = 'orange'
        if neighbour is not None:
            c[neighbour] = 'yellow'
        return c

    states.append([colours(), f"Start at node {start}: distance 0. Every other node starts at ∞ (unknown).",
                   format_distances(distances)])

    queue = [(0, start)]
    while queue:
        dist, node = heapq.heappop(queue)
        if node in settled:
            continue  # Stale queue entry (a shorter distance was found later)
        settled.add(node)
        states.append([colours(current=node),
                       f"Node {node} has the smallest tentative distance ({dist}) of the unsettled nodes, "
                       f"so its shortest distance is now final.",
                       format_distances(distances)])

        if node == target:
            path = shortest_path(previous, start, target)
            c = colours()
            for p in path:
                c[p] = 'purple'
            states.append([c, f"Reached node {target}: shortest distance {dist} along path {' -> '.join(map(str, path))}.",
                           format_distances(distances)])
            return states, distances, previous

        for neighbour, weight in sorted(adj[node].items()):
            if neighbour in settled:
                continue
            new_dist = dist + weight
            if new_dist < distances[neighbour]:
                old = '∞' if distances[neighbour] == INF else distances[neighbour]
                distances[neighbour] = new_dist
                previous[neighbour] = node
                heapq.heappush(queue, (new_dist, neighbour))
                message = (f"Check neighbour {neighbour}: {dist} + {weight} = {new_dist} is shorter than {old}, "
                           f"so update its distance to {new_dist} (via {node}).")
            else:
                message = (f"Check neighbour {neighbour}: {dist} + {weight} = {new_dist} is not shorter than "
                           f"{distances[neighbour]}, so keep {distances[neighbour]}.")
            states.append([colours(current=node, neighbour=neighbour), message, format_distances(distances)])

    unreachable = [node for node, d in distances.items() if d == INF]
    message = "All reachable nodes are settled; the shortest distances from node " + str(start) + " are final."
    if unreachable:
        message += f"\nNodes {unreachable} cannot be reached from node {start}."
    if target is not None:
        message += f"\nNode {target} is not reachable from node {start}."
    states.append([colours(), message, format_distances(distances)])
    return states, distances, previous
