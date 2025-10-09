# breadth-first-search (queue):     Lines 484 - 548
# depth-first-search (recursive):   Lines 551 - 616

# add_node:     Lines 393 - 420
# delete_node:  Lines 422 - 446
# add_edge:     Lines 448 - 467

import customtkinter as ctk
import tkinter as tk # For boolean variable
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphVisualiser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="gray")
        self.master = master
        
        self.graph = nx.Graph()

        # Variables for drag-and-drop
        self.pos = None
        self.dragging_node = None
        self.node_colours = {i: "" for i in range(10)}
        self.found = False
    
    def connect_mouse_events(self):
        # Connect mouse events
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_drag)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        
    def setVis(self):
        # Split the page into: canvas, output, and UI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Create GUI components
        self.canvas_frame = ctk.CTkFrame(self, fg_color="grey", border_width=0)
        self.canvas_frame.grid(row=0, column=0, rowspan=3, pady=10, padx=10)

        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=10, padx=10)

        self.controls_frame.columnconfigure(0, weight=1)
        self.controls_frame.columnconfigure(1, weight=1)
        self.controls_frame.columnconfigure(2, weight=1)

        self.controls_frame.rowconfigure(0, weight=1)
        self.controls_frame.rowconfigure(1, weight=1)
        self.controls_frame.rowconfigure(2, weight=1)
        self.controls_frame.rowconfigure(3, weight=1)
        self.controls_frame.rowconfigure(4, weight=1)
        self.controls_frame.rowconfigure(5, weight=1)
        self.controls_frame.rowconfigure(6, weight=1)
        self.controls_frame.rowconfigure(7, weight=1)
        
        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.grid(row=2, column=1, rowspan=2, sticky="nsew", pady=10, padx=10)
        
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)

        # Control panel UI - labels, buttons and entry fields

        # Graph Generation
        self.random_graph_button = ctk.CTkButton(self.controls_frame, text="Generate Random Graph", command=self.generate_random_graph)
        self.random_graph_button.grid(row=0, column=0)

        self.clear_button = ctk.CTkButton(self.controls_frame, text="Clear Graph", command=self.clear_graph)
        self.clear_button.grid(row=0, column=2)

        # Adding nodes
        ctk.CTkLabel(self.controls_frame, text="Node to Add: (0-9)").grid(row=1, column=0)
        self.add_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.add_node_entry.grid(row=1, column=1, sticky="w")

        self.add_node_button = ctk.CTkButton(self.controls_frame, text="Add Node", command=lambda: self.add_node(self.add_node_entry.get()))
        self.add_node_button.grid(row=1, column=1, columnspan=2)

        # Deleting nodes
        ctk.CTkLabel(self.controls_frame, text="Node to Delete: (0-9)").grid(row=2, column=0)
        self.delete_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.delete_node_entry.grid(row=2, column=1, sticky="w")

        self.delete_node_button = ctk.CTkButton(self.controls_frame, text="Delete Node", command=lambda: self.delete_node(self.delete_node_entry.get()))
        self.delete_node_button.grid(row=2, column=1, columnspan=2)

        # Adding edges
        ctk.CTkLabel(self.controls_frame, text="Edge: From").grid(row=3, column=0)
        self.edge_from_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.edge_from_entry.grid(row=3, column=0, sticky="e")

        ctk.CTkLabel(self.controls_frame, text="To").grid(row=3, column=1)
        self.edge_to_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.edge_to_entry.grid(row=3, column=1, sticky="e")

        self.add_edge_button = ctk.CTkButton(self.controls_frame, text="Add Edge", command=lambda: self.add_edge(self.edge_from_entry.get(), self.edge_to_entry.get()))
        self.add_edge_button.grid(row=3, column=2)

        # Entry field for starting node (for BFS and DFS)
        ctk.CTkLabel(self.controls_frame, text="Start Node:").grid(row=4, column=0)
        self.start_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.start_node_entry.grid(row=4, column=0, sticky="e")

        ctk.CTkLabel(self.controls_frame, text="Find:").grid(row=4, column=1)
        self.find_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.find_node_entry.grid(row=4, column=1, sticky="e")

        # Traversals (searches)
        self.bfs_button = ctk.CTkButton(self.controls_frame, width=50, text="BFS", command=lambda: self.visualize_bfs(self.start_node_entry.get(), self.find_node_entry.get()))
        self.bfs_button.grid(row=4, column=2, sticky="w", padx=30)

        self.dfs_button = ctk.CTkButton(self.controls_frame, width=50, text="DFS", command=lambda: self.visualize_dfs(self.start_node_entry.get(), self.find_node_entry.get()))
        self.dfs_button.grid(row=4, column=2, sticky="e", padx=30)

        # Checkbox for weighted/unweighted graph
        self.is_weighted = tk.BooleanVar(value=False)
        self.weighted_checkbox = ctk.CTkCheckBox(self.controls_frame, text="Weighted Graph", variable=self.is_weighted, command=self.toggle_weights)
        self.weighted_checkbox.grid(row=5, column=2)

        self.get_weight = ctk.CTkButton(self.controls_frame, state="disabled", text="Total Weight", command=self.get_total_weight)
        self.get_weight.grid(row=5, column=1)

        # Speed control
        self.speed_frame = ctk.CTkFrame(self.controls_frame, border_width=0)
        self.speed_frame.grid(row=6, column=0, columnspan=4, padx=10)
        self.speed_var = ctk.DoubleVar(value=700)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self.speed_frame, text="Speed (ms)")
        self.speed_label.pack(side="left", padx=10)

        self.speed_slider = ctk.CTkSlider(master=self.speed_frame, from_=1000, to=10, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, fill="x", expand=True)
    
        # Playback functionality
        self.playback_holder = ctk.CTkFrame(self.controls_frame, fg_color="transparent", border_width=0)
        self.playback_holder.grid(row=7, column=0, columnspan=4)
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


        # Plot canvas for the graph
        ctk.CTkLabel(self.canvas_frame, text="Graph Visualiser", font=("Arial", 26, "bold"), fg_color="transparent").pack(pady=20)
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        self.canvas.get_tk_widget().pack()
        
        
        # This is for the log where the messages will be outputted
        self.message_title = ctk.CTkLabel(self.message_frame, fg_color="transparent", text="LOG", font=("Arial Black", 24, "bold"))
        self.message_title.pack(pady=20)
        self.message_label = ctk.CTkLabel(self.message_frame, text="", font=("Arial",20), wraplength=400)
        self.message_label.pack(expand=True)
        
        
        # This is to output the list after a traversal is completed
        self.output_title = ctk.CTkLabel(self.output_frame, fg_color="transparent", text="OUTPUT", font=("Arial Black", 18))
        self.output_title.pack(pady=10)
        self.output_label = ctk.CTkLabel(self.output_frame, text="[ ]", font=("Arial",20))
        self.output_label.pack(pady=10)

    def draw_graph(self, **kwargs):
        # Custom colours for different steps in the animation
        node_colours = kwargs.get('node_colours', self.node_colours)

        color_map = [node_colours.get(node) for node in self.graph.nodes()]

        self.ax.clear()

        # Draw graph nodes
        nx.draw(
            self.graph,
            self.pos,
            ax=self.ax,
            with_labels=True,
            node_color=color_map,
            node_size=500,
            font_size=12,
            font_weight='bold'
            )
        
        # Draw weights on edges if graph is weighted
        try:
            if self.is_weighted.get():
                edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            
                nx.draw_networkx_edge_labels(
                    self.graph,
                    self.pos,
                    edge_labels=edge_labels,
                    ax=self.ax)
        except:
            pass

        self.canvas.draw()

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

    def increment_slider(self):
        self.playback_slider.set(self.playback_slider.get()+1)
        self.animation_index += 1

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
        node_colours = self.states[self.animation_index][0]
        self.output_message(self.states[self.animation_index][1])
        self.change_output(self.states[self.animation_index][2])
        self.draw_graph(node_colours=node_colours)


    def run_animation(self):
        if not self.is_running:
            return

        if self.animation_index < len(self.states): # len(self.states) is the same as self.total_steps
            node_colours = self.states[self.animation_index][0]
            self.draw_graph(node_colours=node_colours)
            self.output_message(self.states[self.animation_index][1])
            self.change_output(self.states[self.animation_index][2])
            
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

    def cancel_animation(self): # Cancel any scheduled events by using after_id
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_cancel(self.after_increment)
            self.after_id = None  # Reset after_id since it is no longer active
            self.after_increment = None

            self.draw_graph()

    def on_slider_move(self, value):
        value=int(value)
        if self.last_slider_value != value:
            self.cancel_animation()

            # Pause the traversal
            self.is_running = False
            self.stop_button.configure(text="▷")
            # In case the animation finished and the command changes, reset command for stop button
            self.stop_button.configure(command=self.toggle_pause)
            
            node_colours = self.states[value][0]
            self.draw_graph(node_colours=node_colours)
            self.output_message(self.states[value][1])
            self.change_output(self.states[value][2])
            
            self.animation_index = value
            
            self.last_slider_value = value

    def toggle_pause(self):        
        if not self.is_running:
            self.is_running = True
            self.stop_button.configure(text="| |")
            self.run_animation()
        else:
            self.is_running = False
            self.stop_button.configure(text="▷")

    def reset_animation_variables(self):
        # Variables for animation
        self.is_running = False # To check whether the animation is running or paused
        self.after_id = None  # Store after_id to cancel scheduled events
        self.states = {} # Hash table to hold the data for each step in the animation
        self.state_index = 1 # Index for storing the states after each step in the simulation
        self.animation_index = 0 # Index for outputting during the animation
        
    def get_total_weight(self):
        self.toggle_pause()

        total = 0
        for (u, v) in self.graph.edges():
            total += self.graph[u][v]['weight']
        
        self.output_message("Total weight of the graph: " + str(total))

    def generate_random_graph(self, num_nodes=None):
        if num_nodes == None:
            num_nodes = random.randint(5,8)

        self.cancel_animation()

        self.graph.clear()  # Clear any previous graph

        # Generate a random graph with a probability for edge creation
        self.graph = nx.gnp_random_graph(n=num_nodes, p=random.uniform(0.3, 0.6))
        
        for node in range(num_nodes + 1):
            self.node_colours[node] = 'lightblue'
        # Initial layout
        self.pos = nx.spring_layout(self.graph, seed=69)
        self.draw_graph()

        self.output_message(f"Random graph of length {num_nodes} generated")

    def add_node(self, entry_value):
        self.cancel_animation()
        if len(self.graph) == 10:
            self.output_message("Max number of nodes (10) reached for the graph")
            return
        
        try:
            if entry_value.strip() == "":
                value = random.choice(list(set(range(10)) - set(list(self.graph.nodes()))))
            else:
                value = int(entry_value)
        except ValueError:
            self.output_message("Please enter a valid node number")
            return
        
        if value < 0 or value > 9:
            self.output_message("Please enter a node number in suitable range: 0-9")
            return

        if value in self.graph.nodes():
            self.output_message(f"Node {value} already exists.")
            return

        self.graph.add_node(value) # Add a new node with the new identifier
        self.pos[value] = (random.random(), random.random()) # Add new node position randomly
        self.node_colours[value] = 'lightblue'
        self.draw_graph()
        self.output_message(f"Added node {value} to the graph\nGraph length: {len(self.graph)}")

    def delete_node(self, entry_value):
        self.cancel_animation()

        if len(self.graph) == 0:
            self.output_message("Graph is empty, no nodes to delete")
            return

        try:
            if entry_value.strip() == "":
                value = random.choice(list(self.graph.nodes()))
            else:
                value = int(entry_value)
        except ValueError:
            self.output_message("Please enter a valid node number")
            return

        if value not in self.graph.nodes():
            self.output_message(f"Node {value} does not exist.")
            return

        self.graph.remove_node(value)
        self.pos.pop(value, None)  # Remove the node position
        self.node_colours[value] = ""
        self.draw_graph()
        self.output_message(f"Deleted node {value} from the graph\nGraph length: {len(self.graph)}")

    def add_edge(self, node_from, node_to):
        self.cancel_animation()

        try:
            node1 = int(node_from)
            node2 = int(node_to)
        except ValueError:
            self.output_message("Please enter valid node numbers")
            return
        
        if node1 in self.graph.nodes() and node2 in self.graph.nodes():
            if self.graph.has_edge(node1, node2):
                self.output_message(f"Edge between {node1} and {node2} already exists")
            else:
                self.graph.add_edge(node1, node2)
                if self.is_weighted.get():
                    self.graph[node1][node2]['weight'] = random.randint(1, 20)  # Add random weight
                self.draw_graph()
        else:
            self.output_message(f"One or both nodes do not exist in the graph")

    def toggle_weights(self):
        if self.is_weighted.get():
            # Add weights to existing edges
            for (u, v) in self.graph.edges():
                if 'weight' not in self.graph[u][v]:
                    self.graph[u][v]['weight'] = random.randint(1, 20)
            self.get_weight.configure(state="normal")
        else:
            # Remove weights from the graph
            for (u, v) in self.graph.edges():
                if 'weight' in self.graph[u][v]:
                    del self.graph[u][v]['weight']
            self.get_weight.configure(state="disabled")
        self.draw_graph()

    def visualize_bfs(self, start_entry, find_entry):
        self.cancel_animation()
        self.found = False

        if len(self.graph) == 0: # Check if the graph is empty
            self.output_message("Graph is empty")
            return

        try:
            start_node = int(start_entry)
            find_node = None
            if find_entry.strip() != "":
                find_node = int(find_entry)
        except ValueError:
            self.output_message("Please enter a valid node number")
            return

        distance = 1

        if start_node not in self.graph.nodes():
            self.output_message(f"Node {start_node} is not in the graph")
            return

        self.reset_animation_variables()
        self.states[0] = [copy.deepcopy(self.node_colours), "", ""]
        visited = []
        queue = [start_node]
        while queue and not self.found:
            node = queue.pop(0)
            visited.append(node)
            self.highlight_node(node, 'r')  # Highlight visited node
            neighbours = set(self.graph.neighbors(node)) - set(visited) - set(queue) # Only adds the neighbours that have not been visited or queued into next nodes to visit
            queue.extend(neighbours)

            text = f"Visiting node {node}"
            if queue:
                text += f"\nQueue (nodes to visit): {queue}"
            else:
                text += f"\nNo more nodes to visit, BFS complete"

            if find_entry.strip() != "":
                text += f"\nNode {find_entry} NOT found"

            if neighbours:
                text += f"\n{neighbours} enqueued into the queue of nodes to visit next"
                if find_node not in queue:
                    distance += 1
            self.states[self.state_index] = [copy.deepcopy(self.node_colours), text, f"Start Node: {start_node}     Visited: {visited}"]
            self.state_index += 1

            if find_node == node:
                self.found = True
                self.highlight_node(node, 'green')
                self.states[self.state_index] = [copy.deepcopy(self.node_colours), f"Node {find_entry} found, {distance} edge(s) away from the start node {start_entry}", f"Start Node: {start_node}     Visited: {visited}"]
                self.state_index += 1

        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()


    def visualize_dfs(self, start_entry, find_entry):
        self.cancel_animation()
        self.found = False

        if len(self.graph) == 0:
            self.output_message("Graph is empty")
            return
        
        try:
            start_node = int(start_entry)
            find_node = None
            if find_entry.strip() != "":
                find_node = int(find_entry)
        except ValueError:
            self.output_message("Please enter a valid node number")
            return

        if start_node not in self.graph.nodes():
            self.output_message(f"Node {start_node} is not in the graph")
            return

        self.reset_animation_variables()
        self.states[0] = [copy.deepcopy(self.node_colours), "", ""]
        visited = []
        self.dfs_recursive(start_node, start_node, find_node, visited)

        if self.found:
            self.highlight_node(find_node, 'green')  # Highlight visited node
            text = f"Node {find_node} found"

            self.states[self.state_index] = [copy.deepcopy(self.node_colours), text, f"Start Node: {start_node}     Visited: {visited}"]
            self.state_index += 1

        if find_node and not self.found:
            text = f"Node {find_node} NOT found"

            self.states[self.state_index] = [copy.deepcopy(self.node_colours), text, f"Start Node: {start_node}     Visited: {visited}"]
            self.state_index += 1

        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def dfs_recursive(self, cur_node, start_node, find_node, visited):
        if self.found:
            return

        self.highlight_node(cur_node, 'orange')  # Highlight visited node

        visited.append(cur_node)
        self.states[self.state_index] = [copy.deepcopy(self.node_colours), f"Visiting node {cur_node} and add it to visited nodes", f"Start Node: {start_node}     Visited: {visited}"]
        self.state_index += 1

        if cur_node == find_node:
            self.found = True
            return

        for neighbour in self.graph.neighbors(cur_node):
            if neighbour not in visited:  # Only recurse on unvisited neighbors
                self.dfs_recursive(neighbour, start_node, find_node, visited)

    def clear_graph(self):
        self.generate_random_graph(num_nodes=0)
        self.output_message("Graph cleared")

    def highlight_node(self, node, colour):
        self.node_colours[node] = colour

    def on_click(self, event):
        if event.inaxes is None:
            return

        # Find the closest node to the click event
        click_pos = (event.xdata, event.ydata)
        for node, pos in self.pos.items():
            dist = (pos[0] - click_pos[0])**2 + (pos[1] - click_pos[1])**2
            if dist < 0.05:  # Adjust sensitivity as needed
                self.dragging_node = node
                break

    def on_drag(self, event):
        if self.is_running:
            self.toggle_pause()

        if event.inaxes is None or self.dragging_node is None:
            return

        # Update node position while dragging
        self.pos[self.dragging_node] = (event.xdata, event.ydata)
        self.draw_graph()

    def on_release(self, event):
        self.dragging_node = None

    def output_message(self, text):
        self.message_label.configure(text=text)

    def change_output(self, text):
        self.output_label.configure(text=text)

def main(master, window):
    window.geometry("1360x1020")
    window.minsize(1360, 1020)

    vis = GraphVisualiser(master)
    vis.pack(fill="both", expand=True)

    # Variables for animation
    vis.reset_animation_variables()

    # Set GUI components
    vis.setVis()

    # Connect mouse events for the drag and drop
    vis.connect_mouse_events()

    # Generate an initial random graph
    vis.generate_random_graph()
    
def test():
    root = ctk.CTk()
    root.geometry("1360x820")
    root.minsize(1360, 820)

    app = GraphVisualiser(root)
    app.pack(fill="both", expand=True)

    # Variables for animation
    app.reset_animation_variables()

    # Set GUI components
    app.setVis()

    # Connect mouse events for the drag and drop
    app.connect_mouse_events()

    # Generate an initial random graph
    app.generate_random_graph()

    root.mainloop()
    
#test()
