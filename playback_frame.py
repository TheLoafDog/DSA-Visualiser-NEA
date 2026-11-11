"""Shared bar-chart + playback base class for the sorting and searching visualisers.

``PlaybackFrame`` owns everything the two visualisers had in common:
the title, the bar-chart canvas, the playback slider and its five buttons
(◀◀ ◀| ▷ |▶ ▶▶), the animation state (``states``, ``animation_index``,
``animation_active``, the scheduled ``after`` ids) and the methods that
step through, pause, restart and skip the animation.

Subclasses provide:
  - ``build_header_widgets()`` (optional): widgets packed between the title
    and the canvas (the sorting visualiser puts its algorithm dropdown here).
  - ``unpack_state(state) -> (data, colour_array, text)``: how one entry of
    ``self.states`` maps onto what is drawn. Sorting states carry their own
    data snapshot; searching states only carry colours and use ``self.data``.
  - ``show_index_labels`` (class attribute): whether to write the index under
    each bar.
"""
import customtkinter as ctk


class PlaybackFrame(ctk.CTkFrame):
    show_index_labels = False
    slider_border_colour = None  # Sorting visualiser uses "black"

    def __init__(self, master, speed_var, message_box):
        # Passes the master and speed_var arguments for inheritance and to adjust speed of animations
        super().__init__(master, width=800, height=600)
        self.speed_var = speed_var  # Store reference to the speed variable
        self.message_box = message_box # Each visualiser affects its own message box

        self.propagate(False)

        self.title = ctk.CTkLabel(master=self, font=("Arial", 26, "bold"))
        self.title.pack(pady=10)

        self.build_header_widgets()

        self.canvas = ctk.CTkCanvas(master=self, width=600, height=350)
        self.canvas.pack(padx=20, pady=20)

        slider_kwargs = {}
        if self.slider_border_colour:
            slider_kwargs["border_color"] = self.slider_border_colour
        self.playback_slider = ctk.CTkSlider(master=self, height=20, command=self.on_slider_move, **slider_kwargs)
        self.playback_slider.pack(padx=20, pady=5, fill="x", expand=True)
        self.playback_slider.configure(state="disabled")

        self.edit_playback_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.edit_playback_frame.pack(pady=5)
        self.edit_buttons = []

        self.beginning_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.beginning_button.pack(side="left", padx=3)
        self.beginning_button.configure(text="◀◀", command=lambda: self.change_slider_value("beginning"))
        self.edit_buttons.append(self.beginning_button)

        self.decrement_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.decrement_button.pack(side="left", padx=3)
        self.decrement_button.configure(text="◀|", command=lambda: self.change_slider_value("decrement"))
        self.edit_buttons.append(self.decrement_button)

        self.stop_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=50)
        self.stop_button.pack(side="left", padx=3)
        self.stop_button.configure(text="▷", command=self.toggle_pause)
        self.edit_buttons.append(self.stop_button)

        self.increment_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.increment_button.pack(side="left", padx=3)
        self.increment_button.configure(text="|▶", command=lambda: self.change_slider_value("increment"))
        self.edit_buttons.append(self.increment_button)

        self.complete_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.complete_button.pack(side="left", padx=3)
        self.complete_button.configure(text="▶▶", command=lambda: self.change_slider_value("end"))
        self.edit_buttons.append(self.complete_button)

        # Keep track of whether the animation is ACTIVE or PAUSED
        self.animation_active = False
        self.after_id = None  # Store after_id to cancel scheduled events
        self.after_increment = None

        # Animation variables
        self.data = [] # Data to be visualised
        self.states = {} # Holds the key of each step (starting at 0)
        self.state_index = 0
        self.animation_index = 0
        self.last_value = None # This is so that the slider value only changes when it moves

    # --- hooks for subclasses -------------------------------------------------

    def build_header_widgets(self):
        """Pack any widgets that belong between the title and the canvas."""
        pass

    def unpack_state(self, state):
        """Return (data, colour_array, text) for one entry of self.states."""
        raise NotImplementedError

    # --- drawing -------------------------------------------------------------

    def draw_bars(self, data, colour_array):
        self.canvas.delete("all")
        c_height = 330
        c_width = 580
        bar_width = c_width / (len(data) + 1)
        offset = 30
        spacing = 10

        normalized_data = [i / max(data) for i in data]  # Normalize data

        for i, height in enumerate(normalized_data):
            # Calculate coordinates for the bar
            x0 = i * bar_width + offset + spacing
            y0 = c_height - height * 300
            x1 = (i + 1) * bar_width + offset
            y1 = c_height

            # Draw the bar
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colour_array[i])

            # Add the value label on top of the bar
            self.canvas.create_text(
                (x0 + x1) // 2,  # X-coordinate: center of the bar
                y0 - 10,         # Y-coordinate: slightly above the bar
                text=str(data[i]),  # Display the actual value
                fill="black",
                font=("Arial", 10)
            )

            if self.show_index_labels:
                # Add the index label below the bar
                self.canvas.create_text(
                    (x0 + x1) // 2,  # X-coordinate: center of the bar
                    y1 + 10,         # Y-coordinate: slightly below the bar
                    text=str(i),
                    fill="black",
                    font=("Arial", 10)
                )
        self.update_idletasks()

    def show_state(self, index):
        """Draw the given step and show its message."""
        data, colour_array, text = self.unpack_state(self.states[index])
        self.message_box.change_message(text)
        self.draw_bars(data, colour_array)

    # --- state loading -------------------------------------------------------

    def load_states(self, states): # Stores generated steps into self.states
        for state in states:
            self.states[self.state_index] = state
            self.state_index += 1

    def reset_animation(self):
        """Stop any running animation and clear the recorded steps, ready for a new run."""
        self.cancel_animation()  # Stop any ongoing animations before starting a new one
        self.stop_button.configure(command=self.toggle_pause)
        self.states = {}
        self.state_index = 0
        self.animation_index = 0
        self.animation_active = False
        self.playback_slider.set(0)

    def begin_animation(self):
        """Enable the playback controls and start playing from the first step."""
        self.animation_active = True
        self.set_slider_attributes()
        self.run_animation()

    # --- playback ------------------------------------------------------------

    def toggle_pause(self):
        if not self.animation_active:
            self.animation_active = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.animation_active = False
            self.stop_button.configure(text="▷")

    def cancel_scheduled(self):
        # Cancel any scheduled events by using after_id
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_cancel(self.after_increment)
            self.after_id = None  # Reset after_id since it is no longer active
            self.after_increment = None

    def cancel_animation(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Reset variables and cancel any pending step calls
        self.animation_active = False
        self.cancel_scheduled()

    def run_animation(self):
        if not self.animation_active:
            return

        if self.animation_index < len(self.states):
            self.show_state(self.animation_index)

            self.after_increment = self.after(int(self.speed_var.get()), lambda: self.increment_slider())
            self.after_id = self.after(int(self.speed_var.get()), lambda: self.run_animation())
        else:
            self.stop_button.configure(text="↺", command=lambda: self.restart_visualiser(play=True))

    def restart_visualiser(self, play=True):
        self.stop_button.configure(command=self.toggle_pause) # Reset command for stop button

        # Establish variables for the start of the animation
        self.animation_index = 0

        if play:
            self.begin_animation()
        else:
            self.playback_slider.set(0)
            self.adjust_canvas()

    def change_slider_value(self, mode):
        if mode == "increment" and self.animation_index < len(self.states)-1:
            self.increment_slider()
            self.adjust_canvas()

        if mode == "decrement" and self.animation_index > 0:
            self.decrement_slider()

        if mode == "beginning":
            self.restart_visualiser(play=False)

        if mode == "end":
            self.skip_animation()

    def pause_for_manual_control(self):
        self.animation_active = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)

    def on_slider_move(self, value):
        if value != self.last_value:
            self.cancel_scheduled()
            self.pause_for_manual_control()

            # Next set the visualiser in relation to the slider value
            self.show_state(value)

            self.animation_index = value
            self.last_value = value

    def adjust_canvas(self):
        self.pause_for_manual_control()

        # Next set the visualiser in relation to the slider value
        self.show_state(self.animation_index)

    def increment_slider(self):
        self.playback_slider.set(self.playback_slider.get()+1)
        self.animation_index += 1

        # Cannot add the other stuff included in decrement slider or skip animations since increment_slider() is used elsewhere

    def decrement_slider(self):
        self.playback_slider.set(self.playback_slider.get()-1)
        self.animation_index = self.playback_slider.get()
        self.adjust_canvas()

    def skip_animation(self):
        self.animation_index = len(self.states)-1
        self.playback_slider.set(self.animation_index)
        self.adjust_canvas()

    def set_slider_attributes(self):
        self.playback_slider.set(0)
        actions_number = len(self.states) - 1
        self.playback_slider.configure(from_=0, to=actions_number, number_of_steps=actions_number)
        # Reactivate slider and other buttons
        self.playback_slider.configure(state="normal")
        self.stop_button.configure(text="| |")
        for button in self.edit_buttons:
            button.configure(state="normal")
