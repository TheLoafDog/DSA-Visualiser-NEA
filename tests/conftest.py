"""Shared pytest setup.

The app modules live in the repo root and open data files (e.g. the DSA
Types Database) by relative path, so every test runs from the repo root
with the root on sys.path.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)


def _display_available():
    """True if Tk can open a window (a real display or Xvfb)."""
    try:
        import tkinter
        root = tkinter.Tk()
        root.destroy()
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def display():
    """Skip the test if no display is available (run under `xvfb-run` on CI)."""
    if not _display_available():
        pytest.skip("no display available (run under xvfb-run)")
