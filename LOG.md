# Log

## 2026-11-10 — bootstrap
- Explored the repo: Python/CustomTkinter app, entry `Main.py`, 8 visualiser modules, `Quiz.py`, hashed text database.
- Confirmed the app compiles and launches headlessly (xvfb + python3.12 with tkinter). No tests, CI, .gitignore or requirements.txt yet.
- Added CLAUDE.md (how to run/check + session rules), ROADMAP.md (Phase 1 tooling, Phase 2 new DSAs/quizzes) and this log.

## 2026-11-11 — .gitignore
- Added a Python .gitignore and untracked the committed `__pycache__/` folder (19 .pyc files).
- No code changes. Merged by Claude (interactive session with Brandon).

## 2026-11-11 — requirements.txt + README
- Added requirements.txt (customtkinter, networkx, matplotlib, pillow) and a README "How to run" with install steps and the tkinter note.
- Docs only. Merged by Claude (interactive session with Brandon).

## 2026-11-11 — pytest harness
- Added `tests/` with a conftest (repo-root cwd + `display` fixture that skips without a display), a headless smoke test for `Main.App`, and tests that `hashDataRetrieve` returns the right entry for every name in `DSAs_array`.
- CLAUDE.md checks now run pytest under xvfb (and note `apt-get install python3-tk` for the sandbox). Merged by Claude (autonomous run).

## 2026-11-11 — quiz pool test
- Added `tests/test_quiz_pool.py`: every answer is one of its options, options distinct, difficulty 1–3, topics are known DSA names, question texts unique.
- All 61 questions already pass, so no questions needed fixing. Noted: the pool has no "Searching" questions (Phase 2 item covers this). Merged by Claude (autonomous run).

## 2026-11-11 — shared hash module
- New `dsa_hash.py` (`hash_index`, `place_index`, `retrieve`); `Main.hashDataRetrieve` and both functions in the generator script now delegate to it, removing the duplicated hash code.
- Verified the regenerated database is byte-identical to the committed one (modulo CRLF line endings; the committed .txt was not touched). Added `tests/test_dsa_hash.py`. Merged by Claude (autonomous run).

## 2026-11-11 — sorting step functions
- New `sorting_steps.py` with pure `bubble_sort_steps`, `insertion_sort_steps`, `merge_sort_steps` (input → list of `[data, colours, text]` states, no UI). The three `sorting_vis` frames now call them via a small `parentFrame.load_states` helper; the state sequences are identical to before (checked old vs new frames on 35 datasets under xvfb).
- Added `tests/test_sorting_steps.py` (final state sorted, states well-formed, input untouched, step counts). Merged by Claude (autonomous run).

## 2026-11-11 — searching step functions
- New `searching_steps.py` with pure `linear_search_steps` and `binary_search_steps` (data + target → list of `[colours, text]` states, no UI). `searching_vis` frames now return these from `search_step`; `parentFrame.start_searching_simulation` loads them and starts the animation. State sequences identical to before (checked old vs new frames on 216 data/target cases under xvfb).
- Small fix: a non-integer search value now shows the "Please enter an integer" message and stops, instead of continuing (which raised a TypeError in the binary search). Added `tests/test_searching_steps.py`. Merged by Claude (autonomous run).

## 2026-11-11 — CI workflow
- Added `.github/workflows/checks.yml`: on pushes to main and on PRs, an ubuntu-24.04 runner installs python3-tk + xvfb, the requirements and pytest, then runs `py_compile *.py` and `pytest` under xvfb-run (the same checks as CLAUDE.md).
- Merged by Claude (autonomous run). The first real run happens on the merge commit; see the Actions tab if it fails.

