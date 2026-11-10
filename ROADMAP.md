# Roadmap

One item per Claude session, top to bottom. Items tagged [needs Brandon] are skipped by unattended runs.

## Phase 1 — Structure and tooling
- [ ] Add a `.gitignore` (Python caches, venvs, OS files) and remove the committed `__pycache__/` folder from git.
- [ ] Add `requirements.txt` and expand README "How to run" with the install command and a note that Python needs tkinter.
- [ ] Add a `tests/` harness with pytest: a headless smoke test that builds `Main.App` (skips if no display), and a test that `hashDataRetrieve` returns the right entry for every name in `DSAs_array`.
- [ ] Add a test that validates the quiz pool: every `answer_position` is one of its `options`, difficulty is 1–3, every topic is a known DSA name; fix any bad questions it finds.
- [ ] Move the hash function into one shared module used by both `Main.py` and the database generator script, removing the duplicate (keep behaviour and the generated file identical).
- [ ] [needs Brandon] Rename `making and testing hash with the database for dsa types.py` / `DSA Types Database.txt` to space-free names (may affect references in the NEA write-up).
- [ ] Pull the pure step-generation logic for bubble/insertion/merge sort out of `sorting_vis.py` into functions (no UI), with unit tests that the final state is sorted.
- [ ] Same for linear/binary search in `searching_vis.py`, with unit tests.
- [ ] Add a GitHub Actions workflow that runs `py_compile` and pytest under xvfb.
- [ ] Reduce duplication between `sorting_vis.parentFrame` and `searching_vis.parentFrame` (shared bar-chart/playback base class).

## Phase 2 — New implementations
- [ ] Add quick sort to the sorting visualiser dropdown (using the step-generation pattern from Phase 1).
- [ ] Add selection sort to the sorting visualiser.
- [ ] Add quiz questions for under-covered topics: Queue, Searching, Tree (aim ~6 each across difficulties 1–3).
- [ ] Add a binary search tree mode (insert/search with comparisons highlighted) to the binary tree visualiser.
- [ ] Add Dijkstra's shortest path to the graph visualiser (weighted graphs), with an output of distances.
- [ ] Add a hash table visualiser (insert/search with linear probing), plus its revision-database entry and menu wiring.
- [ ] Add quiz questions and revision content for the new algorithms above (quick/selection sort, BST, Dijkstra, hash table).
