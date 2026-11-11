"""Pure binary search tree logic for the BST mode of the tree visualiser (no UI).

``BST`` stores the tree as parent/left/right dictionaries keyed by value. The
``*_steps`` methods return a list of animation states, each
``[node_colours, message, output]`` — exactly what
``graph_vis.GraphVisualiser.run_animation`` draws — without touching the tree
(``insert`` / ``insert_steps`` are the only methods that change it).

Colour meanings (shared with tree_vis):
  lightblue - not involved in the current step
  orange    - node being compared with the value
  green     - the value was found / the new node was placed
  red       - the search ended at an empty spot (value not present)
  white     - the new node before it has been placed (insert)
"""
import random

BASE_COLOUR = 'lightblue'


class BST:
    def __init__(self, values=()):
        self.root = None
        self.left = {}    # value -> left child value (or None)
        self.right = {}   # value -> right child value (or None)
        self.parent = {}  # value -> parent value (None for the root)
        for value in values:
            self.insert(value)

    # ---- basic structure -------------------------------------------------
    def __len__(self):
        return len(self.parent)

    def __contains__(self, value):
        return value in self.parent

    def values(self):
        """Values in in-order (sorted) order."""
        return self.inorder()

    def edges(self):
        """(parent, child) pairs, for drawing."""
        return [(self.parent[v], v) for v in self.parent if self.parent[v] is not None]

    def insert(self, value):
        """Insert without recording steps. Duplicates are ignored. Returns True if inserted."""
        return self.insert_steps(value) is not None and value in self

    def depth(self, value):
        d = 0
        while self.parent[value] is not None:
            value = self.parent[value]
            d += 1
        return d

    def height(self):
        """Number of levels (0 for an empty tree)."""
        return max((self.depth(v) for v in self.parent), default=-1) + 1

    # ---- traversals ------------------------------------------------------
    def inorder(self, node=None, out=None):
        if out is None:
            out = []
            node = self.root
        if node is None:
            return out
        self.inorder(self.left[node], out)
        out.append(node)
        self.inorder(self.right[node], out)
        return out

    def preorder(self, node=None, out=None):
        if out is None:
            out = []
            node = self.root
        if node is None:
            return out
        out.append(node)
        self.preorder(self.left[node], out)
        self.preorder(self.right[node], out)
        return out

    def postorder(self, node=None, out=None):
        if out is None:
            out = []
            node = self.root
        if node is None:
            return out
        self.postorder(self.left[node], out)
        self.postorder(self.right[node], out)
        out.append(node)
        return out

    # ---- layout ----------------------------------------------------------
    def layout(self):
        """Positions {value: (x, y)} in 0..1: x by in-order rank, y by depth."""
        order = self.inorder()
        if not order:
            return {}
        levels = self.height()
        pos = {}
        for i, value in enumerate(order):
            x = 0.5 if len(order) == 1 else i / (len(order) - 1)
            y = 1.0 if levels == 1 else 1.0 - self.depth(value) / (levels - 1)
            pos[value] = (x, y)
        return pos

    # ---- step generation -------------------------------------------------
    def _colours(self):
        return {v: BASE_COLOUR for v in self.parent}

    def search_steps(self, value):
        """States for searching ``value``: each comparison highlights the node orange."""
        states = []
        path = []
        if self.root is None:
            states.append([self._colours(), f"The tree is empty, so {value} cannot be in it.", "Not found"])
            return states

        node = self.root
        while node is not None:
            path.append(node)
            colours = self._colours()
            colours[node] = 'orange'
            if value == node:
                colours[node] = 'green'
                states.append([colours, f"Compare {value} with {node}: equal, so {value} has been FOUND.",
                               f"Path: {path}\nComparisons: {len(path)}"])
                return states
            if value < node:
                direction, nxt = "left", self.left[node]
            else:
                direction, nxt = "right", self.right[node]
            message = (f"Compare {value} with {node}: {value} {'<' if value < node else '>'} {node}, "
                       f"so go {direction}.")
            if nxt is None:
                message += f"\nThe {direction} child is empty, so {value} is NOT in the tree."
                colours[node] = 'red'
                states.append([colours, message, f"Path: {path}\nComparisons: {len(path)}\nNot found"])
                return states
            states.append([colours, message, f"Path: {path}\nComparisons: {len(path)}"])
            node = nxt
        return states  # pragma: no cover - loop always returns

    def insert_steps(self, value):
        """Insert ``value`` and return the states that show where it goes.

        Returns ``None`` (and changes nothing) if the value is already present.
        """
        if value in self:
            return None

        states = []
        path = []
        if self.root is None:
            self.root = value
            self.parent[value] = None
            self.left[value] = self.right[value] = None
            states.append([{value: 'green'},
                           f"The tree is empty, so {value} becomes the root.", f"Inserted {value} as the root"])
            return states

        node = self.root
        while True:
            path.append(node)
            colours = self._colours()
            colours[node] = 'orange'
            colours[value] = 'white'
            if value < node:
                direction, nxt = "left", self.left[node]
            else:
                direction, nxt = "right", self.right[node]
            message = (f"Compare {value} with {node}: {value} {'<' if value < node else '>'} {node}, "
                       f"so go {direction}.")
            if nxt is None:
                self.parent[value] = node
                self.left[value] = self.right[value] = None
                if direction == "left":
                    self.left[node] = value
                else:
                    self.right[node] = value
                message += f"\nThe {direction} child is empty, so {value} is placed there."
                states.append([colours, message, f"Path: {path}\nComparisons: {len(path)}"])
                final = self._colours()
                final[value] = 'green'
                states.append([final, f"{value} has been inserted as the {direction} child of {node}.",
                               f"Path: {path}\nComparisons: {len(path)}\nIn-order: {self.inorder()}"])
                return states
            states.append([colours, message, f"Path: {path}\nComparisons: {len(path)}"])
            node = nxt

    def traversal_steps(self, kind):
        """States for a pre/in/post-order traversal: visited nodes turn purple/pink/violet."""
        order = {"pre": self.preorder, "in": self.inorder, "post": self.postorder}[kind]()
        colour = {"pre": 'purple', "in": 'pink', "post": 'violet'}[kind]
        name = {"pre": "pre-order", "in": "in-order", "post": "post-order"}[kind]
        states = []
        visited = []
        colours = self._colours()
        for node in order:
            visited.append(node)
            colours = dict(colours)
            colours[node] = colour
            states.append([colours, f"Performing a {name} traversal\nVisiting node: {node}", f"Visited: {visited}"])
        return states


def random_bst(num_nodes=None, low=1, high=99, rng=random):
    """A BST built by inserting ``num_nodes`` distinct random values in random order."""
    if num_nodes is None:
        num_nodes = rng.randint(5, 8)
    return BST(rng.sample(range(low, high + 1), num_nodes))
