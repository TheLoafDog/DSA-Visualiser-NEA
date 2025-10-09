# Basic Queue class (inherited from Array):             Lines 15 - 525
# Circular Queue class (inherited from Basic Queue):    Lines 527 - 1094
# Priority Queue class (inherited from Basic Queue):    Lines 1096 - 1380

import copy
import customtkinter as ctk
import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import array_vis

class QueueVisualiser(array_vis.ArrayVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

        # Attributes for the queue
        self.rear = 3 # Points to the last item in the queue
        self.front = 0 # Points to the first stored value

        self.max = 7 # Maximum index in the static queue visualiser

        # Inherited attributes BELOW
        #self.data = [random.randint(-99, 99) for _ in range(4)] + ["" for _ in range(4)]
        #self.after_id = None
        #self.after_increment = None
        #self.reset_animation_variables()

    def peek(self):
        if not self.checkIfValid():
            self.output_message("Queue is no longer valid. Reset the array by clearing it")
            return
        
        if self.isEmpty():
            self.output_message("Queue is empty. No front value to peek")
            return
        
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        # Simulate the animations
        self.highlight_nodes([self.front])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
        self.state_index += 1

        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front]}", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([self.front])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front]}\nDeselect the front node", self.front, self.rear]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def dequeue(self):
        if not self.checkIfValid():
            self.output_message("Queue is no longer valid. Reset the array by clearing it")
            return
        
        if self.isEmpty():
            self.output_message("Queue is empty. No values to remove")
            return

        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        # Simulate the animations
        self.highlight_nodes([self.front])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
        self.state_index += 1

        message = "Deselect previous front node"
        self.update_node_value(self.front, "")
        if not self.isEmpty():
            highlighted_node = self.front
            self.front += 1
        else:
            message += ". Queue is now empty"
            highlighted_node = self.front

        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Remove front value and increment front pointer", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([highlighted_node])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def enqueue(self, entry_value):
        if not self.isEmpty(): # Check if queue is not empty
            if not self.checkIfValid(): # Check whether the queue is not valid
                self.output_message("Queue is no longer valid. Reset the array by clearing it")
                return
        
            if self.isFull(): # Check if adding a value will result in overflow error
                self.output_message("Queue is full")
                return
        
        try: # Check input type
            value = int(entry_value)
        except ValueError:
            self.output_message("Invalid input. Please enter an integer")
            return
        
        if value < -99 or value > 99: # Check input range
            self.output_message("Invalid input. Value not in suitable range")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        self.highlight_nodes([self.rear])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get current rear node and check if it is empty", self.front, self.rear]
        self.state_index += 1

        # Simulate the animations
        if not self.isEmpty():
            self.reset_node_highlights([self.rear])
            self.rear += 1
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Rear node is not empty so deselect the node and increment the rear pointer", self.front, self.rear]
            self.state_index += 1

            self.highlight_nodes([self.rear])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Highlight the empty node at the rear pointer", self.front, self.rear]
            self.state_index += 1

        self.update_node_value(self.rear, value)
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Insert the value: {value}, at the rear pointer", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([self.rear])
        message = "Deselect the node"
        if self.rear == self.max:
            message += ". Queue is now full"
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
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
        
        # self.canvas_frame holds the self.canvas which holds the self.graph (self.graph is in the form of self.canvas.get_tk_widget())
        # Canvas
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Array Queue Visualiser", font=("Arial", 26, "bold"))
        self.canvas_title.pack(pady=20)

        self.canvas.get_tk_widget().pack(expand=True)
        
        self.playback_holder = ctk.CTkFrame(master=self.canvas_frame, fg_color="transparent")
        self.playback_holder.pack(pady=5)
        self.playback_slider = ctk.CTkSlider(master=self.playback_holder, height=20, border_color="black", command=self.on_slider_move)
        self.playback_slider.pack(pady=10, side="left")
        self.playback_slider.configure(state="disabled")
        self.last_slider_value = None
        
        self.edit_playback_frame = ctk.CTkFrame(master=self.playback_holder, fg_color="transparent")
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

        # Meta Data of queue - front index, rear index, length, valid
        self.metadata_frame = ctk.CTkFrame(self)
        self.metadata_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.metadata_frame.propagate(False)
        
        self.metadata_title = ctk.CTkLabel(self.metadata_frame, fg_color="transparent", text="METADATA", font=("Arial Black", 20, "bold"))
        self.metadata_title.pack(pady=20)
        self.metadata_label = ctk.CTkLabel(self.metadata_frame, text="", wraplength=320, font=("Arial", 20))
        self.metadata_label.pack(expand=True)
        self.change_metadata()
        
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
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
        
        # Enqueue
        self.enqueue_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.enqueue_frame.grid(row=1, column=1, pady=10, padx=10)
        self.enqueue_label = ctk.CTkLabel(self.enqueue_frame, text="Enqueue value: (-99 to 99)")
        self.enqueue_label.pack(side="top")
        self.enqueue_entry = ctk.CTkEntry(self.enqueue_frame, width=50)
        self.enqueue_entry.pack(side="left")
        
        self.enqueue_btn = ctk.CTkButton(
            self.enqueue_frame, height=30, width=80, text="Enqueue", 
            command=lambda: self.enqueue(self.enqueue_entry.get())
        )
        self.enqueue_btn.pack(side="left", padx=3)
        
        # Dequeue
        self.dequeue_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Dequeue",
            command=lambda: self.dequeue()
        )
        self.dequeue_btn.grid(row=2, column=1, pady=10, padx=10)

        # Peek
        self.peek_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Peek",
            command=lambda: self.peek()
        )
        self.peek_btn.grid(row=2, column=0, pady=10, padx=10)

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
    
    def draw_array(self, **kwargs):
        labels = kwargs.get('labels', self.labels)
        colour_list = kwargs.get('colour_array', self.node_colours)
        front = kwargs.get('front', self.front) # Front pointer index
        rear = kwargs.get('rear', self.rear) # Rear pointer index
        
        self.ax.clear()

        # Draw the graph
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            labels=labels,
            node_size=1000,
            node_color=colour_list,
            node_shape="s",
            edgecolors="black",
            ax=self.ax,
            linewidths=2
        )

        # Add index below each node
        for index, (x, y) in self.pos.items():
            self.ax.text(
                x,
                y - 0.65,
                str(index),
                ha='center',
                va='center',
                fontsize=10,
                color='black'
            )

        # Draw front pointer
        if front is not None:
            x, y = self.pos[front]
            self.ax.annotate(
                "Front",
                xy=(x, y + 0.5),  # Arrow tip position
                xytext=(x, y + 1.5),  # Label position
                ha='center',
                va='center',
                color='blue',
                arrowprops=dict(facecolor='blue', shrink=0.05)
            )

        # Draw rear pointer
        if rear is not None:
            x, y = self.pos[rear]
            if rear == front:
                # If front and rear are the same, place rear below the node
                self.ax.annotate(
                    "Rear",
                    xy=(x, y - 0.75),  # Arrow tip position
                    xytext=(x, y - 1.75),  # Label position
                    ha='center',
                    va='center',
                    color='red',
                    arrowprops=dict(facecolor='red', shrink=0.05)
                )
            else:
                # Otherwise, place rear above the node
                self.ax.annotate(
                    "Rear",
                    xy=(x, y + 0.5),  # Arrow tip position
                    xytext=(x, y + 1.5),  # Label position
                    ha='center',
                    va='center',
                    color='red',
                    arrowprops=dict(facecolor='red', shrink=0.05)
                )

        self.ax.set_xlim(-self.padding, len(self.data)-1 + self.padding)
        self.ax.set_ylim(-1 - self.padding, 1 + self.padding)

        self.canvas.draw()

    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            labels = self.states[self.animation_index][0]
            colour_array = self.states[self.animation_index][1]
            front = self.states[self.animation_index][3]
            rear = self.states[self.animation_index][4]
            self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear)

            self.change_metadata(front=front, rear=rear, length=(rear-front), valid=self.checkIfValid(front=front))
            text = self.states[self.animation_index][2]
            self.output_message(text)
            
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
        front = self.states[self.animation_index][3]
        rear = self.states[self.animation_index][4]
        self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear)

        self.change_metadata(front=front, rear=rear, length=(rear-front), valid=self.checkIfValid(front=front))
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
            front = self.states[self.animation_index][3]
            rear = self.states[self.animation_index][4]
            self.draw_array(labels=labels, colour_array=colour_array)
            self.output_message(self.states[value][2])
            self.change_metadata(front=front, rear=rear, length=(rear-front), valid=self.checkIfValid(front=front))
            
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

    def generate_array(self, length=0):
        self.reset_animation_variables()
        try:
            if length == "":
                length = random.randint(2,7) # If the entry is left empty, then a random array will be generated
            else:
                length = int(length)
        except ValueError:
            self.output_message("Input invalid. Please enter valid integers")
            return
        
        if length > 8 or length < 0:
            self.output_message("Invalid input. Index not in suitable range")
            return
        
        # Variables for array
        self.rear = length-1  # Length of array that is filled (not index)
        self.front = 0
        if length == 0:
            self.rear += 1
        self.data = [random.randint(-99, 99) for _ in range(length)] + ["" for _ in range(8-length)]  # Whole array including NULL values
        
        self.labels = {}
        for i, value in enumerate(self.data):
            self.labels[i] = value
        self.node_colours = ['lightblue' for _ in range(len(self.data))]  # Default colour for all nodes
        
        if length == 0:
            self.output_message("Queue cleared")
        else:
            self.output_message("Queue with random elements of length " + str(length) + " generated")
        self.change_metadata()
        self.draw_array()

    def isFull(self): # When the rear pointer has reached the max number of nodes the static queue goes up to (index 7)
        return self.rear == self.max and self.data[7]

    def isEmpty(self): # Used to check whether the queue is empty or not (can return True for invalid arrays, so when the array is no longer valid, then it disables the UI)
        return self.rear == self.front and not self.data[self.front] # The front pointer and rear pointer can point at the same index if there is one value in the queue

    def checkIfValid(self, **kwargs): # When the queue can no longer be used, when the front and rear reach index 7, run this method before every 
        front = kwargs.get('front', self.front)
        return not(front == self.max and not self.data[front]) # The front pointer and rear pointer can point at the same index if there is one value at the end.

    def change_metadata(self, **kwargs):
        front = kwargs.get('front', self.front)
        rear = kwargs.get('rear', self.rear)
        length = kwargs.get('length', self.rear-self.front)
        valid = kwargs.get('valid', self.checkIfValid())

        if self.data[7]:
            length += 1
        text = f"Static Queues are memory inefficient (cannot be used again when front pointer reaches the end)\nFront index: {front}\nRear index: {rear}\nLength: {length}\nValid: {valid}\nCapacity: 8"

        self.metadata_label.configure(text=text)

