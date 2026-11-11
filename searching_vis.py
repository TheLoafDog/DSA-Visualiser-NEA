# Parent frame (inherits the shared bar-chart/playback base class in playback_frame.py):  Lines 16 - 98
# Linear Search Class (inheritance off parent frame):   Lines 100 - 109
# Binary Search Class (inheritance off parent frame):   Lines 111 - 133

# Linear search steps:  searching_steps.linear_search_steps
# Binary search steps:  searching_steps.binary_search_steps

import customtkinter as ctk
import random

from playback_frame import PlaybackFrame
import searching_steps

# Global Variables

class parentFrame(PlaybackFrame):
    def __init__(self, master, speed_var, message_box):
        # The title, canvas, playback slider/buttons and animation variables are built by PlaybackFrame
        super().__init__(master, speed_var, message_box)

        # The two buttons and entry for value to be seached for in each visualiser to play the animation
        self.value_entry = ctk.CTkEntry(master=self)
        self.value_entry.pack(side="left", padx=10, pady=10)
        self.value_entry.bind("<KeyRelease>", self.activate_start_button)  # Bind key release to update recommendations

        self.start_button = ctk.CTkButton(master=self, state="disabled")
        self.start_button.pack(side="left", padx=10, pady=10)

        self.generate_button = ctk.CTkButton(master=self, text="Generate Data")
        self.generate_button.pack(side="right", padx=10, pady=10)
        self.generate_button.configure(command=lambda: self.generate_random_data_set())

        self.clear_button = ctk.CTkButton(master=self, text="Clear Data")
        self.clear_button.pack(side="right", padx=10, pady=10)
        self.clear_button.configure(command=lambda: self.clear_data())

        self.colour_array = []

        self.generate_random_data_set() # On start up, have data already being visualised

    def clear_data(self):
        self.canvas.delete("all")
        self.data = []
        self.start_button.configure(state="disabled")
        for button in self.edit_buttons:
            button.configure(state="disabled")
        self.playback_slider.configure(state="disabled")

        self.animation_active = False

        self.message_box.change_message("Data cleared.")

    def activate_start_button(self, event):
        value = self.value_entry.get().strip()

        try: # If there is no data, then an error arises
            if value and self.data:
                self.start_button.configure(state="normal", command=lambda: self.start_searching_simulation(value))
            else:
                self.start_button.configure(state="disabled")
        except:
            self.message_box.change_message("There is no data to be searched.")

    def unpack_state(self, state): # Searching states are [colours, text]; the data itself never changes
        return self.data, state[0], state[1]

    def draw_graph(self, colour_array):
        self.draw_bars(self.data, colour_array)

    def search_step(self, target_value): # Overridden by each search: returns the list of [colours, text] states from searching_steps
        return []

    def generate_random_data_set(self):
        self.data = [] # Data to be visualised
        for _ in range(20):
            self.data.append(random.randint(10, 100))

        self.colour_array = ['grey'] * len(self.data)

        self.draw_graph(self.colour_array)

        text = "Visualises random data set:\n" + str(self.data)
        self.message_box.change_message(text)

    def start_searching_simulation(self, target_value):
        try:
            target_value = int(target_value)
        except ValueError:
            self.message_box.change_message("Inputted data type is invalid.\nPlease enter an integer.")
            return

        self.reset_animation() # Stop any ongoing animation and clear the previous steps

        self.colour_array = ['grey'] * len(self.data)

        self.load_states(self.search_step(target_value)) # Simulates the search and stores the states

        self.begin_animation()

class linearFrame(parentFrame):
    def __init__(self, master, speed_var, message_box):
        super().__init__(master, speed_var, message_box=message_box)

        # Tailor widgets to the search
        self.title.configure(text="Visualiser 1: Linear Search")
        self.start_button.configure(text="Start Linear Search")

    def search_step(self, target_value): # Override base search_step: linear search states from searching_steps
        return searching_steps.linear_search_steps(self.data, target_value)

class binaryFrame(parentFrame):
    def __init__(self, master, speed_var, message_box):
        super().__init__(master, speed_var, message_box)
        
        # Tailor widgets to the search
        self.title.configure(text="Visualiser 2: Binary Search")
        self.start_button.configure(text="Start Binary Search")

    def generate_random_data_set(self): # Overwrite this method so that it sorts the values
        self.data = [] # Data to be visualised
        for _ in range(20):
            self.data.append(random.randint(10, 100))

        self.colour_array = ['grey'] * len(self.data)

        self.data = sorted(self.data)
        self.draw_graph(self.colour_array)

        text = "Visualises random data set: (sorted)\n" + str(self.data)
        self.message_box.change_message(text)

    def search_step(self, value): # Override base search_step: binary search states from searching_steps
        return searching_steps.binary_search_steps(self.data, value)

class controlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.shared_data = [] # Data to be visualised for both searches

        # Clear canvas
        self.clear_button = ctk.CTkButton(master=self, text="Clear Data")
        self.clear_button.pack(side="left", padx=10, pady=10)

        # Generate shared data set
        self.generate_shared_data_button = ctk.CTkButton(master=self, text="Generate Shared Data")
        self.generate_shared_data_button.pack(side="left", padx=10, pady=10)

        # Shared speed control
        self.speed_var = ctk.DoubleVar(value=100)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self, text="Shared Speed Control (ms)")
        self.speed_label.pack(side="left", padx=10, pady=10)

        self.speed_slider = ctk.CTkSlider(master=self, from_=10, to=1000, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Shared value to be searched for
        self.shared_entry = ctk.CTkEntry(master=self)
        self.shared_entry.pack(side="left", padx=10, pady=10)

        # Compare Both button
        self.compare_both_button = ctk.CTkButton(master=self, text="Search Both", state="disabled")
        self.compare_both_button.pack(side="left", padx=10, pady=10)

    def activate_start_button(self, event, vis1, vis2):
        value = self.shared_entry.get().strip()

        try: # If there is no data, then an error arises
            if value and self.shared_data:
                self.compare_both_button.configure(state="normal", command=lambda: self.start_both(value, vis1, vis2))
            else:
                self.compare_both_button.configure(state="disabled")
        except:
            vis1.message_box.change_message("There is no shared data, which would not be a fair comparison.")
            vis2.message_box.change_message("There is no shared data, which would not be a fair comparison.")
    
    def generate_shared_data(self, vis1, vis2):
        self.shared_data = [] # Data to be visualised for both searches
        for _ in range(20):
            datum = random.randint(10, 100)
            self.shared_data.append(datum)

        vis1.data = self.shared_data
        vis2.data = sorted(self.shared_data)

        colour_array = ['grey'] * len(self.shared_data) # Not a set number - add a feature where the input data can vary in size
        vis1.draw_graph(colour_array)
        vis2.draw_graph(colour_array)

        text1 = f"Visualises shared (random) data set:\n{self.shared_data}"
        text2 = f"Visualises shared (random) data set: (sorted)\n{self.shared_data}"
        vis1.message_box.change_message(text1)
        vis2.message_box.change_message(text2)

    def start_both(self, value, vis1, vis2):
        vis1.start_searching_simulation(value)
        vis2.start_searching_simulation(value)

    def clear_both(self, vis1, vis2):
        text = "Cleared data"
        vis1.message_box.change_message(text)
        vis2.message_box.change_message(text)

        vis1.clear_data()
        vis2.clear_data()

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

class AppTest(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x960")
        self.minsize(1500,960)
        self.title("Searching")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Control frame instance
        self.control_frame = controlFrame(master=self)
        self.control_frame.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

        # Messages for each search
        self.linear_message_box = messageFrame(master=self, title="Linear Search Log")
        self.linear_message_box.grid(row=2, column=0, padx=20, pady=20)

        self.binary_message_box = messageFrame(master=self, title="Binary Search Log")
        self.binary_message_box.grid(row=2, column=1, padx=20, pady=20)

        # Linear and binary search frames with speed_var passed in
        self.linear_frame = linearFrame(master=self, speed_var=self.control_frame.speed_var, message_box=self.linear_message_box)
        self.linear_frame.grid(row=0, column=0, padx=20, pady=20)

        self.binary_frame = binaryFrame(master=self, speed_var=self.control_frame.speed_var, message_box=self.binary_message_box)
        self.binary_frame.grid(row=0, column=1, padx=20, pady=20)
        
        self.control_frame.compare_both_button.configure(command=lambda: self.control_frame.start_both(self.linear_frame, self.binary_frame)) # Not configured in the control frame since the linear and binary search does not exist at that point
        self.control_frame.generate_shared_data_button.configure(command=lambda: self.control_frame.generate_shared_data(self.linear_frame, self.binary_frame))
        self.control_frame.shared_entry.bind(
            "<KeyRelease>", 
            lambda event: self.control_frame.activate_start_button(vis1=self.linear_frame, vis2=self.binary_frame, event=event)
        )

def main(master, window): # add the changes from the test app to the actual app
    window.geometry("1500x1120")
    window.minsize(1500,1120)
    master.configure(fg_color="gray")

    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
    master.grid_columnconfigure(1, weight=1)

    # Control frame instance
    control_frame = controlFrame(master=master)
    control_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    # Messages for each search
    linear_message_box = messageFrame(master=master, title="Linear Search Log")
    linear_message_box.grid(row=2, column=0, padx=20, pady=20)

    binary_message_box = messageFrame(master=master, title="Binary Search Log")
    binary_message_box.grid(row=2, column=1, padx=20, pady=20)

    # Linear and binary search frames with speed_var passed in
    linear_frame = linearFrame(master=master, speed_var=control_frame.speed_var, message_box=linear_message_box)
    linear_frame.grid(row=0, column=0, padx=20, pady=20)

    binary_frame = binaryFrame(master=master, speed_var=control_frame.speed_var, message_box=binary_message_box)
    binary_frame.grid(row=0, column=1, padx=20, pady=20)

    control_frame.compare_both_button.configure(command=lambda: control_frame.start_both(linear_frame, binary_frame))
    control_frame.generate_shared_data_button.configure(command=lambda: control_frame.generate_shared_data(linear_frame, binary_frame))
    control_frame.shared_entry.bind(
        "<KeyRelease>", 
        lambda event: control_frame.activate_start_button(vis1=linear_frame, vis2=binary_frame, event=event)
    )
    control_frame.clear_button.configure(command=lambda: control_frame.clear_both(linear_frame, binary_frame))