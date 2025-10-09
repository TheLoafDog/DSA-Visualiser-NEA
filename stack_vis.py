# Stack visualiser (inherited off Array):   Lines 17 - 503
# Peek:     Lines 37 - 62
# Pop:      Lines 64 - 99
# Push:     Lines 101 - 138


import copy
import customtkinter as ctk
import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import array_vis

class StackVisualiser(array_vis.ArrayVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

        # Attributes for the stack
        self.top = 3 # Points to the top item of the stack (its index)

        self.max = 7 # Maximum number of nodes in the static stack visualiser

        # Inherited attributes BELOW
        #self.data = [random.randint(-99, 99) for _ in range(4)] + ["" for _ in range(4)]
        #self.after_id = None
        #self.reset_animation_variables()
    
    def isEmpty(self):
        return self.top == 0
    
    def is_full(self):
        return self.top == self.max

    def peek(self):
        if self.isEmpty():
            self.output_message("Stack is empty. No top value to peek")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.top]

        # Simulate the animations
        self.highlight_nodes([self.top])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the top node", self.top]
        self.state_index += 1

        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Get the top value. Top value: {self.data[self.top]}", self.top]
        self.state_index += 1

        self.reset_node_highlights([self.top])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Top value: {self.data[self.top]}\nDeselect the top node", self.top]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def pop(self):
        if self.isEmpty():
            self.output_message("Stack is empty. Nothing to pop out")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.top]

        # Simulate the animations
        self.highlight_nodes([self.top])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the top node", self.top]
        self.state_index += 1

        self.update_node_value(self.top, "")
        highlighted_node = self.top
        self.top -= 1
        message = "Pop off the top value and decrement the top pointer"
        final_message = "Deselect the previous top node"

        if self.isEmpty():
            message += ". Stack is now empty"
            final_message += ". Stack is now empty"

        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.top]
        self.state_index += 1

        self.reset_node_highlights([highlighted_node])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), final_message, self.top]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def push(self, entry_value):
        if self.isFull():
            self.output_message("Stack is full. No space to push a value in")
            return

        try:
            value = int(entry_value)
        except ValueError:
            self.output_message("Invalid Input. Please enter an integer")
            return
        
        if value > 99 or value < -99:
            self.output_message("Invalid Input. Please enter an integer in the correct range")
            return

        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.top]

        # Simulate the animations
        self.top += 1
        self.highlight_nodes([self.top])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get next empty node", self.top]
        self.state_index += 1

        self.update_node_value(self.top, value)
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Push value into the top node", self.top]
        self.state_index += 1

        self.reset_node_highlights([self.top])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Deselect top node", self.top]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def setVis(self):
        # Split the page into: canvas, output, and UI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # self.canvas_frame holds the self.canvas which holds the self.graph (self.graph is in the form of self.canvas.get_tk_widget())
        # Canvas
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)

        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Array Stack Visualiser", font=("Arial", 26, "bold"))
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
        self.message_label = ctk.CTkLabel(self.message_frame, text="", wraplength=300, font=("Arial", 20))
        self.message_label.pack(expand=True)

        # Meta Data of stack - top index, length, capacity
        self.metadata_frame = ctk.CTkFrame(self)
        self.metadata_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.metadata_frame.propagate(False)
        
        self.metadata_title = ctk.CTkLabel(self.metadata_frame, fg_color="transparent", text="METADATA", font=("Arial Black", 20, "bold"))
        self.metadata_title.pack(pady=20)
        self.metadata_label = ctk.CTkLabel(self.metadata_frame, text="", wraplength=175, font=("Arial", 20))
        self.metadata_label.pack(expand=True)
        self.change_metadata()
        
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
        
        self.UI_holder.columnconfigure(0, weight=1)
        self.UI_holder.columnconfigure(1, weight=1)
        self.UI_holder.columnconfigure(2, weight=1)
        self.UI_holder.rowconfigure(0, weight=1)
        self.UI_holder.rowconfigure(1, weight=1)
        self.UI_holder.rowconfigure(2, weight=1)
        
        # Speed control
        self.speed_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.speed_frame.grid(row=0, column=1, pady=20, padx=10)
        self.speed_var = ctk.DoubleVar(value=700)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self.speed_frame, text="Speed (ms)")
        self.speed_label.pack(side="left", padx=10)

        self.speed_slider = ctk.CTkSlider(master=self.speed_frame, from_=1000, to=10, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, fill="x", expand=True)
        
        # Push
        self.push_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.push_frame.grid(row=1, column=1, pady=10, padx=10)
        self.push_label = ctk.CTkLabel(self.push_frame, text="Push value: (-99 to 99)")
        self.push_label.pack(side="top")
        self.push_entry = ctk.CTkEntry(self.push_frame, width=50)
        self.push_entry.pack(side="left")
        
        self.push_btn = ctk.CTkButton(
            self.push_frame, height=30, width=80, text="Push", 
            command=lambda: self.push(self.push_entry.get())
        )
        self.push_btn.pack(side="left", padx=3)
        
        # Pop
        self.pop_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Pop",
            command=lambda: self.pop()
        )
        self.pop_btn.grid(row=2, column=1, pady=10, padx=10)

        # Peek
        self.peek_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Peek",
            command=lambda: self.peek()
        )
        self.peek_btn.grid(row=2, column=0, pady=10, padx=10)

        # Clear stack
        self.clear_stack_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Clear stack",
            command=lambda: self.generate_stack()
        )
        self.clear_stack_btn.grid(row=1, column=0)
        
        # Generate random stack
        self.generate_stack_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.generate_stack_frame.grid(row=0, column=0, pady=10, padx=10)
        self.generate_stack_label = ctk.CTkLabel(self.generate_stack_frame, text="Generate stack of length: (no entry = length of 4)")
        self.generate_stack_label.pack(side="top")
        self.generate_stack_entry = ctk.CTkEntry(self.generate_stack_frame, width=50)
        self.generate_stack_entry.pack(side="left", expand=True)
        
        self.generate_stack_btn = ctk.CTkButton(
            self.generate_stack_frame, height=30, width=80, text="Generate Random",
            command=lambda: self.generate_stack(length=self.generate_stack_entry.get())
        )
        self.generate_stack_btn.pack(side="right", expand=True, padx=3)
    
    def setGraph(self):
        # Add nodes based on the stack
        for index, element in enumerate(self.data):
            self.graph.add_node(index, value=element) # Add nodes with values = element and index = indentifier
        
        # Define fixed positions for the nodes
        scale_factor = 0.75 # Defines how close the nodes are together
        total_width = (len(self.data) - 1) * scale_factor # Gets width of occupied space by the nodes
        center_offset = total_width / 8
        self.pos = {i: (0, i * scale_factor + center_offset) for i in range(len(self.data))}  # Horizontal positions aligned
        
        # Adjust the labels so that they are the elements and not the indexes
        self.labels = nx.get_node_attributes(self.graph, 'value')
        
        # Create GUI components
        self.canvas_frame = ctk.CTkFrame(self)
        
        # Plot canvas for the graph
        self.figure, self.ax = plt.subplots(figsize=(2, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        
        self.padding = 0.5
        self.ax.set_xlim(-1-self.padding, 1 + self.padding) # X-axis for fixed vertical position
        self.ax.set_ylim(-self.padding, len(self.data) - 1 + self.padding) # Y-axis for horizontal layout

        self.node_colours = ['lightblue' for _ in range(len(self.data))] # Default colour for all nodes

        self.draw_stack()


    def draw_stack(self, **kwargs):
        labels = kwargs.get('labels', self.labels)
        colour_list = kwargs.get('colour_array', self.node_colours)
        top = kwargs.get('top', self.top) # Top pointer index
        
        self.ax.clear()

        # Draw the graph
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            labels=labels,
            node_size=650,
            node_color=colour_list,
            node_shape="s",
            edgecolors="black",
            ax=self.ax,
            linewidths=2
        )

        # Add index below each node
        for index, (x, y) in self.pos.items():
            self.ax.text(
                x - 0.65,
                y,
                str(index),
                ha='center',
                va='center',
                fontsize=10,
                color='black'
            )

        # Draw top pointer
        if top is not None and top != -1:
            x, y = self.pos[top]
            self.ax.annotate(
                "top",
                xy=(x + 0.5, y),  # Arrow tip position
                xytext=(x + 1.5, y),  # Label position
                ha='center',
                va='center',
                color='blue',
                arrowprops=dict(facecolor='blue', shrink=0.05)
            )

        # Swap around the x and y limits for the stack compared to the queue or array
        self.ax.set_xlim(-1 - self.padding, 1 + self.padding)
        self.ax.set_ylim(-self.padding, len(self.data)-1 + self.padding)

        self.canvas.draw()

    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            labels = self.states[self.animation_index][0]
            colour_array = self.states[self.animation_index][1]
            top = self.states[self.animation_index][3]
            self.draw_stack(labels=labels, colour_array=colour_array, top=top)

            self.change_metadata(top=top, length=top)
            text = self.states[self.animation_index][2]
            self.output_message(text)
            self.change_metadata()
            
            self.after_increment = self.after(int(self.speed_var.get()), lambda: self.increment_slider())
            self.after_id = self.after(int(self.speed_var.get()), lambda: self.run_animation())
        else:
            self.stop_button.configure(text="↺", command=lambda: self.restart_visualiser())

    def adjust_canvas(self):
        # Pause the sort
        self.is_running = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)
            
        # Next set the sort visualiser in relation to the slider value
        labels = self.states[self.animation_index][0]
        colour_array = self.states[self.animation_index][1]
        top = self.states[self.animation_index][3]
        self.draw_stack(labels=labels, colour_array=colour_array, top=top)

        self.change_metadata(top=top, length=top)
        text = self.states[self.animation_index][2]
        self.output_message(text)
    
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
            self.draw_stack(labels=labels, colour_array=colour_array)
            self.output_message(self.states[value][2])
            
            self.animation_index = value
            
            self.last_slider_value = value

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

    def generate_stack(self, length=0):
        self.reset_animation_variables()
        try:
            if length == "":
                length = random.randint(2,7) # If the entry is left empty, then a random stack will be generated
            else:
                length = int(length)
        except ValueError:
            self.output_message("Input invalid. Please enter valid integers.")
            return
        
        if length > 8 or length < 0:
            self.output_message("Invalid input. Index not in suitable range.")
            return

        # Variables for stack
        self.top = length-1 # Index position of the last value
        if length == 0:
            self.top = 0
        self.data = [random.randint(-99, 99) for _ in range(length)] + ["" for _ in range(8-length)]  # Whole stack including NULL values
        
        self.labels = {}
        for i, value in enumerate(self.data):
            self.labels[i] = value
        self.node_colours = ['lightblue' for _ in range(len(self.data))]  # Default colour for all nodes
        
        if length == 0:
            self.output_message("Queue cleared.")
        else:
            self.output_message("Queue with random elements of length " + str(length) + " generated.")
        self.draw_stack()


    def isFull(self): # When the top pointer has reached the max number of nodes the static queue goes up to (index 7)
        if self.top == self.max and self.data[self.top]:
            return True
        else:
            return False

    def isEmpty(self): # Used to check whether the queue is empty or not (can return True for invalid stacks, so when the stack is no longer valid, then it disables the UI)
        return self.top == -1

    def change_metadata(self, **kwargs):
        top = kwargs.get('top', self.top)
        length = kwargs.get('length', self.top)
        if self.isEmpty:
            length = 0
        text = f"Top index: {top}\nLength: {length}\nCapacity: 8"

        self.metadata_label.configure(text=text)

def main(master, window):
    window.geometry("960x1060")
    window.minsize(960, 1060)
    
    vis = StackVisualiser(master)
    vis.pack(fill="both", expand=True)
    vis.setGraph()
    vis.setVis()