class PriorityQueueVisualiser(QueueVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

        # Inherited attributes BELOW
        #self.rear = 3 # Points to the last item in the queue
        #self.front = 0 # Points to the first stored value

        #self.max = 7 # Maximum index in the static queue visualiser
        self.max_nodes = 8

        #self.after_id = None
        #self.after_increment = None
        #self.reset_animation_variables()

        # Override the attribute self.data, since I will use a 2d array to hold the data of the priority queue
        #   Each node will be: [value, priority]
        self.data = [[random.randint(-99, 99), random.randint(1,3)] for _ in range(4)]
        self.data = sorted(self.data, key=lambda x: x[1]) # Sort in ascending order using the second element (priority, with 1 being highest) using a mapping function
        self.data += ["" for _ in range(4)]

    def setGraph(self):
        # Add nodes based on the array
        for index, element in enumerate(self.data):
            self.graph.add_node(index, value=element) # Add nodes with values = element and index = indentifier
        
        # Define fixed positions for the nodes
        scale_factor = 0.825 # Defines how close the nodes are together
        total_width = (len(self.data) - 1) * scale_factor # Gets width of occupied space by the nodes
        center_offset = total_width / 8
        self.pos = {i: (i * scale_factor + center_offset, 0) for i in range(len(self.data))}  # Horizontal positions aligned
        
        # Adjust the labels so that they are the node value and priority and not the indexes
        self.labels = {}
        for index, element in enumerate(self.data):
            # Create a label that combines value and priority, if there is a value
            label = ""
            if element:
                label = f"{element[0]} | {element[1]}"
            self.graph.add_node(index, value=element)
            self.labels[index] = label  # Store the label separately
        
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

        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Priority Queue Visualiser (Circular Array)", font=("Arial", 26, "bold"))
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

        # Meta Data of queue - front index, rear index, length, valid
        self.metadata_frame = ctk.CTkFrame(self)
        self.metadata_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.metadata_frame.propagate(False)
        
        self.metadata_title = ctk.CTkLabel(self.metadata_frame, fg_color="transparent", text="METADATA", font=("Arial Black", 20, "bold"))
        self.metadata_title.pack(pady=10)
        self.metadata_label = ctk.CTkLabel(self.metadata_frame, text="", wraplength=300, font=("Arial", 20))
        self.metadata_label.pack(expand=True)
        self.change_metadata()
        
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
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
        
        # Enqueue
        self.enqueue_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.enqueue_frame.grid(row=1, column=1, pady=10, padx=10)
        self.enqueue_label = ctk.CTkLabel(self.enqueue_frame, text="Enqueue value: (-99 to 99)")
        self.enqueue_label.pack(side="top")

        ctk.CTkLabel(self.enqueue_frame, text="Value:").pack(side="left", padx=3)
        self.enqueue_value_entry = ctk.CTkEntry(self.enqueue_frame, width=50)
        self.enqueue_value_entry.pack(side="left", padx=3)
        ctk.CTkLabel(self.enqueue_frame, text="Priority:").pack(side="left", padx=3)
        self.enqueue_priority_entry = ctk.CTkEntry(self.enqueue_frame, width=50)
        self.enqueue_priority_entry.pack(side="left", padx=3)
        
        self.enqueue_btn = ctk.CTkButton(
            self.enqueue_frame, height=30, width=80, text="Enqueue", 
            command=lambda: self.enqueue(self.enqueue_value_entry.get(), self.enqueue_priority_entry.get())
        )
        self.enqueue_btn.pack(side="left", padx=3)
        
        # Dequeue
        self.dequeue_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Dequeue",
            command=lambda: self.dequeue()
        )
        self.dequeue_btn.grid(row=2, column=1, pady=10, padx=10)

        # Peek
        self.peek_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Peek",
            command=lambda: self.peek()
        )
        self.peek_btn.grid(row=2, column=0, pady=10, padx=10)

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

    def draw_array(self, **kwargs):
        labels = kwargs.get('labels', self.labels)
        colour_list = kwargs.get('colour_array', self.node_colours)
        front = kwargs.get('front', self.front) # Front pointer index
        rear = kwargs.get('rear', self.rear) # Rear pointer index
        temp = kwargs.get('temp', None)

        self.ax.clear()

        # Draw the graph
        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            labels=labels,
            node_size=1300,
            node_color=colour_list,
            node_shape="s",
            edgecolors="black",
            ax=self.ax,
            linewidths=2,
            font_size=9
        )

        # Add index below each node
        for index, (x, y) in self.pos.items():
            self.ax.text(
                x,
                y - 0.7,
                str(index),
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

        # Draw front pointer
        if front is not None:
            x, y = self.pos[front]
            self.ax.annotate(
                "Front",
                xy=(x, y + 0.5),  # Arrow tip position
                xytext=(x, y + 1.5),  # Label position
                ha='center',
                va='center',
                color='blue',
                arrowprops=dict(facecolor='blue', shrink=0.05)
            )

        # Draw rear pointer
        if rear is not None:
            x, y = self.pos[rear]
            if rear == front:
                # If front and rear are the same, place rear below the node
                self.ax.annotate(
                    "Rear",
                    xy=(x, y - 0.75), # Arrow tip position
                    xytext=(x, y - 1.75), # Label position
                    ha='center',
                    va='center',
                    color='red',
                    arrowprops=dict(facecolor='red', shrink=0.05)
                )
            else:
                # Otherwise, place rear above the node
                self.ax.annotate(
                    "Rear",
                    xy=(x, y + 0.5), # Arrow tip position
                    xytext=(x, y + 1.5), # Label position
                    ha='center',
                    va='center',
                    color='red',
                    arrowprops=dict(facecolor='red', shrink=0.05)
                )

        # Draw temp pointer below the nodes
        if temp is not None:
            x, y = self.pos[temp]
            self.ax.annotate(
                "Temp",
                xy=(x, y - 0.75), # Arrow tip position
                xytext=(x, y - 1.75), # Label position
                ha='center',
                va='center',
                color='green',
                arrowprops=dict(facecolor='green', shrink=0.05)
            )

        self.ax.set_xlim(-self.padding, len(self.data)-1 + self.padding)
        self.ax.set_ylim(-1 - self.padding, 1 + self.padding)

        self.canvas.draw()

    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            labels = self.states[self.animation_index][0]
            colour_array = self.states[self.animation_index][1]
            front = self.states[self.animation_index][3]
            rear = self.states[self.animation_index][4]

            try:
                temp = self.states[self.animation_index][5]
                self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear, temp=temp)
            except: # If there is no self.states[self.animation_index][5] then an error arises
                self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear)

            self.change_metadata(front=front, rear=rear, length=(rear-front))
            text = self.states[self.animation_index][2]
            self.output_message(text)
            
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
        front = self.states[self.animation_index][3]
        rear = self.states[self.animation_index][4]
        
        try:
            temp = self.states[self.animation_index][5]
            self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear, temp=temp)
        except: # If there is no self.states[self.animation_index][5] then an error arises
            self.draw_array(labels=labels, colour_array=colour_array, front=front, rear=rear)

        self.change_metadata(front=front, rear=rear, length=(rear-front))
        text = self.states[self.animation_index][2]
        self.output_message(text)

    def generate_array(self, length=0):
        self.reset_animation_variables()
        try:
            if length == "":
                length = random.randint(2,7) # If the entry is left empty, then a random array will be generated
            else:
                length = int(length)
        except ValueError:
            self.output_message("Input invalid. Please enter valid integers")
            return
        
        if length > 8 and length < 0:
            self.output_message("Invalid input. Index not in suitable range")
            return
        
        # Variables for array
        self.rear = length-1  # Length of array that is filled (not index)
        self.front = 0
        if length == 0:
            self.rear += 1

        self.data = [[random.randint(-99, 99), random.randint(1,3)] for _ in range(length)]
        self.data = sorted(self.data, key=lambda x: x[1]) # Sort in ascending order using the second element (priority, with 1 being highest) using a mapping function
        self.data += ["" for _ in range(8-length)]

        self.labels = {}
        for index, element in enumerate(self.data):
            # Create a label that combines value and priority, if there is a value
            label = ""
            if element:
                label = f"{element[0]} | {element[1]}"
            self.labels[index] = label  # Store the label separately

        self.node_colours = ['lightblue' for _ in range(len(self.data))]  # Default colour for all nodes
        
        if length == 0:
            self.output_message("Queue cleared")
        else:
            self.output_message("Queue with random elements of length " + str(length) + " generated")
        self.change_metadata()
        self.draw_array()

    def peek(self):
        if self.isEmpty():
            self.output_message("Queue is empty. No front value to peek")
        else:
            self.reset_animation_variables()
                
            # First add the initial state before the algorithm runs
            self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

            # Simulate the animations
            self.highlight_nodes([self.front])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
            self.state_index += 1

            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front][0]}", self.front, self.rear]
            self.state_index += 1

            self.reset_node_highlights([self.front])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front][0]}\nDeselect the front node", self.front, self.rear]
            self.state_index += 1

            self.is_running = True
            self.set_slider_attributes() # Give data to slider
                
            self.run_animation()

    def dequeue(self):
        if self.isEmpty():
            self.output_message("Queue is empty. No values to remove")
            return

        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        # Simulate the animations
        self.highlight_nodes([self.front])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
        self.state_index += 1

        message = "Deselect previous front node"
        self.update_node_value(self.front, "")
        if not self.isEmpty():
            highlighted_node = self.front
            self.front += 1
            if self.front > self.max:
                self.front = 0
        else:
            message += ". Queue is now empty"
            highlighted_node = self.front
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Remove front value and increment front pointer", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([highlighted_node])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def enqueue(self, entry_value, priority_value):
        if self.isFull():
            self.output_message("Queue is full. Cannot enqueue")
            return
        
        try: # Check input type
            value = int(entry_value)
            priority = int(priority_value)
        except ValueError:
            self.output_message("Invalid input. Please enter an integer.")
            return
        
        if value < -99 or  value > 99: # Check input range
            self.output_message("Invalid input. Value not in suitable range.")
            return
        
        if priority < 1 or priority > 3: # Check input range
            self.output_message("Invalid input. Priority not in suitable range.")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        # Simulate the animations
        if self.isEmpty():
            self.highlight_nodes([self.rear])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get current rear node and check if it is empty", self.front, self.rear]
            self.state_index += 1

            element = f"{value} | {priority}"
            self.update_node_value(self.rear, element)
            self.data[self.rear] = [value, priority]
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Insert the value: {element}, at the rear pointer", self.front, self.rear]
            self.state_index += 1

            self.reset_node_highlights([self.rear])
            message = "Deselect the node"
            if self.rear == self.max:
                message += ". Queue is now full"
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
            self.state_index += 1
        else:
            # If it is not empty, the node has to be inserted in its correct position according to its priority

            temp = self.rear # Use temp to find the right insertion point
            length = (self.rear-self.front) % self.max_nodes

            # Shift elements to make space for new element
            while length >= 0 and self.data[temp][1] > priority:
                # Shift element one position ahead

                # Create new label from current node
                new_label = f"{self.data[temp][0]} | {self.data[temp][1]}"

                # Change label data
                self.update_node_value((temp + 1) % self.max_nodes, new_label)

                # Change actual data
                self.data[(temp + 1) % self.max_nodes] = self.data[temp]

                # Highlight nodes being accessed
                self.highlight_nodes([(temp+1) % self.max_nodes, temp])

                # Change label data
                self.update_node_value(temp, "")
                
                self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Shift element one position ahead", self.front, self.rear, temp]
                self.state_index += 1
                self.reset_node_highlights([(temp+1) % self.max_nodes, temp])

                # Decrement temp pointer
                temp = (temp-1) % self.max_nodes
                self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Deselect nodes and decrement the temp pointer circularly", self.front, self.rear, temp]
                self.state_index += 1

                # Decrement the length
                length -= 1
            
            # Change label data
            self.update_node_value((temp+1) % self.max_nodes, f"{value} | {priority}")

            # Insert the new element
            self.data[(temp + 1) % self.max_nodes] = [value, priority] # Change the actual data

            self.highlight_nodes([(temp+1) % self.max_nodes])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Insert the new element at index [temp + 1], since a node with higher or equal priority has been reached", self.front, self.rear, temp]
            self.state_index += 1

            self.reset_node_highlights([(temp+1) % self.max_nodes])
            self.rear = (self.rear + 1) % self.max_nodes
            temp = None

            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Deselect node, remove temp pointer and increment the rear pointer", self.front, self.rear, temp]
            self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def isFull(self): # When the rear pointer has reached the max number of nodes the static queue goes up to (index 7)
        return (self.rear + 1) % (self.max + 1) == self.front
        
    def change_metadata(self, **kwargs):
        front = kwargs.get('front', self.front)
        rear = kwargs.get('rear', self.rear)
        length = kwargs.get('length', self.rear-self.front)

        if self.data[self.rear]:
            length = 8
        text = f"Nodes: [Value, Priority]\nHighest Priority = 1\nLowest Priority = 3\n\nFront index: {front}\nRear index: {rear}\nLength: {length}\nCapacity: 8"

        self.metadata_label.configure(text=text)

