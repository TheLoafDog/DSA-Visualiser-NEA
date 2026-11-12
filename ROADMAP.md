# Roadmap

Up to 4 items per Claude session, top to bottom. Items tagged [needs Brandon] are skipped by unattended runs.

## Phase 1 — Structure and tooling
- [x] Add a `.gitignore` (Python caches, venvs, OS files) and remove the committed `__pycache__/` folder from git.
- [x] Add `requirements.txt` and expand README "How to run" with the install command and a note that Python needs tkinter.
- [x] Add a `tests/` harness with pytest: a headless smoke test that builds `Main.App` (skips if no display), and a test that `hashDataRetrieve` returns the right entry for every name in `DSAs_array`.
- [x] Add a test that validates the quiz pool: every `answer_position` is one of its `options`, difficulty is 1–3, every topic is a known DSA name; fix any bad questions it finds.
- [x] Move the hash function into one shared module used by both `Main.py` and the database generator script, removing the duplicate (keep behaviour and the generated file identical).
- [ ] [needs Brandon] Rename `making and testing hash with the database for dsa types.py` / `DSA Types Database.txt` to space-free names (may affect references in the NEA write-up).
- [x] Pull the pure step-generation logic for bubble/insertion/merge sort out of `sorting_vis.py` into functions (no UI), with unit tests that the final state is sorted.
- [x] Same for linear/binary search in `searching_vis.py`, with unit tests.
- [x] Add a GitHub Actions workflow that runs `py_compile` and pytest under xvfb.
- [x] Reduce duplication between `sorting_vis.parentFrame` and `searching_vis.parentFrame` (shared bar-chart/playback base class).

## Phase 2 — New implementations
- [x] Add quick sort to the sorting visualiser dropdown (using the step-generation pattern from Phase 1).
- [x] Add selection sort to the sorting visualiser.
- [x] Add quiz questions for under-covered topics: Queue, Searching, Tree (aim ~6 each across difficulties 1–3).
- [x] Add a binary search tree mode (insert/search with comparisons highlighted) to the binary tree visualiser.
- [x] Add Dijkstra's shortest path to the graph visualiser (weighted graphs), with an output of distances.
- [x] Add a hash table visualiser (insert/search with linear probing), plus its revision-database entry and menu wiring.
- [x] Add quiz questions and revision content for the new algorithms above (quick/selection sort, BST, Dijkstra, hash table).

## Phase 3 — More operations, algorithms and polish
- [x] Add a Delete operation to the hash table visualiser (linear probing with tombstones so later probes still find keys), with pure steps in `hash_table_steps.py` and tests.
- [x] Add a Delete operation to the binary search tree mode (leaf, one child, two children via in-order successor) with the comparisons animated, pure logic in `bst_steps.py` and tests.
- [ ] Add heap sort to the sorting visualiser (build max-heap, then repeatedly swap the root to the end; colour the heap region), using the step-generation pattern, with tests.
- [ ] Add Prim's minimum spanning tree to the graph visualiser (weighted graphs; animate the frontier edge chosen each step and show the total weight), with pure steps and tests against networkx.
- [ ] Derive the main-menu filter "Types" and "Categories" checkbox lists from the revision database instead of the hard-coded lists in `Main.py` (removes the duplicate "Binary" entry and picks up Quick/Selection/Hashing), keeping the checkboxes inside the filter frame, with a test.
