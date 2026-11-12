"""Pure step generation for the hash table visualiser (no UI).

A hash table is a fixed-size list of slots; ``None`` marks an empty slot.
Keys are non-negative integers and the hash function is ``key % size``.
Collisions are resolved by *linear probing*: move to the next slot
(wrapping round to index 0) until a free slot / the key is found.

Each function returns a list of animation states. A state is
``[table, colours, text]`` where ``table`` is a snapshot of the slots,
``colours`` is one colour name per slot and ``text`` is the message to show.

Colours:
  - grey:   untouched slot
  - orange: slot currently being examined
  - red:    occupied slot that caused a collision (insert) / mismatch (search)
  - green:  slot where the key was placed or found
  - purple: slot where the search ended empty (key not in table)
"""
EMPTY = 'grey'
EXAMINE = 'orange'
COLLISION = 'red'
FOUND = 'green'
NOT_FOUND = 'purple'


def hash_index(key, size):
    """Home slot for ``key`` in a table of ``size`` slots."""
    return key % size


def _state(table, colours, text):
    return [list(table), list(colours), text]


def insert_steps(table, key):
    """Insert ``key`` into ``table`` (modified in place) with linear probing.

    Returns the list of states. If the table is full, or the key is already
    present, no slot is changed and the final message says so.
    """
    size = len(table)
    colours = [EMPTY] * size
    states = [_state(table, colours, f"Insert {key}: hash({key}) = {key} mod {size} = {hash_index(key, size)}")]

    index = hash_index(key, size)
    for probe in range(size):
        colours[index] = EXAMINE
        if probe == 0:
            states.append(_state(table, colours, f"Check the home slot, index {index}."))
        else:
            states.append(_state(table, colours, f"Probe {probe}: check index {index}."))

        if table[index] is None:
            table[index] = key
            colours[index] = FOUND
            if probe == 0:
                text = f"Index {index} is empty. Place {key} there (no collision)."
            else:
                text = f"Index {index} is empty. Place {key} there after {probe} probe{'s' if probe != 1 else ''}."
            states.append(_state(table, colours, text))
            return states

        if table[index] == key:
            colours[index] = FOUND
            states.append(_state(table, colours, f"{key} is already in the table at index {index}. Nothing to insert."))
            return states

        colours[index] = COLLISION
        states.append(_state(table, colours, f"Collision: index {index} already holds {table[index]}. Move to the next slot."))
        index = (index + 1) % size

    states.append(_state(table, colours, f"Every slot has been checked: the table is full, so {key} cannot be inserted."))
    return states


def search_steps(table, key):
    """Search for ``key`` in ``table``; the table is not modified.

    Returns the list of states. The search stops at the first empty slot
    (the key cannot be past it) or after every slot has been probed.
    """
    size = len(table)
    colours = [EMPTY] * size
    states = [_state(table, colours, f"Search {key}: hash({key}) = {key} mod {size} = {hash_index(key, size)}")]

    index = hash_index(key, size)
    for probe in range(size):
        colours[index] = EXAMINE
        if probe == 0:
            states.append(_state(table, colours, f"Check the home slot, index {index}."))
        else:
            states.append(_state(table, colours, f"Probe {probe}: check index {index}."))

        if table[index] is None:
            colours[index] = NOT_FOUND
            states.append(_state(table, colours, f"Index {index} is empty, so {key} is not in the table ({probe + 1} slot{'s' if probe else ''} checked)."))
            return states

        if table[index] == key:
            colours[index] = FOUND
            states.append(_state(table, colours, f"Found {key} at index {index} after {probe + 1} slot{'s' if probe else ''} checked."))
            return states

        colours[index] = COLLISION
        states.append(_state(table, colours, f"Index {index} holds {table[index]}, not {key}. Move to the next slot."))
        index = (index + 1) % size

    states.append(_state(table, colours, f"Every slot has been checked: {key} is not in the table."))
    return states


def load_factor(table):
    """Fraction of slots in use (0.0 – 1.0)."""
    return sum(1 for slot in table if slot is not None) / len(table)