class CircularQueueVisualiser(QueueVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

        # Inherited attributes BELOW
        #self.rear = 3 # Points to the last item in the queue
        #self.front = 0 # Points to the first stored value

        self.max = 8 # Maximum number of nodes in the static queue visualiser

        #self.data = [random.randint(-99, 99) for _ in range(4)] + ["" for _ in range(4)]
        #self.after_id = None
        #self.after_increment = None
        #self.reset_animation_variables()

    def setVis(self):
        # Split the page into: canvas, output, and UI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # self.canvas_frame holds the self.canvas which holds the self.graph (self.graph is in the form of self.canvas.get_tk_widget())
        # Canvas
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Circular Array Queue Visualiser", font=("Arial", 26, "bold"))
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

        # Meta Data of queue - front index, rear index, length, valid
        self.metadata_frame = ctk.CTkFrame(self)
        self.metadata_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.metadata_frame.propagate(False)
        
        self.metadata_title = ctk.CTkLabel(self.metadata_frame, fg_color="transparent", text="METADATA", font=("Arial Black", 20, "bold"))
        self.metadata_title.pack(pady=20)
        self.metadata_label = ctk.CTkLabel(self.metadata_frame, text="", wraplength=300, font=("Arial", 20))
        self.metadata_label.pack(expand=True)
        self.change_metadata()
        
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
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
        
        # Enqueue
        self.enqueue_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.enqueue_frame.grid(row=1, column=1, pady=10, padx=10)
        self.enqueue_label = ctk.CTkLabel(self.enqueue_frame, text="Enqueue value: (-99 to 99)")
        self.enqueue_label.pack(side="top")
        self.enqueue_entry = ctk.CTkEntry(self.enqueue_frame, width=50)
        self.enqueue_entry.pack(side="left")
        
        self.enqueue_btn = ctk.CTkButton(
            self.enqueue_frame, height=30, width=80, text="Enqueue", 
            command=lambda: self.enqueue(self.enqueue_entry.get())
        )
        self.enqueue_btn.pack(side="left", padx=3)
        
        # Dequeue
        self.dequeue_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Dequeue",
            command=lambda: self.dequeue()
        )
        self.dequeue_btn.grid(row=2, column=1, pady=10, padx=10)

        # Peek
        self.peek_btn = ctk.CTkButton(
            self.UI_holder, height=30, width=80, text="Peek",
            command=lambda: self.peek()
        )
        self.peek_btn.grid(row=2, column=0, pady=10, padx=10)

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

    def peek(self):
        if self.isEmpty():
            self.output_message("Queue is empty. No front value to peek")
        else:
            self.reset_animation_variables()
                
            # First add the initial state before the algorithm runs
            self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

            # Simulate the animations
            self.highlight_nodes([self.front])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
            self.state_index += 1

            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front]}", self.front, self.rear]
            self.state_index += 1

            self.reset_node_highlights([self.front])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Front value: {self.data[self.front]}\nDeselect the front node", self.front, self.rear]
            self.state_index += 1

            self.is_running = True
            self.set_slider_attributes() # Give data to slider
                
            self.run_animation()

    def dequeue(self):
        if self.isEmpty():
            self.output_message("Queue is empty. No values to remove")
            return

        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        # Simulate the animations
        self.highlight_nodes([self.front])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get the first node", self.front, self.rear]
        self.state_index += 1

        message = "Deselect previous front node"
        self.update_node_value(self.front, "")
        if not self.isEmpty():
            highlighted_node = self.front
            self.front = (self.front + 1) % self.max
        else:
            message += ". Queue is now empty"
            highlighted_node = self.front
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Remove front value and increment the front pointer circularly", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([highlighted_node])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def enqueue(self, entry_value):
        if self.isFull():
            self.output_message("Queue is full. Cannot enqueue")
            return
        
        try: # Check input type
            value = int(entry_value)
        except ValueError:
            self.output_message("Invalid input. Please enter an integer.")
            return
        
        if value < -99 or  value > 99: # Check input range
            self.output_message("Invalid input. Value not in suitable range.")
            return
        
        self.reset_animation_variables()

        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "", self.front, self.rear]

        self.highlight_nodes([self.rear])
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Get current rear node and check if it is empty", self.front, self.rear]
        self.state_index += 1

        # Simulate the animations
        if not self.isEmpty():
            self.reset_node_highlights([self.rear])
            self.rear = (self.rear + 1) % self.max
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Rear node is not empty so deselect the node and increment the rear pointer circularly", self.front, self.rear]
            self.state_index += 1

            self.highlight_nodes([self.rear])
            self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), "Highlight the empty node at the rear pointer", self.front, self.rear]
            self.state_index += 1

        self.update_node_value(self.rear, value)
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), f"Insert the value: {value}, at the rear pointer", self.front, self.rear]
        self.state_index += 1

        self.reset_node_highlights([self.rear])
        message = "Deselect the node"
        if self.rear == self.max-1:
            message += ". Queue is now full"
        self.states[self.state_index] = [copy.deepcopy(self.labels), copy.deepcopy(self.node_colours), message, self.front, self.rear]
        self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()


    def isFull(self): # When the rear pointer has reached the max number of nodes the static queue goes up to (index 7)
        return (self.rear + 1) % self.max == self.front
        
    def change_metadata(self, **kwargs):
        front = kwargs.get('front', self.front)
        rear = kwargs.get('rear', self.rear)
        length = kwargs.get('length', (self.rear-self.front) % self.max)
        if not self.isEmpty():
            length += 1
        text = f"Front index: {front}\nRear index: {rear}\nLength: {length}\nCapacity: 8"

        self.metadata_label.configure(text=text)

def main(master, window):
    window.geometry("1280x1020")
    window.minsize(1280, 1020)

    # Create tabview widget
    tabview = ctk.CTkTabview(master)
    tabview.pack(padx=20, pady=20, fill="both", expand=True)

    # Create tabs
    tab1 = tabview.add("Queue")
    tab2 = tabview.add("Circular Queue")
    tab3 = tabview.add("Priority Queue")
    
    vis1 = QueueVisualiser(tab1)
    vis1.pack(fill="both", expand=True)
    vis1.setGraph()
    vis1.setVis()

    vis2 = CircularQueueVisualiser(tab2)
    vis2.pack(fill="both", expand=True)
    vis2.setGraph()
    vis2.setVis()

    vis3 = PriorityQueueVisualiser(tab3)
    vis3.pack(fill="both", expand=True)
    vis3.setGraph()
    vis3.setVis()