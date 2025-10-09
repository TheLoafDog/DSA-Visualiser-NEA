# generate_array:   Lines 374 - 401
# search_node:      Lines 403 - 453
# find_minmax_node: Lines 455 - 524
# edit_node:        Lines 526 - 560
# remove_node:      Lines 560 - 600
# insert_node:      Lines 603 - 638

import copy
import customtkinter as ctk
import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ArrayVisualiser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="gray")
        self.master = master
        
        self.graph = nx.Graph()

        # Variables for array
        self.lenFilled = 4  # Length of array that is filled (not index)
        self.data = [random.randint(-99, 99) for _ in range(4)] + ["" for _ in range(4)]  # Whole array including NULL values
        
        # Variables for animation
        self.after_id = None
        self.after_increment = None
        self.reset_animation_variables()

    def setGraph(self):
        # Add nodes based on the array
        for index, element in enumerate(self.data):
            self.graph.add_node(index, value=element) # Add nodes with values = element and index = indentifier
        
        # Define fixed positions for the nodes
        scale_factor = 0.75 # Defines how close the nodes are together
        total_width = (len(self.data) - 1) * scale_factor # Gets width of occupied space by the nodes
        center_offset = total_width / 8
        self.pos = {i: (i * scale_factor + center_offset, 0) for i in range(len(self.data))}  # Horizontal positions aligned
        
        # Adjust the labels so that they are the elements and not the indexes
        self.labels = nx.get_node_attributes(self.graph, 'value')
        
        # Create GUI components
        self.canvas_frame = ctk.CTkFrame(self)
        
        # Plot canvas for the graph
        self.figure, self.ax = plt.subplots(figsize=(6, 2))
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        
        self.padding = 0.5
        self.ax.set_xlim(-self.padding, len(self.data) - 1 + self.padding)  # X-axis for horizontal layout
        self.ax.set_ylim(-1-self.padding, 1 + self.padding)  # Y-axis for fixed vertical position
        
        self.node_colours = ['lightblue' for _ in range(len(self.data))] # Default colour for all nodes

        self.draw_array()

    def setVis(self):
        # Split the page into: canvas, output, and UI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # self.canvas_frame holds the self.canvas which holds the self.graph (self.graph is in the form of self.canvas.get_tk_widget())
        # Canvas
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Array Visualiser", font=("Arial", 26, "bold"))
        self.canvas_title.pack(pady=20)

        self.canvas.get_tk_widget().pack(expand=True)
        
        self.playback_holder = ctk.CTkFrame(master=self.canvas_frame, fg_color="transparent", border_width=0)
        self.playback_holder.pack(pady=5)
        self.playback_slider = ctk.CTkSlider(master=self.playback_holder, height=20, border_color="black", command=self.on_slider_move)
        self.playback_slider.pack(pady=10, side="left")
        self.playback_slider.configure(state="disabled")
        self.last_slider_value = None
        
        self.edit_playback_frame = ctk.CTkFrame(master=self.playback_holder, fg_color="transparent", border_width=0)
        self.edit_playback_frame.pack(pady=5, padx=5)
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
        
        # Log
        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.grid(row=0, column=1, sticky="nsew", pady=10, padx=10)
        self.message_frame.propagate(False)
        
        self.message_title = ctk.CTkLabel(self.message_frame, fg_color="transparent", text="LOG", font=("Arial Black", 20, "bold"))
        self.message_title.pack(pady=20)
        self.message_label = ctk.CTkLabel(self.message_frame, text="", wraplength=150, font=("Arial", 20))
        self.message_label.pack(expand=True)
        
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
        
        self.UI_holder.columnconfigure(0, weight=1)
        self.UI_holder.columnconfigure(1, weight=1)
        self.UI_holder.columnconfigure(2, weight=1)
        
        # Speed control
        self.speed_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.speed_frame.grid(row=0, column=1, pady=20, padx=10)
        self.speed_var = ctk.DoubleVar(value=700)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self.speed_frame, text="Speed (ms)")
        self.speed_label.pack(side="left", padx=10)

        self.speed_slider = ctk.CTkSlider(master=self.speed_frame, from_=1000, to=10, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, fill="x", expand=True)
        
        # Insertion
        self.insert_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.insert_frame.grid(row=1, column=1, pady=10, padx=10)
        self.insert_label = ctk.CTkLabel(self.insert_frame, text="Insert value: (-99 to 99)")
        self.insert_label.pack(side="top")
        self.insert_entry = ctk.CTkEntry(self.insert_frame, width=50)
        self.insert_entry.pack(side="left")
        
        self.insert_btn = ctk.CTkButton(
            self.insert_frame, height=30, width=80, text="Insert", 
            command=lambda: self.insert_node(self.insert_entry.get())
        )
        self.insert_btn.pack(side="left", padx=3)
        
        # Deletion
        self.remove_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.remove_frame.grid(row=2, column=1, pady=10, padx=10)
        self.remove_label = ctk.CTkLabel(self.remove_frame, text="Remove value at index: (0 to 7)")
        self.remove_label.pack(side="top")
        self.remove_entry = ctk.CTkEntry(self.remove_frame, width=50)
        self.remove_entry.pack(side="left", expand=True)
        
        self.remove_btn = ctk.CTkButton(
            self.remove_frame, height=30, width=80, text="Remove",
            command=lambda: self.remove_node(self.remove_entry.get())
        )
        self.remove_btn.pack(side="right", padx=3)
        
        # Edit
        self.edit_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.edit_frame.grid(row=2, column=2, pady=10, padx=10)     
        self.edit_label = ctk.CTkLabel(self.edit_frame, text="Edit Value")
        self.edit_label.pack(side="top")
        self.edit_index_label = ctk.CTkLabel(self.edit_frame, text="Index: ")
        self.edit_index_label.pack(side="left")
        self.edit_index_entry = ctk.CTkEntry(self.edit_frame, width=50)
        self.edit_index_entry.pack(side="left")
        self.edit_value_label = ctk.CTkLabel(self.edit_frame, text="Value: ")
        self.edit_value_label.pack(side="left")
        self.edit_value_entry = ctk.CTkEntry(self.edit_frame, width=50)
        self.edit_value_entry.pack(side="left")
        
        self.edit_btn = ctk.CTkButton(
            self.edit_frame, height=30, width=80, text="Edit", 
            command=lambda: self.edit_node(self.edit_value_entry.get(), self.edit_index_entry.get())
        )
        self.edit_btn.pack(side="left", padx=3)
        
        # Max and Min
        self.min_max_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.min_max_frame.grid(row=2, column=0, pady=10, padx=10)
        self.min_max_label = ctk.CTkLabel(self.min_max_frame, text="Find Min or Max nodes")
        self.min_max_label.pack(side="top")
        
        self.min_btn = ctk.CTkButton(
            self.min_max_frame, height=30, width=80, text="Min",
            command=lambda: self.find_minmax_node(False)
        )
        self.min_btn.pack(side="left", expand=True, padx=3)
        
        self.max_btn = ctk.CTkButton(
            self.min_max_frame, height=30, width=80, text="Max",
            command=lambda: self.find_minmax_node(True)
        )
        self.max_btn.pack(side="right", expand=True, padx=3)
        
        # Search
        self.search_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.search_frame.grid(row=1, column=2, pady=10, padx=10)
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search node value: ")
        self.search_label.pack(side="top")
        self.search_entry = ctk.CTkEntry(self.search_frame, width=50)
        self.search_entry.pack(side="left", expand=True)
        
        self.search_btn = ctk.CTkButton(
            self.search_frame, height=30, width=80, text="Search",
            command=lambda: self.search_node(self.search_entry.get())
        )
        self.search_btn.pack(side="right", padx=3)
        
        # Clear array
        self.clear_array_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Clear Array",
            command=lambda: self.generate_array()
        )
        self.clear_array_btn.grid(row=1, column=0)
        
        # Generate random array
        self.generate_array_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.generate_array_frame.grid(row=0, column=0, pady=10, padx=10)
        self.generate_array_label = ctk.CTkLabel(self.generate_array_frame, text="Generate array of length: (no entry = length of 4)")
        self.generate_array_label.pack(side="top")
        self.generate_array_entry = ctk.CTkEntry(self.generate_array_frame, width=50)
        self.generate_array_entry.pack(side="left", expand=True)
        
        self.generate_array_btn = ctk.CTkButton(
            self.generate_array_frame, height=30, width=80, text="Generate Random",
            command=lambda: self.generate_array(length=self.generate_array_entry.get())
        )
        self.generate_array_btn.pack(side="right", expand=True, padx=3)

    def adjust_canvas(self):
        # Pause the sort
        self.is_running = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)
            
        # Next set the sort visualiser in relation to the slider value
        labels = self.states[self.animation_index][0]
        colour_array = self.states[self.animation_index][1]
        text = self.states[self.animation_index][2]
        self.output_message(text)
        self.draw_array(labels=labels, colour_array=colour_array)

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

    def decrement_slider(self):
        self.playback_slider.set(self.playback_slider.get()-1)
        self.animation_index = self.playback_slider.get()
        self.adjust_canvas()

    def skip_animation(self):
        self.animation_index = len(self.states)-1
        self.playback_slider.set(self.animation_index)
        self.adjust_canvas()

    def reset_animation_variables(self):
        # Variables for animation
        self.is_running = False # To check whether the animation is running or paused
        # Cancel any scheduled events by using after_id
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_cancel(self.after_increment)
            self.after_id = None  # Reset after_id since it is no longer active
            self.after_increment = None
        self.states = {} # Hash table to hold the data for each step in the animation
        self.state_index = 1 # Index for storing the states after each step in the simulation
        self.animation_index = 0 # Index for outputting during the animation
        
    def draw_array(self, **kwargs):
        labels = kwargs.get('labels', self.labels)
        colour_list = kwargs.get('colour_array', self.node_colours)

        self.ax.clear()
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            labels=labels, # Custom labels due to nature of nodes
            node_size=1000, # Adjusted the node size so that they are touching each other
            node_color=colour_list,
            node_shape="s",
            edgecolors="black",
            ax=self.ax,
            linewidths=2
        )
        
        for index, (x, y) in self.pos.items():  # Index below node
            self.ax.text(
                x,
                y - 0.65,
                str(index),
                ha='center',
                va='center',
                fontsize=10,
                color='black'
            )

        self.ax.set_xlim(-self.padding, len(self.data)-1 + self.padding)
        self.ax.set_ylim(-1 - self.padding, 1 + self.padding)
        
        self.canvas.draw()
    
    def set_slider_attributes(self):
        self.playback_slider.set(0)
        self.playback_slider.configure(from_=0, to=len(self.states)-1, number_of_steps=len(self.states)-1)
        # Reactivate slider and other buttons
        self.playback_slider.configure(state="normal")
        self.stop_button.configure(state="normal", text="| |", command=self.toggle_pause)
        for button in self.edit_buttons:
            button.configure(state="normal")
    
    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            labels = self.states[self.animation_index][0]
            colour_array = self.states[self.animation_index][1]
            self.draw_array(labels=labels, colour_array=colour_array)

            message = self.states[self.animation_index][2]
            self.output_message(message)
            
            self.after_increment = self.after(int(self.speed_var.get()), lambda: self.increment_slider())
            self.after_id = self.after(int(self.speed_var.get()), lambda: self.run_animation())
        else:
            self.stop_button.configure(text="↺", command=lambda: self.restart_visualiser())

    def restart_visualiser(self, play=True):
        self.is_running = play

        self.stop_button.configure(command=self.toggle_pause) # Reset command for stop button

        # Establish variables for the start of the animation
        self.animation_index = 0
        self.sort_active = True
            
        # Run methods to start the actual animation
        self.set_slider_attributes()
        
        if not self.is_running:
            self.stop_button.configure(text="▷")
            self.adjust_canvas()

        self.run_animation()
    
    def generate_array(self, length=0):
        self.reset_animation_variables()
        try:
            if length == "":
                length = random.randint(2,7) # If the entry is left empty, then a random array will be generated
            else:
                length = int(length)
        except ValueError:
            self.output_message("Input invalid. Please enter valid integers.")
            return
        
        if length > 8 or length < 0:
            self.output_message("Invalid input. Index not in suitable range.")
            return

        # Variables for array
        self.lenFilled = length  # Length of array that is filled (not index)
        self.data = [random.randint(-99, 99) for _ in range(length)] + ["" for _ in range(8-length)]  # Whole array including NULL values
        
        self.labels = {}
        for i, value in enumerate(self.data):
            self.labels[i] = value
        self.node_colours = ['lightblue' for _ in range(len(self.data))]  # Default colour for all nodes
        
        if length == 0:
            self.output_message("Array cleared.")
        else:
            self.output_message("Array with random elements of length " + str(length) + " generated.")
        self.draw_array()
        
    def search_node(self, entry_value):
        # Check if the array is full
        if self.lenFilled == 0:
            self.output_message("Array is empty.")
            return

        try:
            value = int(entry_value)  # Convert entry to integer
        except ValueError:
            self.output_message("Invalid input. Please enter valid integers.")
            return
        
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), ""]
        indexes = [] # Holds the indexes of the nodes with the desired value

        # Simulate the animation first
        for i in range(0, self.lenFilled):
            change = False
            self.highlight_nodes([i])
            if self.data[i] == value:
                indexes.append(i)
                self.highlight_nodes([i], colour="orange")
                change = True
                
            text = "Checking node at index: " + str(i) + "."
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of current state
            self.state_index += 1 # Increment state index
            
            if not change:
                self.reset_node_highlights([i])
        
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours)] # Add data of current state          

        if indexes:
            text = "Value found at indexes: \n"
        else:
            text = "Value not found in array##"

        for i in indexes:
            text += str(i) + ", "

        self.states[self.state_index].append(text[:-2])
        self.reset_node_highlights(indexes)
        
        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()
    
    def find_minmax_node(self, boolean): # True means Max, False means Min
        # Check if array is not empty
        if self.lenFilled == 0:
            self.output_message("Array is empty.")
            return
        
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.highlight_nodes([0])
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Check value at index 0."]
        self.highlight_nodes([0], colour="orange")

        indexes = [] # Holds the indexes of the nodes with the desired value
        current = self.data[0]
        indexes.append(0)
        
        # Simulate the algorithm first, adding to states each step
        for i in range(1, self.lenFilled):
            text = "Value of node at index " + str(i)
            change = False # Checks whether a change has been made
            self.highlight_nodes([i])
            if self.data[i] == current:
                text += " the same as the current value so its index will also be recorded."
                indexes.append(i)
                self.highlight_nodes([i])
                change = True
                
            if boolean:
                if self.data[i] > current:  # Check if the value is higher than the current highest
                    text += " is greater than the current max value so it is the new max value.\n" + str(self.data[i]) + " > " + str(current)
                    current = self.data[i]
                    self.reset_node_highlights(indexes)
                    self.highlight_nodes([i])
                    indexes.append(i)
                    change = True
                else:
                    text += " is less than the current max value so no change occurs.\n" + str(self.data[i]) + " < " + str(current)
            else:
                if int(self.data[i]) < current: # Check if the value is lower than the current lowest
                    text += " is less than the current min value so it is the new min value.\n" + str(self.data[i]) + " < " + str(current)
                    current = self.data[i]
                    self.reset_node_highlights(indexes)
                    self.highlight_nodes([i])
                    indexes.append(i)
                    change = True
                else:
                    text += " is greater than the current max value so no change occurs.\n" + str(self.data[i]) + " > " + str(current)
                
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of current state
            self.state_index += 1 # Increment state index

            self.highlight_nodes([i], colour="orange")
            
            if not change:
                self.reset_node_highlights([i])
            
        if boolean:
            text = "Max value = " + str(current)
        else:
            text = "Min value = " + str(current)
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of last state

        # Reset highlighted nodes once info is stored
        self.reset_node_highlights(indexes)

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
            
        self.run_animation()
    
    def edit_node(self, entry_value, index):
        try:
            index = int(index)
            value = int(entry_value)
        except:
            self.output_message("Invalid input. Please enter an integer for the index or value.")
            return
        
        if index < 0 or index > (self.lenFilled-1): # Check if index is not in range
            self.output_message("Invalid input. Please enter an index with data.")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), ""]

        # Establish actions and text for the animation
        actions = [
            ["Select the node at the desired index", lambda: self.highlight_nodes([index])], 
            ["Update the node value from " + str(self.data[index]) + " to " + str(value), lambda: self.update_node_value(index, value)], # Change label of node on the graph
            ["The node at index " + str(index) + " has been successfully editted", lambda: self.reset_node_highlights([index])]
        ]

        # Simulate the algorithm first, adding to states each step
        for text, action in actions:
            action() # Perform the action
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of current state
            self.state_index += 1 # Increment state index
        
        self.is_running = True
        self.set_slider_attributes() # Give data to slider
            
        self.run_animation()

    def remove_node(self, entry_value):
        try:
            value = int(entry_value)  # Convert entry to integer
        except ValueError:
            self.output_message("Invalid input. Please enter an integer.")
            return

        # Check if the index is in range
        if value >= self.lenFilled or value < 0:
            self.output_message("Invalid input. Index not in suitable range.")
            return
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), ""]
        
        # Establish actions for the animation
        actions = [
            ["Select node at index " + str(value) + " which needs its value to be removed", lambda: self.highlight_nodes([value])],
            ["Remove node value", lambda: self.update_node_value(value, "")], # Change label of node on the graph
            ["Unselect node", lambda: self.reset_node_highlights([value])]
        ]
        
        # Make the actions to be performed
        for i in range(value + 1, self.lenFilled):
            actions.append(["Select nodes which need to switch their values", lambda index=i: self.highlight_nodes([index-1, index])])
            actions.append(["Switch values of nodes at indexes " + str(i-1) + " and " + str(i), lambda index=i: self.swap_nodes(index-1, index)])
            actions.append(["Unselect nodes", lambda index=i: self.reset_node_highlights([index-1, index])])
        
        # Simulate the algorithm first, adding to states each step
        for text, action in actions:
            action() # Perform the action
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of current state
            self.state_index += 1 # Increment state index
            
        self.lenFilled -= 1
        
        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()
    
    def insert_node(self, entry_value):
        # Check if the array is full
        if self.lenFilled == len(self.data):
            self.output_message("Array is full.")
            return
        
        try:
            value = int(entry_value)  # Convert entry to integer
        except ValueError:
            self.output_message("Invalid input. Please enter valid integers.")
            return
        
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), ""]
        
        # Establish actions for the animation
        actions = [
            ["Select next available node. Node at index " + str(self.lenFilled), lambda: self.highlight_nodes([self.lenFilled])],
            ["Insert " + str(value) + " into array", lambda: self.update_node_value(self.lenFilled, value)], # Change label of node on the graph
            ["Unselect node", lambda: self.reset_node_highlights([self.lenFilled])]
        ]
        
        # Simulate the algorithm first, adding to states each step
        for text, action in actions:
            action() # Perform the action
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), text] # Add data of current state
            self.state_index += 1 # Increment state index
        
        self.lenFilled += 1
        
        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()
    
    def toggle_pause(self):        
        if not self.is_running:
            self.is_running = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.is_running = False
            self.stop_button.configure(text="▷")

    def swap_nodes(self, n1_index, n2_index):
        #Update the label of the node and redraw the graph.
        self.data[n1_index], self.data[n2_index] = self.data[n2_index], self.data[n1_index]  # Update the array
        self.labels[n1_index], self.labels[n2_index] = self.labels[n2_index], self.labels[n1_index]  # Update the label for the graph
        
    def on_slider_move(self, value):
        value=int(value)
        if self.last_slider_value != value:
            # Cancel any scheduled events by using after_id
            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_cancel(self.after_increment)
                self.after_id = None  # Reset after_id since it is no longer active
                self.after_increment = None
                
            # Pause the sort
            self.is_running = False
            self.stop_button.configure(text="▷")
            # In case the animation finished and the command changes, reset command for stop button
            self.stop_button.configure(command=self.toggle_pause)
            
            labels = self.states[value][0]
            colour_array = self.states[value][1]
            self.draw_array(labels=labels, colour_array=colour_array)
            self.output_message(self.states[value][2])
            
            self.animation_index = value
            
            self.last_slider_value = value

    def update_node_value(self, index, value):
        # Update the label of the node.
        self.data[index] = value  # Update the array
        self.labels[index] = value  # Update the label for the graph
        
    def increment_slider(self):
        self.playback_slider.set(self.playback_slider.get()+1)
        self.animation_index += 1
        
    def reactivate_slider(self):
        self.playback_slider.configure(state="normal")
        # This is separate to the other buttons due to having a different master

    def highlight_nodes(self, node_indexes, colour='red'):
        for node_index in node_indexes:
            self.node_colours[node_index] = colour
        
    def reset_node_highlights(self, node_indexes, colour='lightblue'):
        self.highlight_nodes(node_indexes, colour=colour)

    def output_message(self, text):
        self.message_label.configure(text=text)

def main(master, window):
    vis = ArrayVisualiser(master)
    window.geometry("1280x820")
    window.minsize(1280, 820)
    
    vis.setGraph()
    vis.setVis()
    vis.pack(fill="both", expand=True)
