"""GUI tests for the shared playback base class used by the sorting and searching visualisers."""
import pytest

import customtkinter as ctk


class FakeMessageBox:
    def __init__(self):
        self.messages = []

    def change_message(self, text):
        self.messages.append(text)


class FakeControlFrame:
    pass


@pytest.fixture
def root(display):
    root = ctk.CTk()
    yield root
    root.destroy()


def make_sorting_frame(root):
    import sorting_vis
    frame = sorting_vis.bubbleFrame(master=root, speed_var=ctk.DoubleVar(value=100),
                                    message_box=FakeMessageBox(), vis_num=1,
                                    control_frame=FakeControlFrame())
    frame.run_animation = lambda: None  # don't schedule Tk callbacks
    frame.start_sorting_simulation(data=[5, 3, 4, 1, 2])
    return frame


def make_searching_frame(root):
    import searching_vis
    frame = searching_vis.linearFrame(master=root, speed_var=ctk.DoubleVar(value=100),
                                      message_box=FakeMessageBox())
    frame.run_animation = lambda: None
    frame.data = [10, 20, 30, 40]
    frame.start_searching_simulation("30")
    return frame


FRAMES = [make_sorting_frame, make_searching_frame]


@pytest.mark.parametrize("make", FRAMES, ids=["sorting", "searching"])
def test_start_enables_playback_controls(root, make):
    frame = make(root)
    assert frame.animation_active
    assert len(frame.states) > 1
    assert frame.playback_slider.cget("state") == "normal"
    assert frame.playback_slider.cget("to") == len(frame.states) - 1
    assert all(b.cget("state") == "normal" for b in frame.edit_buttons)


@pytest.mark.parametrize("make", FRAMES, ids=["sorting", "searching"])
def test_step_buttons_move_through_states(root, make):
    frame = make(root)
    last = len(frame.states) - 1

    frame.change_slider_value("increment")
    assert frame.animation_index == 1 and not frame.animation_active
    frame.change_slider_value("decrement")
    assert frame.animation_index == 0
    frame.change_slider_value("decrement")  # can't go below the first step
    assert frame.animation_index == 0
    frame.change_slider_value("end")
    assert frame.animation_index == last
    frame.change_slider_value("increment")  # can't go past the last step
    assert frame.animation_index == last
    frame.change_slider_value("beginning")
    assert frame.animation_index == 0 and frame.playback_slider.get() == 0


@pytest.mark.parametrize("make", FRAMES, ids=["sorting", "searching"])
def test_slider_move_shows_that_step_message(root, make):
    frame = make(root)
    frame.on_slider_move(2)
    assert frame.animation_index == 2
    assert frame.message_box.messages[-1] == frame.unpack_state(frame.states[2])[2]
    assert frame.stop_button.cget("text") == "▷"


@pytest.mark.parametrize("make", FRAMES, ids=["sorting", "searching"])
def test_toggle_pause(root, make):
    frame = make(root)
    frame.toggle_pause()
    assert not frame.animation_active and frame.stop_button.cget("text") == "▷"
    frame.toggle_pause()
    assert frame.animation_active and frame.stop_button.cget("text") == "| |"


def test_restart_clears_previous_states(root):
    frame = make_sorting_frame(root)
    first_run = len(frame.states)
    frame.start_sorting_simulation(data=[2, 1])
    assert len(frame.states) < first_run
    assert frame.playback_slider.cget("to") == len(frame.states) - 1
