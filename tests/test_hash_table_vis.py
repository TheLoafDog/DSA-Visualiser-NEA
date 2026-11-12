"""GUI tests for the hash table visualiser (skipped without a display)."""
import customtkinter as ctk
import pytest


@pytest.fixture
def vis(display):
    import hash_table_vis

    root = ctk.CTk()
    try:
        frame = hash_table_vis.main(root, root)
        root.update()
        yield frame
    finally:
        root.destroy()


def test_main_builds_an_empty_table(vis):
    import hash_table_vis

    assert vis.table == [None] * hash_table_vis.TABLE_SIZE
    assert vis.canvas.find_all()  # the empty table is drawn straight away


def test_invalid_keys_are_rejected(vis):
    vis.value_entry.insert(0, "abc")
    vis.start_operation("insert")
    assert "whole number" in vis.message_box.message_box.cget("text")
    assert vis.states == {}

    vis.value_entry.delete(0, "end")
    vis.value_entry.insert(0, "250")
    vis.start_operation("insert")
    assert "between 0 and" in vis.message_box.message_box.cget("text")
    assert vis.table.count(None) == len(vis.table)


def test_insert_then_search_animates_states(vis):
    vis.value_entry.insert(0, "17")
    vis.start_operation("insert")
    assert vis.table[7] == 17
    assert len(vis.states) == 3
    assert vis.playback_slider.cget("state") == "normal"
    vis.cancel_animation()

    vis.value_entry.delete(0, "end")
    vis.value_entry.insert(0, "27")
    vis.start_operation("search")
    last = vis.states[len(vis.states) - 1]
    assert "not in the table" in last[2]
    assert vis.table[7] == 17  # search leaves the table alone
    vis.cancel_animation()


def test_generate_and_clear(vis):
    import hash_table_vis

    vis.generate_random_table()
    assert sum(1 for k in vis.table if k is not None) == hash_table_vis.TABLE_SIZE // 2
    vis.clear_table()
    assert vis.table == [None] * hash_table_vis.TABLE_SIZE
    assert vis.playback_slider.cget("state") == "disabled"


def test_delete_button_leaves_a_tombstone_drawn_as_x(vis):
    import hash_table_steps

    vis.value_entry.insert(0, "17")
    vis.start_operation("insert")
    vis.cancel_animation()
    vis.start_operation("delete")
    assert vis.table[7] is hash_table_steps.DELETED
    assert "deleted marker" in vis.states[len(vis.states) - 1][2]
    vis.cancel_animation()
    labels = [vis.canvas.itemcget(i, "text") for i in vis.canvas.find_all() if vis.canvas.type(i) == "text"]
    assert "X" in labels
    assert any("deleted marker" in t for t in labels)
