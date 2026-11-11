# Bubble Sort Class (inheritance off parent frame):     Lines 326 - 347
# Insertion Sort (inheritance off parent frame):        Lines 349 - 369
# Merge Sort in-place (inheritance off parent frame):   Lines 371 - 388

# The step generation (pure, no UI) now lives in sorting_steps.py:
# Bubble Sort steps:    sorting_steps.bubble_sort_steps
# Insertion Sort steps: sorting_steps.insertion_sort_steps
# Merge Sort steps:     sorting_steps.merge_sort_steps

import copy
import customtkinter as ctk
import random

import sorting_steps

# Global Variables

class parentFrame(ctk.CTkFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        # Passes the master and speed_var arguments for inheritance and to adjust speed of animations
        super().__init__(master, width=800, height=600)
        self.speed_var = speed_var  # Store reference to the speed variable
        self.message_box = message_box # Affect their own message boxes
        self.vis_num = vis_num # For the title to show Visualiser 1 or Visualiser 2
        self.control_frame = control_frame # The control frame is passed into each parent frame

        self.propagate(False)

        self.title = ctk.CTkLabel(master=self, font=("Arial", 26, "bold"))
        self.title.pack(pady=10)

        options = ["Bubble Sort", "Insertion Sort", "Merge Sort"]
        self.select_sort_type = ctk.CTkOptionMenu(master=self, values=options, command=self.on_select)
        self.select_sort_type.pack(pady=5)

        self.canvas = ctk.CTkCanvas(master=self, width=600, height=350)
        self.canvas.pack(padx=20, pady=20)

        self.playback_slider = ctk.CTkSlider(master=self, height=20, border_color="black", command=self.on_slider_move)
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
        self.stop_button.configure(text="▷", command=lambda: self.toggle_pause)
        self.edit_buttons.append(self.stop_button)

        self.increment_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.increment_button.pack(side="left", padx=3)
        self.increment_button.configure(text="|▶", command=lambda: self.change_slider_value("increment"))
        self.edit_buttons.append(self.increment_button)

        self.complete_button = ctk.CTkButton(master=self.edit_playback_frame, state="disabled", width=40)
        self.complete_button.pack(side="left", padx=3)
        self.complete_button.configure(text="▶▶", command=lambda: self.change_slider_value("end"))
        self.edit_buttons.append(self.complete_button)

        # The two buttons for each visualiser to play the animation
        self.start_button = ctk.CTkButton(master=self,
        command=lambda: self.start_sorting_simulation()
        )
        self.start_button.pack(side="left", padx=10, pady=10)

        # Keep track of whether the sort is ACTIVE or PAUSED
        self.sort_active = False
        self.after_id = None  # Store after_id to cancel scheduled events
        self.after_increment = None

        # Animation variables
        self.states = {} # Holds the key of each step (starting at 0)
        self.state_index = 0
        self.animation_index = 0
        self.last_value = None # This is so that the slider value only changes when it moves

    def on_select(self, selected_value):
        # Create the new frame first
        if selected_value == "Bubble Sort":
            new_frame = bubbleFrame(master=self.master, speed_var=self.speed_var, message_box=self.message_box, vis_num=self.vis_num, control_frame=self.control_frame)
        elif selected_value == "Insertion Sort":
            new_frame = insertionFrame(master=self.master, speed_var=self.speed_var, message_box=self.message_box, vis_num=self.vis_num, control_frame=self.control_frame)
        else:
            new_frame = mergeFrame(master=self.master, speed_var=self.speed_var, message_box=self.message_box, vis_num=self.vis_num, control_frame=self.control_frame)

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

    def draw_graph(self, data, colour_array):
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
            
            # Add the index label on top of the bar
            self.canvas.create_text(
                (x0 + x1) // 2,  # X-coordinate: center of the bar
                y1 + 10,         # Y-coordinate: slightly below the bar
                text=str(i),  # Display the actual value
                fill="black",
                font=("Arial", 10)
            )
        self.update_idletasks()

    def sort_step(self): # This is used to simulate the steps of the animation and add it to the states array.
        pass

    def load_states(self, states): # Stores generated [data, colours, text] steps into self.states and finishes self.data
        for state in states:
            self.states[self.state_index] = state
            self.state_index += 1
        self.data = list(states[-1][0]) # The final (sorted) data

    def start_sorting_simulation(self, **kwargs):
        self.cancel_sorting()  # Stop any ongoing animations before starting a new one

        self.stop_button.configure(command=self.toggle_pause)
        
        if kwargs:
            self.data = kwargs['data']
        else:
            self.data = [] # Data to be visualised
            for _ in range(20):
                self.data.append(random.randint(10, 100))
        
        # Reset the step variables properly
        self.state_index = 0
        self.animation_index = 0
        self.index = 1 # For insertion sort
        self.step_i = 0
        self.step_j = 0
        self.sort_active = False
        self.playback_slider.set(0)

        self.sort_step() # Recursive function that simulates the sort and stores the states

    def toggle_pause(self):        
        if not self.sort_active:
            self.sort_active = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.sort_active = False
            self.stop_button.configure(text="▷")

    def cancel_sorting(self):
        # Clear the canvas
        self.canvas.delete("all")
        
        # Reset variables and cancel any pending sort_step calls
        self.sort_active = False
        
        # Cancel any scheduled events by using after_id
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_cancel(self.after_increment)
            self.after_id = None  # Reset after_id since it is no longer active
            self.after_increment = None

    def run_animation(self):
        if not self.sort_active:
            return
        
        if self.animation_index < len(self.states):
            data = self.states[self.animation_index][0]
            colour_array = self.states[self.animation_index][1]
            text = self.states[self.animation_index][2]
            self.message_box.change_message(text)

            self.draw_graph(data, colour_array)

            self.after_increment = self.after(int(self.speed_var.get()), lambda: self.increment_slider()) 
            self.after_id = self.after(int(self.speed_var.get()), lambda: self.run_animation())
        else:
            self.stop_button.configure(text="↺", command=lambda: self.restart_visualiser())
            
    def restart_visualiser(self, play=True):
        self.stop_button.configure(command=self.toggle_pause) # Reset command for stop button
        
        # Establish variables for the start of the animation
        self.animation_index = 0

        if play: 
            self.sort_active = True
            
            # Run methods to start the actual animation
            self.set_slider_attributes()
        
            self.run_animation()
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

    def on_slider_move(self, value):
        if value != self.last_value:   
            # Cancel any scheduled events by using after_id
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_cancel(self.after_increment)
                self.after_id = None  # Reset after_id since it is no longer active
                self.after_increment = None
            # Pause the sort
            self.sort_active = False
            self.stop_button.configure(text="▷")
            # In case the animation finished and the command changes, reset command for stop button
            self.stop_button.configure(command=self.toggle_pause)
            
            # Next set the sort visualiser in relation to the slider value
            data = self.states[value][0]
            colour_array = self.states[value][1]
            self.draw_graph(data, colour_array)

            text = self.states[self.animation_index][2]
            self.message_box.change_message(text)
            
            self.animation_index = value
            
            self.last_value = value

    def adjust_canvas(self):
        # Pause the sort
        self.sort_active = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)
            
        # Next set the sort visualiser in relation to the slider value
        data = self.states[self.animation_index][0]
        colour_array = self.states[self.animation_index][1]
        text = self.states[self.animation_index][2]
        self.message_box.change_message(text)
        self.draw_graph(data, colour_array)
        
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
        self.stop_button.configure(state="normal", text="| |")
        for button in self.edit_buttons:
            button.configure(state="normal")

class bubbleFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Bubble Sort")
        self.start_button.configure(text="Start Bubble Sort")
        
        # Step variables for bubble sort
        self.step_i = 0
        self.step_j = 0

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.bubble_sort_steps; see tests/test_sorting_steps.py
        self.load_states(sorting_steps.bubble_sort_steps(self.data))

        # Establish variables for the start of the animation
        self.sort_active = True

        # Run methods to start the actual animation
        self.set_slider_attributes()
        self.run_animation()

class insertionFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)
        
        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Insertion Sort")
        self.start_button.configure(text="Start Insertion Sort")

        # Step variables for insertion sort
        self.index = 1

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.insertion_sort_steps; see tests/test_sorting_steps.py
        self.load_states(sorting_steps.insertion_sort_steps(self.data))

        # Establish variables for the start of the animation
        self.sort_active = True

        # Run methods to start the actual animation
        self.set_slider_attributes()
        self.run_animation()

class mergeFrame(parentFrame):
    def __init__(self, master, speed_var, message_box, vis_num, control_frame):
        super().__init__(master, speed_var, message_box=message_box, vis_num=vis_num, control_frame=control_frame)

        # Tailor widgets to the sort
        self.title.configure(text=f"Visualiser {self.vis_num}: Merge Sort")
        self.start_button.configure(text="Start Merge Sort")

    def sort_step(self):
        # The step logic is pure (no UI) in sorting_steps.merge_sort_steps; see tests/test_sorting_steps.py
        self.load_states(sorting_steps.merge_sort_steps(self.data))

        # Establish variables for the start of the animation
        self.sort_active = True

        # Run methods to start the actual animation
        self.set_slider_attributes()
        self.run_animation()
    
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
