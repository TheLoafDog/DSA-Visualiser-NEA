# generate_new_list: Lines 451 - 474
# search:            Lines 476 - 531
# insert:            Lines 533 - 646
# remove:            Lines 648 - 762


import copy
import customtkinter as ctk
import tkinter as tk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Node:
    def __init__(self, value, node_colour='lightblue', pointer_colour='black'):
        self.value = value
        self.next = None # Points to the next node (this is an actual object)
        self.colour = node_colour
        self.pointer_colour = pointer_colour
        # Would have an index attribute but I will get the index using id(object) where it returns the memory address the object is stored at

# To draw list, I need the following attributes of each node:
#   Their positions:    pos
#   Their colours:      colour
#   Their labels:       value
# However, each node is identified using their identifiers which would be the memory address (what the visualised pointer is pointing towards)
# These values are not stored in a static array, so I have to go through the linked list each time to make these attributes

# There are two pointers:
#   visualised pointer (node_id): what the pointer in the visualiser is shown to point at (this would be the memory adress the next node is stored at)
#   actual pointer (self.next): what the pointer in the actual linked list (back end) is pointing at (this would be the next actual node object in the linked list)

class LinkedListVisualiser(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(master=root, fg_color="gray")
        self.root = root
        
        self.graph = nx.DiGraph()

        # Variables for linked list
        self.temp = None # For when removing a node, I need to store the final result and apply it if another process is called
        self.head = None
        
        # Make the default randomised data on start up
        self.generate_data()

        # Variables for animation
        self.after_id = None # Stores the next step in the animation in case it needs to be cancelled
        self.after_increment = None
        self.reset_animation_variables()
        
        # Establish graph
        self.setGraph()
        
        # Next setup the visualiser and other UI components

        # Split the page into: canvas, output, and UI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.setMainPanel() # Main panel that has the visualiser and playback functionality
        self.setLogPanel() # Log that outputs messages in each step or to show errors
        self.setInteractivePanel() # UI that lets the user interact with the visualiser

    def generate_data(self, length=4):
        self.temp = None
        self.head = None
        self.graph.clear() # Clear all the existing nodes and edges of the networkx graph
        for _ in range(0, length):
            new_node = Node(random.randint(1,99))
            if length == 0: # When the user wants to create a random linked list of custom length another function is called before hand to handle input errors by the user
                self.head = None
            else:    
                if self.head is None:
                    self.head = new_node
                    self.graph.add_node(id(new_node))
                else:
                    current = self.head
                    while current.next: # Get to the end of the linked list
                        current = current.next
                    current.next = new_node # Create new node object
                    self.graph.add_node(id(new_node)) # Create new node in networkx WITH identifier = memory address of node object AND (REMOVED, because it is not needed since this is already recorded inside the node class ==>) value = randomly generated value stored (actual value)

                    # Add the arrows to show the connection of the nodes as pointers
                    self.graph.add_edge(id(current), id(new_node), label=id(new_node)) # (arg1, arg2, arg3) Adds edge from node (arg1) to node (arg2) with a label (arg3)

    def get_list(self):
        linked_list = []

        current=self.head
        while current:
            linked_list.append(current.value)

            current = current.next

    def get_node_positions(self): # pos must be in the form of a dictionary to fit the networkx drawing format (for node positions)
        pos = {} # Each key = node identifier AND data = (x,y) positions on graph
        x_offset = 0
        node_count = 0

        current = self.head
        while current:
            node_id = id(current)  # Use the object's memory address as the node identifier
            pos[node_id] = (x_offset, 0)
            x_offset += 1
            node_count += 1

            current = current.next

        return node_count, pos
    
    def get_node_colours(self): # node_colours must be in the form of an list to fit the networkx drawing format (for colours)
        node_colours = []
        
        current = self.head
        while current:
            node_colours.append(current.colour)
            current = current.next

        return node_colours
    
    def get_labels(self): # labels must be in the form of an dictionary to fit the networkx drawing format (for labels of the nodes)
        labels = {}

        current = self.head
        while current:
            node_id = id(current)
            labels[node_id] = current.value

            current = current.next

        return labels
    
    def get_pointer_colours(self):
        pointer_colours = []

        if self.head:
            current = self.head
            while current.next:
                pointer_colours.append(current.pointer_colour)

                current = current.next

        return pointer_colours

    def set_slider_attributes(self):
        self.playback_slider.set(0)
        self.playback_slider.configure(from_=0, to=len(self.states)-1, number_of_steps=len(self.states)-1)
        # Reactivate slider and other buttons
        self.playback_slider.configure(state="normal")
        self.stop_button.configure(state="normal", text="| |", command=self.toggle_pause)
        for button in self.edit_buttons:
            button.configure(state="normal")

    def adjust_canvas(self):
        # Pause the sort
        self.is_running = False
        self.stop_button.configure(text="▷")
        # In case the animation finished and the command changes, reset command for stop button
        self.stop_button.configure(command=self.toggle_pause)
            
        # Next set the sort visualiser in relation to the slider value
        labels = self.states[self.animation_index][0]
        node_colours = self.states[self.animation_index][1]
        pointer_colours = self.states[self.animation_index][2]
        positions = self.states[self.animation_index][3]
        text = self.states[self.animation_index][4]
        self.output_message(text)
        if len(self.states[self.animation_index]) > 5: # For remove and insert functions have varying nodes
            head_address = self.states[self.animation_index][5]
            tail_address = self.states[self.animation_index][6]
            self.draw_list(labels=labels, node_colours=node_colours, pointer_colours=pointer_colours, positions=self.states[self.animation_index][3], head_address=head_address, tail_address=tail_address)
        else:
            self.draw_list(labels=labels, node_colours=node_colours, pointer_colours=pointer_colours, positions=self.states[self.animation_index][3])

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
    
    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            labels = self.states[self.animation_index][0]
            node_colours = self.states[self.animation_index][1]
            pointer_colours = self.states[self.animation_index][2]
            if len(self.states[self.animation_index]) > 5: # For remove and insert functions have varying nodes
                head_address = self.states[self.animation_index][5]
                tail_address = self.states[self.animation_index][6]
                self.draw_list(labels=labels, node_colours=node_colours, pointer_colours=pointer_colours, positions=self.states[self.animation_index][3], head_address=head_address, tail_address=tail_address)
            else:
                self.draw_list(labels=labels, node_colours=node_colours, pointer_colours=pointer_colours, positions=self.states[self.animation_index][3])

            message = self.states[self.animation_index][4]
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


    def draw_list(self, **kwargs):
        if kwargs:
            labels = kwargs['labels']
            node_colours = kwargs['node_colours']
            pointer_colours = kwargs['pointer_colours']
            node_count, pos = kwargs['positions']
        else:
            labels = self.get_labels()
            node_colours = self.get_node_colours()
            pointer_colours = self.get_pointer_colours()
            node_count, pos = self.get_node_positions()

        if len(kwargs) > 4: # For insert and remove
            head_address = kwargs['head_address']
            tail_address = kwargs['tail_address']
        else:
            if self.head:
                head_address = id(self.head) # For head label
                tail_node = self.head # For tail label
                while tail_node.next:
                    tail_node = tail_node.next
                tail_address = id(tail_node)
            else: # Else no self.head, list is empty
                head_address = None

        self.ax.clear()
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            labels=labels,  # Custom labels due to nature of nodes
            node_size=700,  # Adjusted the node size so that they are touching each other
            node_color=node_colours,
            ax=self.ax,
            arrows=True,
            arrowstyle="->",
            arrowsize=20,
            edge_color=pointer_colours,
        )

        # Add edge labels with a border
        pointer_labels = {}
        for u, v, data in self.graph.edges(data=True):
            pointer_labels[(u, v)] = "..." + str(data["label"])[9:]
        for index, ((u, v), label) in enumerate(pointer_labels.items()):
            x, y = pos[u][0] * 0.6 + pos[v][0] * 0.4 + 0.03, 0  # Position of the label
            self.ax.text(
                x,
                y,
                label,
                fontsize=9,
                color=pointer_colours[index],
                ha="center",
                va="center",
                bbox=dict(
                    boxstyle="round,pad=0.3",  # Rounded border
                    facecolor="white",  # Background color
                    edgecolor=pointer_colours[index],  # Border color
                    linewidth=1,  # Border width
                ),
            )

        # Add head and tail labels
        if head_address and tail_address:  # Ensure the list is not empty
            # Add head label
            head_x, head_y = pos[head_address]
            self.ax.text(
                head_x,
                head_y - 0.4,  # Position below the head node
                f"Head\n{head_address}",  # Label with memory address
                fontsize=10,
                color="blue",
                ha="center",
                va="top",
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor="white",
                    edgecolor="blue",
                    linewidth=1,
                ),
            )

            # Add tail label (only if it's different from the head)
            if head_address != tail_address:
                tail_x, tail_y = pos[tail_address]
                self.ax.text(
                    tail_x,
                    tail_y - 0.4,  # Position below the tail node
                    f"Tail\n{tail_address}",  # Label with memory address
                    fontsize=10,
                    color="red",
                    ha="center",
                    va="top",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="white",
                        edgecolor="red",
                        linewidth=1,
                    ),
                )
            else:
                # If head and tail are the same, add tail label below the head label
                self.ax.text(
                    head_x,
                    head_y + 1,  # Position above the node
                    f"Tail\n{tail_address}",  # Label with memory address
                    fontsize=10,
                    color="red",
                    ha="center",
                    va="top",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor="white",
                        edgecolor="red",
                        linewidth=1,
                    ),
                )

        self.padding = 0.2
        self.ax.set_xlim(-self.padding, node_count - 1 + self.padding)  # X-axis for horizontal layout
        self.ax.set_ylim(-1 - self.padding, 1 + self.padding)  # Y-axis for fixed vertical position

        self.canvas.draw()
    
    def toggle_pause(self):        
        if not self.is_running:
            self.is_running = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.is_running = False
            self.stop_button.configure(text="▷")
        
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
            node_colours = self.states[value][1]
            pointer_colours = self.states[value][2]
            self.draw_list(labels=labels, node_colours=node_colours, pointer_colours=pointer_colours, positions=self.states[value][3])
            self.output_message(self.states[value][4])
            
            self.animation_index = value
            
            self.last_slider_value = value
        
    def increment_slider(self):
        self.playback_slider.set(self.playback_slider.get()+1)
        self.animation_index += 1
        
    def reactivate_slider(self):
        self.playback_slider.configure(state="normal")
        # This is separate to the other buttons due to having a different master

    def output_message(self, text):
        self.message_label.configure(text=text)

    def highlight_node(self, node, colour='red'):
        node.colour = colour

    def unhighlight_node(self, node):
        self.highlight_node(node, colour='lightblue')

    def remove_node(self, node):
        self.highlight_node(node, colour='white')

    def highlight_pointer(self, node):
        node.pointer_colour = 'red'

    def unhighlight_pointer(self, node):
        node.pointer_colour = 'black'

    def remove_pointer(self, node):
        node.pointer_colour = 'white'

    def change_value(self, node, value):
        node.value = value

    # UI function methods underneath
    
    def generate_new_list(self, length):
        self.reset_animation_variables()
        try:
            if length == "":
                length = 4 # If the entry is left empty, then a random list of length 4 will be generated
            else:
                length = int(length)
        except ValueError:
            self.output_message("Input invalid. Please enter valid integers.")

        if length > 8 or length < 0:
            self.output_message("Invalid input. Index not in suitable range.")
            return

        # Call the function that generates data
        self.generate_data(length=length)

        # Output a suitable message to the user
        if length == 0:
            self.output_message("List cleared.")
        else:
            self.output_message("List with random elements of length " + str(length) + " generated.")

        self.draw_list()

    def search(self, entry_value):
        self.after_remove()
        # Check if the array is full
        if self.head == None:
            self.output_message("Linked list is empty.")
            return
        
        try:
            value = int(entry_value)  # Convert entry to integer
        except ValueError:
            self.output_message("Invalid input. Please enter valid integers.")
        
        self.reset_animation_variables()
        
        # First add the initial state before the algorithm runs
        self.states[0] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), ""]
        
        # Simulate the animation first
        current = self.head
        found = False
        while current and not found:

            if current.value == value:
                found = True
                self.highlight_node(current, colour='green')
                text="MATCH!\nValue found at memory register: " + str(id(current))
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text]
                
                self.unhighlight_node(current)
            else:
                self.highlight_node(current) # Highlight current node that is being compared 'red'
                text = "Comparing searched value with value in memory register: " + str(id(current)) + "\n" + str(current.value) + " = " + str(value) + "?"
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text]
                self.state_index += 1

                self.unhighlight_node(current)

                if current.next:
                    self.highlight_pointer(current)
                    text = "NO MATCH!\nGoing to next value using the current node's pointer to find the memory location the next node is stored at: " + str(id(current.next))
                    self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text]
                    self.state_index += 1

                    self.unhighlight_pointer(current)

                current = current.next
        
        if not found:
            text = "NO MATCHES FOR " + str(value) + "!\nValue does not exist in this linked list"
            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text]


        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def insert(self, entry_value, location="tail"):
        self.after_remove()
        if len(self.graph.nodes) == 8: # Check if the list has reached the max number of nodes
            self.output_message("Maximum number of nodes (8) has been reached.")
            return
        
        try:
            value = int(entry_value)  # Convert entry to integer
        except ValueError:
            self.output_message("Invalid input. Please enter valid integers.")
            return
        
        self.reset_animation_variables()
    
        # Simulate the animation first

        new_node = Node("", node_colour='white', pointer_colour='white') # Should not be visible at first
        new_node_id = id(new_node)

        self.graph.add_node(new_node_id)

        if self.head: # Get the initial head and tail of the list before the method is carried out
            tail = self.head
            while tail.next:
                tail = tail.next
            head_address = id(self.head)
            tail_address = id(tail)
        else:
            head_address = None
            tail_address = None

        if location == "head": # Inserting value at the head
            # Check if the linked list is not empty
            if self.head:
                new_node.next = self.head
                self.graph.add_edge(new_node_id, head_address, label=head_address) # Add edge from new_node to previous head
                edges = list(self.graph.edges(data=True))
                edges = [edges[-1]] + edges[:-1] # Order matters, so insert new edge at the front

            self.head = new_node
            # Store initial state before any changes
            self.states[0] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "", head_address, tail_address]
            # Reorder the list so that the newest added value is at the front
            # Convert NetworkX graph nodes to lists
            nodes = list(self.graph.nodes)

            # Move last node and edge to the front
            nodes = [nodes[-1]] + nodes[:-1]

            # Rebuild the graph in the new order
            self.graph.clear()
            self.graph.add_nodes_from(nodes)
            if head_address:
                self.graph.add_edges_from(edges)

            self.highlight_node(new_node) # Make the node visible
            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add new empty node.", head_address, tail_address]
            self.state_index += 1

            new_node.value = value # Add value to the node
            self.unhighlight_node(new_node)

            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add value into empty node.", head_address, tail_address]
            self.state_index += 1

            if head_address:
                self.highlight_pointer(new_node) # Make the pointer visible
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add pointer to empty node.", head_address, tail_address]
                self.state_index += 1
                self.unhighlight_pointer(new_node) # Establish the pointer

            if tail_address:
                # In the next state, the head label moves to the new head
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), str(value) + " has been added to the head of the linked list.", new_node_id, tail_address]
                self.state_index += 1
            else:
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), str(value) + " has been added to the head and tail of the linked list since it was originally empty.", new_node_id, new_node_id]
                self.state_index += 1

        else: #### Add value at the tail ####
            if self.head:
                tail.next = new_node # Add the new node at the end of the list

                tail.pointer_colour = 'white'
                self.graph.add_edge(tail_address, new_node_id, label=new_node_id)
            else:
                self.head = new_node
            
            # Store initial state before any changes
            self.states[0] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "", head_address, tail_address]

            self.highlight_node(new_node) # Make the node visible
            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add new empty node.", id(self.head), tail_address]
            self.state_index += 1

            new_node.value = value # Add value to the node
            self.unhighlight_node(new_node)

            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add value into empty node.", id(self.head), tail_address]
            self.state_index += 1

            if tail_address:
                self.highlight_pointer(tail) # Make the pointer visible
                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "Add pointer to empty node.", id(self.head), tail_address]
                self.state_index += 1
                self.unhighlight_pointer(tail) # Establish the pointer
            
            # In the next state, the tail label moves to the new tail
            self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), str(value) + " has been added to the tail of the linked list.", id(self.head), new_node_id]
            self.state_index += 1

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        self.run_animation()

    def remove(self, location="tail"): # Inconsistency problem again, visually pretend the node disappears, then get rid of it at the end properly
        self.after_remove()
        if self.head:
            self.reset_animation_variables()

            if self.head:
                tail = self.head
                while tail.next:
                    penultimate = tail
                    tail = tail.next
                head_address = id(self.head)
                tail_address = id(tail)
            else:
                head_address = None
                tail_address = None

            # Store initial state before any changes
            self.states[0] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), "", head_address, tail_address]

            # Simulate the animation first

            nodes = list(self.graph.nodes) # Convert the nodes into a list
            edges = list(self.graph.edges(data=True)) # Convert the edges into a list

            if location == "head":
                self.highlight_node(self.head) # Get the first node (head) and highlight it
                text = "Get current head of the linked list."

                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                self.state_index += 1 # Store and increment the state

                if edges:
                    self.highlight_pointer(self.head) # If there are edges (when there is more than one node) get the pointer and highlight it
                    text = "Get the current head's pointer."

                    self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                    self.state_index += 1

                    self.remove_pointer(self.head) # Make the pointer invisilble
                    del edges[0]
                    extra = " and its pointer."

                self.remove_node(self.head) # Make the head node invisible
                del nodes[0] # Remove the first node (head) from the list
                text="Delete " + str(self.head.value)
                if nodes: # Check if it was the last node in the list
                    text += extra
                    text += "\n" + str(self.head.next.value) + " is the new head of the linked list."
                    head_address = id(self.head.next)
                else:
                    text += ".\nLinked list is now empty."
                    head_address = None

                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                self.state_index += 1

                if head_address: # Check if it was the last node in the list
                    self.head = self.head.next
                else:
                    self.head = None
            else: #### Remove the tail ####
                self.highlight_node(tail)
                text = "Get current tail of the linked list."

                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                self.state_index += 1

                if edges:
                    self.highlight_pointer(penultimate)
                    text = "Get pointer that points to tail."

                    self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                    self.state_index += 1

                    self.remove_pointer(penultimate)
                    del edges[-1]
                    extra = " and the pointer that points to it."

                self.remove_node(tail)
                del nodes[-1]

                text="Delete " + str(tail.value)
                if nodes:
                    text += extra
                    text += "\n" + str(penultimate.value) + " is the new head of the linked list."
                    tail_address = id(penultimate)
                else:
                    text += ".\nLinked list is now empty."
                    tail_address = None

                self.states[self.state_index] = [copy.deepcopy(self.get_labels()), copy.deepcopy(self.get_node_colours()), copy.deepcopy(self.get_pointer_colours()), copy.deepcopy(self.get_node_positions()), text, head_address, tail_address]
                self.state_index += 1

                if tail_address: # Check whether the list is empty
                    penultimate.next = None
                else:
                    self.head = None

            self.temp = [nodes, edges]

            self.is_running = True
            self.set_slider_attributes() # Give data to slider

            self.run_animation()
        else:
            self.output_message("Linked list is empty")

        
    def after_remove(self):
        if self.temp: # stores the following in a list [[nodes], [edges]]
            self.graph.clear()
            self.graph.add_nodes_from(self.temp[0])
            self.graph.add_edges_from(self.temp[1])

            self.temp = None

    def setMainPanel(self):
        # self.canvas_frame holds the self.canvas which holds the self.graph (self.graph is in the form of self.canvas.get_tk_widget())
        # Canvas
        self.canvas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        
        self.canvas_title = ctk.CTkLabel(master=self.canvas_frame, text="Linked List Visualiser", font=("Arial", 26, "bold"))
        self.canvas_title.pack(pady=20)
        
        self.canvas.get_tk_widget().pack(expand=True)

        self.playback_holder = ctk.CTkFrame(master=self.canvas_frame, fg_color="transparent", border_width=0)
        self.playback_holder.pack(pady=5, side='left', expand=True)
        self.playback_slider = ctk.CTkSlider(master=self.playback_holder, height=20, border_color="black", command=self.on_slider_move)
        self.playback_slider.pack(pady=10, padx=10, fill='x')
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

    def setLogPanel(self):
        # Log - to show messages in each step
        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.message_frame.propagate(False)
        
        self.message_title = ctk.CTkLabel(self.message_frame, fg_color="transparent", text="LOG", font=("Arial Black", 20, "bold"))
        self.message_title.pack(pady=20)
        self.message_label = ctk.CTkLabel(self.message_frame, text="", wraplength=150, font=("Arial", 20))
        self.message_label.pack(expand=True)

    def setInteractivePanel(self):
        # This will be the frame that holds all the UI
        self.UI_holder = ctk.CTkFrame(self)
        self.UI_holder.pack_propagate(False)
        self.UI_holder.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.UI_holder.columnconfigure(0, weight=1)
        self.UI_holder.columnconfigure(1, weight=1)

        self.UI_holder.rowconfigure(0, weight=1)
        self.UI_holder.rowconfigure(1, weight=1)
        self.UI_holder.rowconfigure(2, weight=1)
        
        # Speed control
        self.speed_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.speed_frame.grid(row=0, column=1, pady=20, padx=10)
        self.speed_var = ctk.DoubleVar(value=100)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self.speed_frame, text="Speed (ms)")
        self.speed_label.pack(side="left", padx=10)

        self.speed_slider = ctk.CTkSlider(master=self.speed_frame, from_=10, to=1000, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, fill="x", expand=True)
        
        # Insertion
        self.insert_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.insert_frame.grid(row=1, column=1, pady=10, padx=10)
        self.insert_label = ctk.CTkLabel(self.insert_frame, text="Insert value:")
        self.insert_label.pack(side="top")
        self.insert_entry = ctk.CTkEntry(self.insert_frame, width=50)
        self.insert_entry.pack(side="left", padx=3)
        
        self.insert_head_btn = ctk.CTkButton(
            self.insert_frame, height = 30, width = 80, text="Insert at head",
            command=lambda: self.insert(self.insert_entry.get(), "head")
        )
        self.insert_head_btn.pack(side="left", padx=3)
        
        self.insert_tail_btn = ctk.CTkButton(
            self.insert_frame, height = 30, width = 80, text="Insert at tail",
            command=lambda: self.insert(self.insert_entry.get())
        )
        self.insert_tail_btn.pack(side="left", padx=3)

        # Deletion
        self.remove_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.remove_frame.grid(row=2, column=1, pady=10, padx=10)
        self.remove_label = ctk.CTkLabel(self.remove_frame, text="Remove value")
        self.remove_label.pack(side="top")
        
        self.remove_head_btn = ctk.CTkButton(
            self.remove_frame, height = 30, width = 80, text="Head",
            command=lambda: self.remove(location="head")
        )
        self.remove_head_btn.pack(side="left", padx=3)

        self.remove_tail_btn = ctk.CTkButton(
            self.remove_frame, height = 30, width = 80, text="Tail",
            command=lambda: self.remove()
        )
        self.remove_tail_btn.pack(side="left", padx=3)

        # Search
        self.search_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.search_frame.grid(row=2, column=0, pady=10, padx=10)
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search node value: ")
        self.search_label.pack(side="top")
        self.search_entry = ctk.CTkEntry(self.search_frame, width=50)
        self.search_entry.pack(side="left", padx=3, expand=True)
        
        self.search_btn = ctk.CTkButton(
            self.search_frame, height = 30, width = 80, text="Search",
            command=lambda: self.search(self.search_entry.get())
        )
        self.search_btn.pack(side="right", padx=3)
        
        # Clear list
        self.clear_list_btn = ctk.CTkButton(
            self.UI_holder, height = 30, width = 80, text="Clear list",
            command = lambda: self.generate_new_list(length=0)
        )
        self.clear_list_btn.grid(row=1, column=0)
        
        # Generate random list
        self.generate_list_frame = ctk.CTkFrame(self.UI_holder, border_width=0)
        self.generate_list_frame.grid(row=0, column=0, pady=10, padx=10)
        self.generate_list_label = ctk.CTkLabel(self.generate_list_frame, text="Generate list of length: (no entry = length of 4)")
        self.generate_list_label.pack(side="top")
        self.generate_list_entry = ctk.CTkEntry(self.generate_list_frame, width=50)
        self.generate_list_entry.pack(side="left", expand=True)
        
        self.generate_list_btn = ctk.CTkButton(
            self.generate_list_frame, height = 30, width = 100, text="Generate Random",
            command = lambda: self.generate_new_list(length=self.generate_list_entry.get())
        )
        self.generate_list_btn.pack(side="right", expand=True)

    def setGraph(self):
        # Create GUI components
        self.canvas_frame = ctk.CTkFrame(self)
        
        # Plot canvas for the graph
        self.figure, self.ax = plt.subplots(figsize=(12, 2))
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)

        self.draw_list()

def test():
    app = ctk.CTk()
    app.geometry("1280x820")
    app.minsize(1280, 820)
    
    vis = LinkedListVisualiser(app)
    vis.pack(fill="both", expand=True)
    
    app.mainloop()


#test()

def main(root, window):
    vis = LinkedListVisualiser(root)
    vis.pack(fill="both", expand=True)

    window.geometry("1280x920")
    window.minsize(1280, 920)
