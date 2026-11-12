"""Pure step generation for the hash table visualiser (no UI).

A hash table is a fixed-size list of slots; ``None`` marks an empty slot
and ``DELETED`` (a tombstone) marks a slot whose key was removed.
Keys are non-negative integers and the hash function is ``key % size``.
Collisions are resolved by *linear probing*: move to the next slot
(wrapping round to index 0) until a free slot / the key is found.

A search treats a tombstone as occupied (it keeps probing past it, since
the key it is looking for may have been placed beyond the deleted slot),
while an insert may reuse the first tombstone it passes.

Each function returns a list of animation states. A state is
``[table, colours, text]`` where ``table`` is a snapshot of the slots,
``colours`` is one colour name per slot and ``text`` is the message to show.

Colours:
  - grey:   untouched slot
  - orange: slot currently being examined
  - red:    occupied slot that caused a collision (insert) / mismatch (search)
  - green:  slot where the key was placed or found
  - purple: slot where the search ended empty (key not in table)
  - black:  tombstone (deleted slot) being probed past
"""


class _Tombstone:
    """Marker for a deleted slot. ``str()`` gives the label drawn in the slot."""
    __slots__ = ()

    def __repr__(self):
        return "DELETED"

    def __str__(self):
        return "X"


DELETED = _Tombstone()

EMPTY = 'grey'
EXAMINE = 'orange'
COLLISION = 'red'
FOUND = 'green'
NOT_FOUND = 'purple'
TOMBSTONE = 'black'


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
    first_tombstone = None
    for probe in range(size):
        colours[index] = EXAMINE
        if probe == 0:
            states.append(_state(table, colours, f"Check the home slot, index {index}."))
        else:
            states.append(_state(table, colours, f"Probe {probe}: check index {index}."))

        if table[index] is None:
            target = index if first_tombstone is None else first_tombstone
            table[target] = key
            colours[target] = FOUND
            if target != index:
                text = f"Index {index} is empty, so {key} is not already stored. Place it in the deleted slot passed earlier, index {target}."
            elif probe == 0:
                text = f"Index {index} is empty. Place {key} there (no collision)."
            else:
                text = f"Index {index} is empty. Place {key} there after {probe} probe{'s' if probe != 1 else ''}."
            states.append(_state(table, colours, text))
            return states

        if table[index] is DELETED:
            if first_tombstone is None:
                first_tombstone = index
            colours[index] = TOMBSTONE
            states.append(_state(table, colours, f"Index {index} holds a deleted marker. Remember it, but keep probing in case {key} is further along."))
            index = (index + 1) % size
            continue

        if table[index] == key:
            colours[index] = FOUND
            states.append(_state(table, colours, f"{key} is already in the table at index {index}. Nothing to insert."))
            return states

        colours[index] = COLLISION
        states.append(_state(table, colours, f"Collision: index {index} already holds {table[index]}. Move to the next slot."))
        index = (index + 1) % size

    if first_tombstone is not None:
        table[first_tombstone] = key
        colours[first_tombstone] = FOUND
        states.append(_state(table, colours, f"Every slot has been checked and {key} is not stored. Place it in the deleted slot at index {first_tombstone}."))
        return states

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

        if table[index] is DELETED:
            colours[index] = TOMBSTONE
            states.append(_state(table, colours, f"Index {index} holds a deleted marker, so {key} may still be further along. Move to the next slot."))
            index = (index + 1) % size
            continue

        colours[index] = COLLISION
        states.append(_state(table, colours, f"Index {index} holds {table[index]}, not {key}. Move to the next slot."))
        index = (index + 1) % size

    states.append(_state(table, colours, f"Every slot has been checked: {key} is not in the table."))
    return states


def delete_steps(table, key):
    """Delete ``key`` from ``table`` (modified in place), leaving a tombstone.

    The slot cannot simply be emptied: a later search for a key that was
    placed past this slot by probing would stop early at the gap. The
    tombstone keeps searches probing and can be reused by a later insert.
    """
    size = len(table)
    colours = [EMPTY] * size
    states = [_state(table, colours, f"Delete {key}: hash({key}) = {key} mod {size} = {hash_index(key, size)}")]

    index = hash_index(key, size)
    for probe in range(size):
        colours[index] = EXAMINE
        if probe == 0:
            states.append(_state(table, colours, f"Check the home slot, index {index}."))
        else:
            states.append(_state(table, colours, f"Probe {probe}: check index {index}."))

        if table[index] is None:
            colours[index] = NOT_FOUND
            states.append(_state(table, colours, f"Index {index} is empty, so {key} is not in the table. Nothing to delete."))
            return states

        if table[index] == key:
            table[index] = DELETED
            colours[index] = TOMBSTONE
            states.append(_state(table, colours, f"Found {key} at index {index}. Replace it with a deleted marker (X) so later searches keep probing past this slot."))
            return states

        if table[index] is DELETED:
            colours[index] = TOMBSTONE
            states.append(_state(table, colours, f"Index {index} holds a deleted marker, so {key} may still be further along. Move to the next slot."))
        else:
            colours[index] = COLLISION
            states.append(_state(table, colours, f"Index {index} holds {table[index]}, not {key}. Move to the next slot."))
        index = (index + 1) % size

    states.append(_state(table, colours, f"Every slot has been checked: {key} is not in the table. Nothing to delete."))
    return states


def is_key(slot):
    """True if ``slot`` holds a key (not empty, not a tombstone)."""
    return slot is not None and slot is not DELETED


def load_factor(table):
    """Fraction of slots in use (0.0 – 1.0). Tombstones count as in use,
    since they still cost probes until the table is rehashed."""
    return sum(1 for slot in table if slot is not None) / len(table)
