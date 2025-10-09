# Linear Search Class (inheritance off parent frame):   Lines 320 - 380
# Binary Search Class (inheritance off parent frame):   Lines 331 - 380

# Linear search steps:  Lines 382 - 453
# Binary search steps:  Lines 410 - 453

import copy
import customtkinter as ctk
import random

# Global Variables

class parentFrame(ctk.CTkFrame):
    def __init__(self, master, speed_var, message_box):
        # Passes the master and speed_var arguments for inheritance and to adjust speed of animations
        super().__init__(master, width=800, height=600)
        self.speed_var = speed_var  # Store reference to the speed variable
        self.message_box = message_box

        self.propagate(False)

        self.title = ctk.CTkLabel(master=self, font=("Arial", 26, "bold"))
        self.title.pack(pady=10)

        self.canvas = ctk.CTkCanvas(master=self, width=600, height=350)
        self.canvas.pack(padx=20, pady=20)

        self.playback_slider = ctk.CTkSlider(master=self, height=20, command=self.on_slider_move)
        self.playback_slider.pack(padx=20, pady=5, fill="x", side="top")
        self.playback_slider.configure(state="disabled")

        self.edit_playback_frame = ctk.CTkFrame(master=self, fg_color="transparent", border_width=0)
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

        # Keep track of whether the search is ACTIVE or PAUSED
        self.search_active = False
        self.after_id = None  # Store after_id to cancel scheduled events
        self.after_increment = None

        # Animation variables
        self.states = {} # Holds the key of each step (starting at 0)
        self.state_index = 0
        self.animation_index = 0
        self.last_value = None # This is so that the slider value only changes when it moves
        self.colour_array = []

        self.generate_random_data_set() # On start up, have data already being visualised

    def clear_data(self):
        self.canvas.delete("all")
        self.data = []
        self.start_button.configure(state="disabled")
        for button in self.edit_buttons:
            button.configure(state="disabled")
        self.playback_slider.configure(state="disabled")

        self.search_active = False

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
        
    def draw_graph(self, colour_array):
        self.canvas.delete("all")
        c_height = 330
        c_width = 580
        bar_width = c_width / (len(self.data) + 1)
        offset = 30
        spacing = 10
    
        normalized_data = [i / max(self.data) for i in self.data]  # Normalize data
        
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
                text=str(self.data[i]),  # Display the actual value
                fill="black",
                font=("Arial", 10)
            )
            
        self.update_idletasks()

    def search_step(self): # This is used to simulate the steps of the animation and add it to the states array.
        pass

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
            
        self.cancel_searching()  # Stop any ongoing animations before starting a new one

        self.stop_button.configure(command=self.toggle_pause)

        # Reset the step variables properly
        self.states = {}
        self.state_index = 0
        self.animation_index = 0
        self.search_active = False
        self.playback_slider.set(0)
        self.cur_index = 0 # For the linear search
        self.matches = [] # For the linear search, this will be a list for all the indexes containing the target value
        self.high = len(self.data) - 1 # For the binary search
        self.found = False # For the binary search iteration
        self.low = 0

        self.colour_array = ['grey'] * len(self.data)

        self.search_step(target_value) # Recursive function that simulates the search and stores the states

    def toggle_pause(self):        
        if not self.search_active:
            self.search_active = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.search_active = False
            self.stop_button.configure(text="▷")

    def cancel_searching(self):
        # Clear the canvas
        self.canvas.delete("all")
        
        # Reset variables and cancel any pending search_step calls
        self.search_active = False
        
        # Cancel any scheduled events by using after_id
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_cancel(self.after_increment)
            self.after_id = None  # Reset after_id since it is no longer active
            self.after_increment = None

    def run_animation(self):
        if not self.search_active:
            return
        
        if self.animation_index < len(self.states):
            # basically fix all these and check the slider values and steps or whatever
            colour_array = self.states[self.animation_index][0] # Will end up making this a 2d list in the form of : [[colour_array], [message (text)]]
            text = self.states[self.animation_index][1]
            self.message_box.change_message(text)
            self.draw_graph(colour_array)

            self.after_increment = self.after(int(self.speed_var.get()), lambda: self.increment_slider()) 
            self.after_id = self.after(int(self.speed_var.get()), lambda: self.run_animation())
        else:
            self.stop_button.configure(text="↺", command=lambda: self.restart_visualiser(play=True))
        
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

            # Pause the search
            self.search_active = False
            self.stop_button.configure(text="▷")
            # In case the animation finished and the command changes, reset command for stop button
            self.stop_button.configure(command=self.toggle_pause)
            
            # Next set the search visualiser in relation to the slider value
            colour_array = self.states[value][0]
            text = self.states[value][1]
            self.message_box.change_message(text)
            self.draw_graph(colour_array)
            
            self.animation_index = value
            
            self.last_value = value

    def adjust_canvas(self):
        # Pause the search
        self.search_active = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)
        
        # Next set the search visualiser in relation to the slider value
        colour_array = self.states[self.animation_index][0]
        text = self.states[self.animation_index][1]
        self.message_box.change_message(text)
        self.draw_graph(colour_array)
        
    def increment_slider(self):
        self.playback_slider.set(self.playback_slider.get()+1)
        self.animation_index += 1

        # Cannot add teh other stuff included in decrement slider or skip animations since increment_slider() is used elsewhere

    def decrement_slider(self):
        self.playback_slider.set(self.playback_slider.get()-1)
        self.animation_index = self.playback_slider.get()
        self.adjust_canvas()

    def skip_animation(self):
        self.animation_index = len(self.states)-1
        self.playback_slider.set(self.animation_index)
        self.adjust_canvas()
        
    def restart_visualiser(self, play):
        self.stop_button.configure(command=self.toggle_pause) # Reset command for stop button
        
        # Establish variables for the start of the animation
        self.animation_index = 0

        if play:
            self.search_active = True
            
            # Run methods to start the actual animation
            self.set_slider_attributes()
        
            self.run_animation()
        else:
            self.playback_slider.set(0)
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

