# Parent frame (inherits the shared bar-chart/playback base class in playback_frame.py):  Lines 23 - 94
# Bubble Sort Class (inheritance off parent frame):     Lines 96 - 106
# Insertion Sort (inheritance off parent frame):        Lines 108 - 118
# Merge Sort in-place (inheritance off parent frame):   Lines 120 - 130
# Quick Sort (inheritance off parent frame):            Lines 132 - 142
# Selection Sort (inheritance off parent frame):        Lines 144 - 154

# The step generation (pure, no UI) now lives in sorting_steps.py:
# Bubble Sort steps:    sorting_steps.bubble_sort_steps
# Insertion Sort steps: sorting_steps.insertion_sort_steps
# Merge Sort steps:     sorting_steps.merge_sort_steps
# Quick Sort steps:     sorting_steps.quick_sort_steps
# Selection Sort steps: sorting_steps.selection_sort_steps

import customtkinter as ctk
import random

from playback_frame import PlaybackFrame
import sorting_steps

# Global Variables

class parentFrame(PlaybackFrame):
    show_index_labels = True
    slider_border_colour = "black"

    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        self.vis_num = vis_num # For the title to show Visualiser 1 or Visualiser 2 (needed by build_header_widgets)
        self.control_frame = control_frame # The control frame is passed into each parent frame
        # The title, canvas, playback slider/buttons and animation variables are built by PlaybackFrame
        super().__init__(master, speed_var, message_box)

        # The start button for each visualiser to play the animation
        self.start_button = ctk.CTkButton(master=self,
        command=lambda: self.start_sorting_simulation()
        )
        self.start_button.pack(side="left", padx=10, pady=10)

    def build_header_widgets(self): # Packed between the title and the canvas
        options = list(sorting_steps.STEP_FUNCTIONS) # "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"
        self.select_sort_type = ctk.CTkOptionMenu(master=self, values=options, command=self.on_select)
        self.select_sort_type.pack(pady=5)

    def on_select(self, selected_value):
        # Create the new frame first (FRAME_CLASSES maps each dropdown name to its frame class)
        frame_class = FRAME_CLASSES[selected_value]
        new_frame = frame_class(master=self.master, speed_var=self.speed_var, message_box=self.message_box, vis_num=self.vis_num, control_frame=self.control_frame)

        new_frame.select_sort_type.set(selected_value) # Show the selected option in the option menu
        self.message_box.title_label.configure(text=f"{selected_value} Log")

        # Update the master's reference to the visualization frame
        if self.vis_num == 1:
            self.master.vis_1 = new_frame
        else:
            self.master.vis_2 = new_frame

        # Configure the compare button
        self.control_frame.compare_both_button.configure(
            command=lambda: self.control_frame.start_both(self.master.vis_1, self.master.vis_2)
        )
        
        # Position the new frame
        new_frame.grid(row=0, column=self.vis_num-1, padx=20, pady=20)
        
        # Now that the new frame is in place, destroy the old one
        self.destroy()

    def unpack_state(self, state): # Sorting states are [data, colours, text]
        return state[0], state[1], state[2]

    def draw_graph(self, data, colour_array):
        self.draw_bars(data, colour_array)

    def sort_step(self): # Overridden by each sort: returns the list of [data, colours, text] states from sorting_steps
        return []

    def load_states(self, states): # Stores generated steps into self.states and finishes self.data
        super().load_states(states)
        self.data = list(states[-1][0]) # The final (sorted) data

    def start_sorting_simulation(self, **kwargs):
        self.reset_animation() # Stop any ongoing animation and clear the previous steps

        if kwargs:
            self.data = kwargs['data']
        else:
            self.data = [] # Data to be visualised
            for _ in range(20):
                self.data.append(random.randint(10, 100))

        self.load_states(self.sort_step()) # Simulates the sort and stores the states

        self.begin_animation()

class bubbleFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Bubble Sort")
        self.start_button.configure(text="Start Bubble Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.bubble_sort_steps; see tests/test_sorting_steps.py
        return sorting_steps.bubble_sort_steps(self.data)

class insertionFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)
        
        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Insertion Sort")
        self.start_button.configure(text="Start Insertion Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.insertion_sort_steps; see tests/test_sorting_steps.py
        return sorting_steps.insertion_sort_steps(self.data)

class mergeFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Merge Sort")
        self.start_button.configure(text="Start Merge Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.merge_sort_steps; see tests/test_sorting_steps.py
        return sorting_steps.merge_sort_steps(self.data)

class quickFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Quick Sort")
        self.start_button.configure(text="Start Quick Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.quick_sort_steps; see tests/test_sorting_steps.py
        return sorting_steps.quick_sort_steps(self.data)

class selectionFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Selection Sort")
        self.start_button.configure(text="Start Selection Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.selection_sort_steps; see tests/test_sorting_steps.py
        return sorting_steps.selection_sort_steps(self.data)

# Dropdown name -> frame class (same names as sorting_steps.STEP_FUNCTIONS)
FRAME_CLASSES = {
    "Bubble Sort": bubbleFrame,
    "Insertion Sort": insertionFrame,
    "Merge Sort": mergeFrame,
    "Quick Sort": quickFrame,
    "Selection Sort": selectionFrame,
}

class controlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Shared speed control
        self.speed_var = ctk.DoubleVar(value=700)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self, text="Speed (ms)")
        self.speed_label.pack(side="left", padx=10, pady=10)

        self.speed_slider = ctk.CTkSlider(master=self, from_=1000, to=10, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Compare Both button
        self.compare_both_button = ctk.CTkButton(master=self, text="Compare Both")
        self.compare_both_button.pack(side="left", padx=10, pady=10)
        
    def start_both(self, vis1, vis2):
        shared_data = [] # Data to be visualised for both sorts
        for _ in range(20):
            datum = random.randint(10, 100)
            shared_data.append(datum)
            
        vis1.start_sorting_simulation(data=copy.deepcopy(shared_data))
        vis2.start_sorting_simulation(data=copy.deepcopy(shared_data)) # Copy is used here since arrays in python are mutable

class messageFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, width=600, height=200)
        self.master = master
        self.title = title

        self.propagate(False) # Completely static, does not change

        self.title_label = ctk.CTkLabel(master=self, font=("Arial", 22, "bold"), text=self.title)
        self.title_label.pack(padx=10, pady=10)

        self.message_box = ctk.CTkLabel(master=self, font=("Arial", 14), text="", wraplength=400)
        self.message_box.pack(expand=True)

    def change_message(self, text):
        self.message_box.configure(text=text)
        
def main(master, window):
    window.geometry("1500x1200")
    window.minsize(1500,1200)
    master.configure(fg_color='gray')

    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
    master.grid_columnconfigure(1, weight=1)

    # Messages for each sort
    vis_1_messagebox = messageFrame(master=master, title="Bubble Sort Log")
    vis_1_messagebox.grid(row=2, column=0, padx=20, pady=20)

    vis_2_messagebox = messageFrame(master=master, title="Insertion Sort Log")
    vis_2_messagebox.grid(row=2, column=1, padx=20, pady=20)

    # Control frame instance
    control_frame = controlFrame(master=master)
    control_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    # Bubble and insertion sort frames with speed_var and message boxes passed in
    master.vis_1 = bubbleFrame(master=master, speed_var=control_frame.speed_var, message_box=vis_1_messagebox, vis_num=1, control_frame=control_frame)
    master.vis_1.grid(row=0, column=0, padx=20, pady=20)

    master.vis_2 = insertionFrame(master=master, speed_var=control_frame.speed_var, message_box=vis_2_messagebox, vis_num=2, control_frame=control_frame)
    master.vis_2.grid(row=0, column=1, padx=20, pady=20)
    master.vis_2.select_sort_type.set("Insertion Sort")

    control_frame.compare_both_button.configure(command=lambda: control_frame.start_both(master.vis_1, master.vis_2))
