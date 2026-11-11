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