class linearFrame(parentFrame):
    def __init__(self, master, speed_var, message_box):
        super().__init__(master, speed_var, message_box=message_box)

        # Tailor widgets to the search
        self.title.configure(text="Visualiser 1: Linear Search")
        self.start_button.configure(text="Start Linear Search")
        
        # Step variables for linear search
        self.cur_index = 0

    def search_step(self, target_value): # Override base search_step for recursive linear search
        if self.cur_index < len(self.data):
            # Highlight the elements that match green and those that don't in red, those yet to be compared remain grey (default)
            self.colour_array[self.cur_index] = 'orange'

            text = "Comparing data in index " + str(self.cur_index) + " and the target value, " + str(target_value)
            # Instead of drawing the array now, it just stores the variables as a state
            self.states[self.state_index] = [copy.deepcopy(self.colour_array), text]

            if self.data[self.cur_index] == target_value: # Checks whether the current value matches with the searched value
                self.colour_array[self.cur_index] = 'green'
                
                text = "MATCH found!\nData[" + str(self.cur_index) + "] == " + str(target_value)
                # Instead of drawing the array now, it just stores the variables as a state
                self.states[self.state_index] = [copy.deepcopy(self.colour_array), text]
                self.matches.append(self.cur_index) # Add match
            else:
                # Instead of drawing the array now, it just stores the variables as a state
                text = "NO MATCH found!\nData[" + str(self.cur_index) + "] != " + str(target_value)
                self.states[self.state_index] = [copy.deepcopy(self.colour_array), text]
                
                self.colour_array[self.cur_index] = 'red'

            self.cur_index += 1
            self.state_index += 1

            self.search_step(target_value) 
        else: # Simulation ends
            colour_array = [] # Manually add the final state
            for _ in range(0, len(self.data)):
                colour_array.append('grey')
                
            if self.matches:
                text = "Matches found at indexes: " + str(self.matches)[1:-1] + "."
            else: # If it is empty, no matches
                text = str(target_value) + " does not exist."

            for i in self.matches:
                colour_array[i] = 'green'

            # Instead of drawing the array now, it just stores the variables as a state
            self.states[self.state_index] = [copy.deepcopy(colour_array), text]

            # Establish variables for the start of the animation
            self.search_active = True

            # Run methods to start the actual animation
            self.set_slider_attributes()

            self.run_animation()

class binaryFrame(parentFrame):
    def __init__(self, master, speed_var, message_box):
        super().__init__(master, speed_var, message_box)
        
        # Tailor widgets to the search
        self.title.configure(text="Visualiser 2: Binary Search")
        self.start_button.configure(text="Start Binary Search")

        # Step variables for binary search
        self.high = 0 # This would be the final index of the data set
        self.low = 0
        self.mid = 0

        self.found = False # Check when the simulation is completed

    def generate_random_data_set(self): # Overwrite this method so that it sorts the values
        self.data = [] # Data to be visualised
        for _ in range(20):
            self.data.append(random.randint(10, 100))

        self.colour_array = ['grey'] * len(self.data)

        self.data = sorted(self.data)
        self.draw_graph(self.colour_array)

        text = "Visualises random data set: (sorted)\n" + str(self.data)
        self.message_box.change_message(text)

    def search_step(self, value): # Override base search_step for recursive binary search
        while self.high >= self.low and not self.found:
            self.mid = (self.high + self.low) // 2
            self.colour_array[self.mid] = "orange"
            self.states[self.state_index] = [copy.deepcopy(self.colour_array), "Compare the middle value with the value.\nMiddle index: " + str(self.mid) + " = (" + str(self.high) + " + " + str(self.low) + ") // 2"]
            self.state_index += 1

            if value == self.data[self.mid]:
                self.colour_array = ['grey'] * len(self.data)
                self.colour_array[self.mid] = 'green'
                # Colour the final searched array green
                self.states[self.state_index] = [copy.deepcopy(self.colour_array), "Data[" + str(self.mid) + "] == " + str(value) + ".\nValue found at index: " + str(self.mid) + "."]
                self.state_index += 1

                # Reset colour of array
                self.colour_array[self.mid] = 'grey'

                self.found = True
            else:
                # Adjust search boundaries and recurse
                if self.data[self.mid] < value:
                    # Target is in the right half
                    text = "Data[" + str(self.mid) + "] < " + str(value) + ".\nValue is greater, so we get rid of all the values on the left side (greater values) of the middle (inclusive)."
                    for i in range(self.low, self.mid + 1):
                        self.colour_array[i] = 'red'
                    self.low = self.mid + 1
                else:
                    # Target is in the left half
                    text = "Data[" + str(self.mid) + "] > " + str(value) + ".\nValue is smaller, so we get rid of all the values on the right side (smaller values) of the middle (inclusive)."
                    for i in range(self.mid, self.high + 1):
                        self.colour_array[i] = 'red'
                    self.high = self.mid - 1

                self.states[self.state_index] = [copy.deepcopy(self.colour_array), text]
                self.state_index += 1
        
        if not self.found:
            # Target not found
            text = ""
            self.colour_array = ['grey'] * len(self.data)
            self.states[self.state_index] = [copy.deepcopy(self.colour_array), str(value) + " does not exist."]
            self.state_index += 1

            self.end = True


        # Establish variables for the start of the animation
        self.search_active = True
            
        # Run methods to start the actual animation
        self.set_slider_attributes()
        self.run_animation()
    
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