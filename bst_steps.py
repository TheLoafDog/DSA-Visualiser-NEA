"""Pure binary search tree logic for the BST mode of the tree visualiser (no UI).

``BST`` stores the tree as parent/left/right dictionaries keyed by value. The
``*_steps`` methods return a list of animation states, each
``[node_colours, message, output]`` — exactly what
``graph_vis.GraphVisualiser.show_state`` draws — without touching the tree
(``insert`` / ``insert_steps`` and ``delete`` / ``delete_steps`` are the only
methods that change it). Delete states carry a fourth element, a
``snapshot()`` of the structure to draw, because the shape of the tree
changes part-way through the animation.

Colour meanings (shared with tree_vis):
  lightblue - not involved in the current step
  orange    - node being compared with the value
  green     - the value was found / the new node was placed
  red       - the search ended at an empty spot (value not present),
              or the node about to be removed (delete)
  white     - the new node before it has been placed (insert)
  yellow    - the in-order successor that replaces a node with two children
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

    def snapshot(self):
        """The structure to draw: {'nodes', 'edges', 'pos'} (independent copies)."""
        return {"nodes": self.inorder(), "edges": self.edges(), "pos": self.layout()}

    def search_path(self, value):
        """Nodes compared when searching for ``value`` (ending at the value, or where it would go)."""
        path = []
        node = self.root
        while node is not None:
            path.append(node)
            if value == node:
                break
            node = self.left[node] if value < node else self.right[node]
        return path

    def delete(self, value):
        """Delete without recording steps. Returns True if the value was removed."""
        if value not in self:
            return False
        self.delete_steps(value)
        return value not in self

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

    # ---- deletion --------------------------------------------------------
    def _remove_node_with_at_most_one_child(self, value):
        child = self.left[value] if self.left[value] is not None else self.right[value]
        parent = self.parent[value]
        if child is not None:
            self.parent[child] = parent
        if parent is None:
            self.root = child
        elif self.left[parent] == value:
            self.left[parent] = child
        else:
            self.right[parent] = child
        del self.parent[value], self.left[value], self.right[value]

    def _replace_value(self, old, new):
        """Put ``new`` (currently detached) in ``old``'s position, keeping old's children."""
        parent, left, right = self.parent[old], self.left[old], self.right[old]
        del self.parent[old], self.left[old], self.right[old]
        self.parent[new], self.left[new], self.right[new] = parent, left, right
        for child in (left, right):
            if child is not None:
                self.parent[child] = new
        if parent is None:
            self.root = new
        elif self.left[parent] == old:
            self.left[parent] = new
        else:
            self.right[parent] = new

    def _successor_path(self, value):
        """Nodes visited going to the smallest value in ``value``'s right subtree
        (the first is the right child, the last is the successor)."""
        path = [self.right[value]]
        while self.left[path[-1]] is not None:
            path.append(self.left[path[-1]])
        return path

    def delete_steps(self, value):
        """Delete ``value`` and return the states, each with a structure snapshot.

        Cases: a leaf is removed; a node with one child is replaced by that child;
        a node with two children takes the value of its in-order successor (the
        smallest value in its right subtree), whose node is then removed.
        If ``value`` is not in the tree nothing changes and the search states
        (ending red) are returned.
        """
        search = self.search_steps(value)
        before = self.snapshot()
        states = [state + [before] for state in search]
        if value not in self:
            return states
        path = self.search_path(value)
        output = f"Path: {path}\n"

        left, right = self.left[value], self.right[value]
        if left is None and right is None:
            colours = self._colours()
            colours[value] = 'red'
            states.append([colours, f"{value} is a leaf (no children), so it can simply be removed.",
                           output + "Case: leaf", before])
            self._remove_node_with_at_most_one_child(value)
            states.append([self._colours(), f"{value} has been deleted.",
                           output + f"Case: leaf\nIn-order: {self.inorder()}", self.snapshot()])
            return states

        if left is None or right is None:
            child = left if left is not None else right
            side = "left" if left is not None else "right"
            colours = self._colours()
            colours[value] = 'red'
            colours[child] = 'green'
            states.append([colours, f"{value} has one child ({child}, on the {side}), so {child} and its subtree take its place.",
                           output + "Case: one child", before])
            self._remove_node_with_at_most_one_child(value)
            colours = self._colours()
            colours[child] = 'green'
            states.append([colours, f"{value} has been deleted; {child} moved up into its position.",
                           output + f"Case: one child\nIn-order: {self.inorder()}", self.snapshot()])
            return states

        colours = self._colours()
        colours[value] = 'red'
        states.append([colours, f"{value} has two children, so find its in-order successor: the smallest value in its right subtree.",
                       output + "Case: two children", before])
        successor_path = self._successor_path(value)
        for i, node in enumerate(successor_path):
            colours = self._colours()
            colours[value] = 'red'
            colours[node] = 'orange'
            message = f"Go to the right child, {node}." if i == 0 else f"Go left to {node}."
            if self.left[node] is None:
                colours[node] = 'yellow'
                message += f"\n{node} has no left child, so {node} is the successor."
            else:
                message += f"\n{node} has a left child, so keep going left."
            states.append([colours, message, output + f"Case: two children\nSuccessor: {node}", before])
        successor = successor_path[-1]
        self._remove_node_with_at_most_one_child(successor)
        self._replace_value(value, successor)
        colours = self._colours()
        colours[successor] = 'yellow'
        states.append([colours, f"{successor} replaces {value}, and {successor}'s old node is removed (it had at most a right child).",
                       output + f"Case: two children\nSuccessor: {successor}\nIn-order: {self.inorder()}", self.snapshot()])
        return states


def random_bst(num_nodes=None, low=1, high=99, rng=random):
    """A BST built by inserting ``num_nodes`` distinct random values in random order."""
    if num_nodes is None:
        num_nodes = rng.randint(5, 8)
    return BST(rng.sample(range(low, high + 1), num_nodes))