## 2026-11-11 — shared playback base class
- New `playback_frame.py` with `PlaybackFrame`: the title, bar-chart canvas, playback slider + ◀◀ ◀| ▷ |▶ ▶▶ buttons and all the step/pause/restart/skip logic that `sorting_vis.parentFrame` and `searching_vis.parentFrame` each had a copy of. Both now inherit from it (sorting adds its dropdown via `build_header_widgets` and index labels; each defines `unpack_state` for its state shape). ~300 duplicated lines removed.
- Verified the drawn bars and widget states are identical for a scripted playback session before/after. Two small fixes: the sorting slider now shows the message of the step it points at (it showed the previous step's), and starting a new sort clears the previous run's states. Added `tests/test_playback_frame.py` (GUI, skipped without a display). Merged by Claude (autonomous run).

## 2026-11-11 — quick sort
- New `sorting_steps.quick_sort_steps` (Lomuto partition, last element as pivot; purple pivot, orange element being compared, cyan "<= pivot" region, green for placed pivots) and a `quickFrame` in `sorting_vis`. The dropdown now lists Bubble/Insertion/Merge/Quick Sort, driven by a `FRAME_CLASSES` table instead of an if/elif chain.
- Existing tests now cover quick sort too, plus tests that green bars are always in their final position and the worst-case comparison count. Merged by Claude (autonomous run).

## 2026-11-11 — selection sort
- New `sorting_steps.selection_sort_steps` (purple = smallest so far, orange = element being compared, green = sorted prefix) and a `selectionFrame` in `sorting_vis`; the dropdown now also lists Selection Sort.
- Tests: selection sort joins the shared parametrised tests, plus checks that the green prefix is always final/growing and that there are exactly n(n-1)/2 comparisons. Merged by Claude (autonomous run).

## 2026-11-11 — quiz questions for Queue, Searching, Tree
- Added 24 questions to `Quiz.question_pool`: 7 Queue-only, 8 Searching (the pool previously had none, so the Searching checkbox now yields questions) and 9 Tree-only, spread over difficulties 1–3. Pool is now 85 questions; `tests/test_quiz_pool.py` passes on all of them.
- Updated the line-number header comments in `Quiz.py`. Merged by Claude (autonomous run).

## 2026-11-11 — binary search tree mode
- New third tab "Binary Search Tree" in the tree visualiser (`tree_vis.BinarySearchTreeVisualiser`): values 1–99 (max 12), Insert and Search animate each comparison (orange = node being compared, green = found/placed, red = empty spot so not found, white = new node before placement), with the path and comparison count in OUTPUT; pre/in/post-order traversals use true left/right children; Generate Random BST and Clear.
- The tree logic is pure in `bst_steps.py` (`BST` with `insert_steps`, `search_steps`, `traversal_steps`, `layout` — x by in-order rank, y by depth). Tests: `tests/test_bst_steps.py` (BST property, search/insert states, traversals, layout) and `tests/test_tree_vis.py` (GUI, skipped without a display). Existing Basic/Binary Tree tabs untouched. Merged by Claude (autonomous run).

## 2026-11-11 — Dijkstra's shortest path
- New `dijkstra_steps.py` (pure: edges + start [+ target] → animation states, distances, previous map; `shortest_path`, `format_distances`). Graph visualiser gets a "Dijkstra" button (enabled with the Weighted Graph checkbox) using Start Node and optional Find: orange = node being settled, yellow = neighbour being relaxed, green = settled, purple = final path to the target; OUTPUT shows the distance table (∞ for unreachable).
- Tests: `tests/test_dijkstra_steps.py` (textbook graph, path/early-stop, 25 random graphs checked against networkx) and `tests/test_graph_vis.py` (GUI, skipped without a display). Merged by Claude (autonomous run).

## 2026-11-12 — hash table visualiser
- New `hash_table_steps.py` (pure: `insert_steps` / `search_steps` with `key mod size` hashing and linear probing, `load_factor`) and `hash_table_vis.py` (`HashTableFrame` on `PlaybackFrame`: 10 slots drawn as boxes, Insert/Search/Generate Random/Clear, orange = slot examined, red = collision/mismatch, green = placed/found, purple = empty slot ending a failed search, load factor shown).
- "Hash Table" added to `DSAs_array`/`DSAs_dict` and a "Hashing" filter category in `Main.py`; a Hash Table revision entry added to the generator script and the database regenerated (the generator now writes CRLF explicitly so the output is identical on every platform; only the new line changed).
- Tests: `tests/test_hash_table_steps.py` and `tests/test_hash_table_vis.py` (GUI, skipped without a display). Quiz questions for it come with the next item. Merged by Claude (autonomous run).

## 2026-11-12 — quiz questions and revision content for the new algorithms
- 39 questions added to `Quiz.question_pool` (12 quick/selection sort, 7 BST, 8 Dijkstra, 12 hash table; difficulties 1–3). "Hash Table" is now a quiz topic checkbox (`QuizPage.DSAs`) and in the test's known topics. Pool is now 124 questions.
- Revision content: Sorting gains Selection Sort and Quick Sort Partitioning entries (types now list Quick and Selection), Tree gains BST Insert and Search, Graph gains Dijkstra's Algorithm; database regenerated (only those three lines changed).
- Updated the line-number header comments in `Quiz.py`. Merged by Claude (autonomous run).

## 2026-11-12 — roadmap extended (Phase 3)
- All unattended Phase 1–2 items are done, so five new items were added: hash table delete (tombstones), BST delete, heap sort, Prim's MST, and deriving the menu filter lists from the database. Merged by Claude (autonomous run).

## 2026-11-12 — hash table delete (tombstones)
- `hash_table_steps.delete_steps` replaces the found key with a `DELETED` tombstone (drawn as a black "X"); search and delete now probe past tombstones, and insert remembers the first tombstone it passes, keeps probing to rule out a duplicate, then places the key in that tombstone. `is_key` helper added; the load factor counts tombstones and the visualiser says how many there are.
- Delete button added to `HashTableFrame`. Tests: 7 new step tests (including a random insert/delete mix checked against a set) and a GUI test. Merged by Claude (autonomous run).
