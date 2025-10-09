# Basic Tree (inherited off Graph):         Lines 23 - 477
# Binary Tree (inherited off Basic Tree):   Lines 479 - 846

# BFS and DFS are inherited and are the same function used in Graph

# Pre-order traversal:          Lines 444 - 458
# Post-order traversal:         Lines 460 - 474
# In-order traversal:           Lines 703 - 727

# Hierarchal layout function:   Lines 209 - 331


import customtkinter as ctk
import tkinter as tk # For boolean variable
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import graph_vis

class TreeVisualiser(graph_vis.GraphVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

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

        # Tree Generation
        self.random_graph_button = ctk.CTkButton(self.controls_frame, text="Generate Random Tree", command=self.generate_random_tree)
        self.random_graph_button.grid(row=0, column=0)

        self.clear_button = ctk.CTkButton(self.controls_frame, text="Clear Tree", command=self.clear_graph)
        self.clear_button.grid(row=0, column=2)

        # Adding nodes
        ctk.CTkLabel(self.controls_frame, text="Node to Add: (1-9)").grid(row=1, column=0)
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

        # Entry field for search node (for BFS and DFS)
        ctk.CTkLabel(self.controls_frame, text="Find:").grid(row=3, column=0)
        self.find_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.find_node_entry.grid(row=3, column=0, sticky="e")

        # Traversals (searches)
        self.bfs_button = ctk.CTkButton(self.controls_frame, width=50, text="BFS", command=lambda: self.visualize_bfs(0, self.find_node_entry.get()))
        self.bfs_button.grid(row=3, column=1, sticky="w", padx=30)

        self.dfs_button = ctk.CTkButton(self.controls_frame, width=50, text="DFS", command=lambda: self.visualize_dfs(0, self.find_node_entry.get()))
        self.dfs_button.grid(row=3, column=1, sticky="e", padx=30)

        # Tree Traversals
        ctk.CTkLabel(self.controls_frame, text="Tree Traversals:").grid(row=4, column=0)

        self.pre_button = ctk.CTkButton(self.controls_frame, width=50, text="Pre-order", command=lambda: self.tree_traversal(0, "pre"))
        self.pre_button.grid(row=4, column=1, sticky="w", padx=15)

        self.post_button = ctk.CTkButton(self.controls_frame, width=50, text="Post-order", command=lambda: self.tree_traversal(0, "post"))
        self.post_button.grid(row=4, column=2, sticky="w", padx=15)

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


        # Plot canvas for the tree
        ctk.CTkLabel(self.canvas_frame, text="Tree Visualiser", font=("Arial", 26, "bold"), fg_color="transparent").pack(pady=20)
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

    def generate_random_tree(self, num_nodes=None):
        if num_nodes is None:
            num_nodes = random.randint(5, 8)

        self.cancel_animation()
        
        self.graph.clear()  # Clear any previous graph
        
        # Create a tree structure
        self.graph = nx.Graph()
        
        # Add nodes
        self.graph.add_nodes_from(range(num_nodes))
        
        # Add random edges to create a tree
        # A tree with n nodes has exactly n-1 edges
        for i in range(1, num_nodes): # Since node 0 is the root node, every other node would have a parent
            # Connect node 'i' to random parent node
            parent = random.choice(range(i))
            self.graph.add_edge(parent, i)
        
        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'
        
        if len(self.graph) > 1:
            # Use hierarchical layout tp adjust positions after deleting the node correctly - only needed for more than one node 
            self.pos = self.hierarchical_layout()
        
        self.draw_graph()

    def hierarchical_layout(self):
        root = 0
        
        # This works by 
        # 1/ calculating the maximum depth of the graph and using each level as the y pos for the node - stores the number of nodes in each layer in the 'levels' dict
        #   does this with a bfs - so it can go through each level
        # 
        # 2/ then the nodes in each level is stored in the 'node_by_level' dict in the form of {'level': [list of nodes at this level]}
        # 
        # 3/ then gets the weights of each node - the weight of the node is the weight of the subtree it would make if it were the root node
        #   this goes from the leaf nodes to the root node (upwards), so each node weight is calculated by
        #   node weight = 'number of immediate children' + 'weight of each children' + 1
        #       'number of immediate children' is accessed with the in-built function'directed_tree.successors(node)'
        #       + 1 is for the parent node itself
        #       'weight of each children' is done by just accessing the dict again with the child node as the key - since it was already calculated
        #
        # 4/ gets x pos based off the nodes weight and the other nodes in the same level with a scale factor

        # Build a directed tree to track parent-child relationships
        self.directed_tree = nx.DiGraph()
        
        # Use BFS to build the directed tree and track levels
        levels = {root: 0}
        queue = [root]
        while queue:
            parent = queue.pop(0)
            for neighbor in self.graph.neighbors(parent):
                if neighbor not in levels:
                    levels[neighbor] = levels[parent] + 1
                    # Add direction from parent to child
                    self.directed_tree.add_edge(parent, neighbor)
                    queue.append(neighbor)

        # Calculate maximum depth of the layers
        if levels:
            max_level = max(levels.values())
        else:
            max_level = 0
        
        # Get the nodes of each level {level: [nodes]}
        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level:
                nodes_by_level[level] = []
            nodes_by_level[level].append(node)
        # Calculate the size of each subtree, where each node is the root of their own subtree
        subtree_sizes = {}
        
        # Start with leaf nodes (bottom layer)
        for level in range(max_level, -1, -1):
            for node in nodes_by_level.get(level, []):
                children = list(self.directed_tree.successors(node)) # Successors are the immediate children of the node
                if not children: # Leaf node
                    subtree_sizes[node] = 1 # Leaf nodes have size 1
                else:
                    # Sum of child subtree sizes plus this node
                    subtree_size = 1
                    for child in children:
                        subtree_size += subtree_sizes[child]

                    subtree_sizes[node] = subtree_size
        
        # Calculate horizontal positions
        positions = {}
        
        # Start with the root node at the center
        positions[root] = (0.5, 1.0)  # Root at top center
        
        # Calculate positions level by level
        for level in range(1, max_level + 1):
            # Process each node at this level
            for parent in nodes_by_level.get(level-1, []): # Process parent nodes from previous level
                children = []
                for child in self.directed_tree.successors(parent):
                    
                    if levels[child] == level:
                        children.append(child)
                        
                if not children:
                    pass
                    
                # Sort children for consistency - ascending from left to right
                children.sort()
                
                # Get parent position
                parent_x = positions[parent][0]
                
                # Calculate total subtree size for this parent's children
                total_subtree_size = sum(subtree_sizes[child] for child in children)
                
                # Calculate starting position (left edge of parent's children)
                # We want to center the children under their parent
                start_x = parent_x - (total_subtree_size / 2 * 0.05)  # Scale factor for width
                
                # Position each child
                for child in children:
                    child_subtree_size = subtree_sizes[child]
                    
                    # Calculate horizontal position based on subtree size
                    child_x = start_x + (child_subtree_size / 2 * 0.05)
                    
                    # Calculate y position based on level
                    child_y = 1.0 - (level / (max_level + 1))
                    
                    positions[child] = (child_x, child_y)
                    
                    # Move start_x for next child
                    start_x += child_subtree_size * 0.05
        
        # Normalize x positions to 0-1 range
        if positions:
            min_x = min(x for x, y in positions.values())
            max_x = max(x for x, y in positions.values())
            
            # Avoid division by zero if all nodes are vertically aligned
            x_range = max_x - min_x
            if x_range > 0:
                for node in positions:
                    x, y = positions[node]
                    normalized_x = (x - min_x) / x_range
                    positions[node] = (normalized_x, y)
        
        return positions
    
    def add_node(self, entry_value):
        self.cancel_animation()

        if len(self.graph.nodes()) == 10:
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
        
        if value < 1 or value > 9:
            self.output_message("Please enter a node number in suitable range: 1-9")
            return

        if value in self.graph.nodes():
            self.output_message(f"Node {value} already exists.")
            return

        nodes = list(self.graph.nodes())

        self.graph.add_node(value) # Add a new node with the new identifier
        self.pos[value] = (random.random(), random.random()) # Add new node position randomly
        self.node_colours[value] = 'lightblue'

        self.graph.add_edge(value, random.choice(nodes))

        # Use hierarchical layout tp adjust positions after adding a new node correctly
        self.pos = self.hierarchical_layout()

        self.draw_graph()

    def delete_node(self, entry_value):
        self.cancel_animation()

        if not self.graph.nodes():
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
        
        if value == 0:
            self.clear_graph()
            self.output_message("Tried to delete node 0 (root) so the entire tree is deleted other than the root")
            return

        removed_nodes = []
        queue = [value]
        while queue: # Traverse self.directed_tree to get children, remove child nodes from self.graph - since the position function updates the self.directed tree using self.graph
            # Get current node
            current = queue.pop(0)

            # Get children of current node
            children = list(self.directed_tree.successors(current))

            # Add children to the queue
            queue += children

            # Remove current node from self.graph
            self.graph.remove_node(current)

            removed_nodes.append(current)

        for node in removed_nodes:
            self.node_colours[node] = ""
        
        self.output_message(f"Node {value} and its subtree has been deleted")

        if len(self.graph) > 1:
            # Use hierarchical layout tp adjust positions after deleting the node correctly - only needed for more than one node 
            self.pos = self.hierarchical_layout()

        self.draw_graph()

    def tree_traversal(self, root, type):
        self.cancel_animation()
        self.reset_animation_variables()

        self.states[0] = [copy.deepcopy(self.node_colours), "", ""]
        
        if type == "pre":
            self.preorder_traversal(self.directed_tree, root)
        else: # type == post
            self.postorder_traversal(self.directed_tree, root)
        
        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def preorder_traversal(self, tree, node, visited=None):
        # For pre-order, at each node, we visit left subtree then right subtree
        if visited is None:
            visited = []
        
        # Visit the current node first
        visited.append(node)
        self.highlight_node(node, 'purple')

        self.states[self.state_index] = [copy.deepcopy(self.node_colours), f"Performing a pre-order traversal\nVisiting node: {node}", f"Visited: {visited}"]
        self.state_index += 1
        
        # Then visit all children
        for child in sorted(tree.successors(node)):  # Sort for consistent order - ensures that the left-most subtrees (lower values are visited first)
            self.preorder_traversal(tree, child, visited)

    def postorder_traversal(self, tree, node, visited=None):
        # For post-order, all the children subtrees are visited first, then the parent node
        if visited is None:
            visited = []
        
        # First visit all children
        for child in sorted(tree.successors(node)):  # Sort for consistent order
            self.postorder_traversal(tree, child, visited)
        
        # Then visit the current node
        visited.append(node)
        self.highlight_node(node, 'violet')

        self.states[self.state_index] = [copy.deepcopy(self.node_colours), f"Performing a post-order traversal\nVisiting node: {node}", f"Visited: {visited}"]
        self.state_index += 1
    
    def clear_graph(self):
        self.generate_random_tree(num_nodes=1)

class BinaryTreeVisualiser(TreeVisualiser):
    def __init__(self, master):
        super().__init__(master=master)

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

        # Tree Generation
        self.random_graph_button = ctk.CTkButton(self.controls_frame, text="Generate Random Tree", command=self.generate_random_tree)
        self.random_graph_button.grid(row=0, column=0)

        self.clear_button = ctk.CTkButton(self.controls_frame, text="Clear Tree", command=self.clear_graph)
        self.clear_button.grid(row=0, column=2)

        # Adding nodes
        ctk.CTkLabel(self.controls_frame, text="Node to Add: (1-9)").grid(row=1, column=0)
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

        # Entry field for search node (for BFS and DFS)
        ctk.CTkLabel(self.controls_frame, text="Find:").grid(row=3, column=0)
        self.find_node_entry = ctk.CTkEntry(self.controls_frame, width=50)
        self.find_node_entry.grid(row=3, column=0, sticky="e")

        # Traversals (searches)
        self.bfs_button = ctk.CTkButton(self.controls_frame, width=50, text="BFS", command=lambda: self.visualize_bfs(0, self.find_node_entry.get()))
        self.bfs_button.grid(row=3, column=1, sticky="w", padx=30)

        self.dfs_button = ctk.CTkButton(self.controls_frame, width=50, text="DFS", command=lambda: self.visualize_dfs(0, self.find_node_entry.get()))
        self.dfs_button.grid(row=3, column=1, sticky="e", padx=30)

        # Tree Traversals
        ctk.CTkLabel(self.controls_frame, text="Tree Traversals:").grid(row=4, column=0)

        self.pre_button = ctk.CTkButton(self.controls_frame, width=50, text="Pre-order", command=lambda: self.tree_traversal(0, "pre"))
        self.pre_button.grid(row=4, column=1, sticky="w", padx=15)

        self.in_button = ctk.CTkButton(self.controls_frame, width=50, text="In-order", command=lambda: self.tree_traversal(0, "in"))
        self.in_button.grid(row=4, column=1, sticky="e", padx=15)

        self.post_button = ctk.CTkButton(self.controls_frame, width=50, text="Post-order", command=lambda: self.tree_traversal(0, "post"))
        self.post_button.grid(row=4, column=2, sticky="w", padx=15)

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


        # Plot canvas for the tree
        ctk.CTkLabel(self.canvas_frame, text="Binary Tree Visualiser", font=("Arial", 26, "bold"), fg_color="transparent").pack(pady=20)
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

    def generate_random_tree(self, num_nodes=None):
        if num_nodes is None:
            num_nodes = random.randint(5, 8)

        self.cancel_animation()
        
        self.graph.clear()  # Clear any previous graph
        
        # Create a tree structure
        self.graph = nx.Graph()
        
        # Add nodes
        self.graph.add_nodes_from(range(num_nodes))

        # Add edges to binary tree
        self.families = {}
        self.valid_nodes = []

        # Initialise the root node
        self.families[0] = []
        self.valid_nodes.append(0)
        
        for i in range(1, num_nodes):
            parent = random.choice(self.valid_nodes)

            self.graph.add_edge(parent, i)

            self.families[parent].append(i) # Add child node to family dictionary for the current parent
            self.valid_nodes.append(i)
            self.families[i] = [] # Initialise the new child node into the families dictionary

            if len(self.families[parent]) == 2:
                self.valid_nodes.remove(parent)
        
        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'

        if len(self.graph) > 1:
            # Use hierarchical layout tp adjust positions after deleting the node correctly - only needed for more than one node 
            self.pos = self.hierarchical_layout()
        
        self.draw_graph()

    def tree_traversal(self, root, type):
        self.cancel_animation()
        self.reset_animation_variables()

        self.states[0] = [copy.deepcopy(self.node_colours), "", ""]
        
        if type == "pre":
            self.preorder_traversal(self.directed_tree, root)
        elif type == "in":
            self.inorder_traversal(self.directed_tree, root)
        else: # type == post
            self.postorder_traversal(self.directed_tree, root)
        
        # Reset node colours
        self.node_colours = {i: "" for i in range(10)}
        for node in self.graph.nodes():
            self.node_colours[node] = 'lightblue'

        self.is_running = True
        self.set_slider_attributes() # Give data to slider
        
        self.run_animation()

    def inorder_traversal(self, tree, node, visited=None):
        if visited is None:
            visited = []
        
        # Check if the node exists in the graph
        if node not in tree:
            raise ValueError(f"Node {node} does not exist in the graph.")
        
        children = sorted(tree.successors(node))  # Sort for consistent order
        
        if children:  # If there are children
            # Traverse the first child (left subtree)
            self.inorder_traversal(tree, children[0], visited)
        
        # Visit the current node
        visited.append(node)
        self.highlight_node(node, 'pink')

        self.states[self.state_index] = [copy.deepcopy(self.node_colours), f"Performing an in-order traversal\nVisiting node: {node}", f"Visited: {visited}"]
        self.state_index += 1
        
        if children:  # If there are children
            # Traverse the remaining children (right subtree)
            for child in children[1:]:
                self.inorder_traversal(tree, child, visited)

    def add_node(self, entry_value):
        self.cancel_animation()

        if len(self.graph.nodes()) == 10:
            self.output_message("Max number of nodes (10) reached for the graph")
            return
        
        try:
            if entry_value == "":
                value = random.choice(list(set(range(10)) - set(list(self.graph.nodes()))))
            else:
                value = int(entry_value)
        except ValueError:
            self.output_message("Please enter a valid node number")
            return
        
        if value < 1 or value > 9:
            self.output_message("Please enter a node number in suitable range: 1-9")
            return

        if value in self.graph.nodes():
            self.output_message(f"Node {value} already exists.")
            return
        
        # Check if valid_nodes is empty - if it is, reinitialize it
        if not self.valid_nodes:
            # If no valid nodes, we need to reset or initialize the valid_nodes
            # Take the first existing node as a valid parent
            if self.graph.nodes():
                first_node = list(self.graph.nodes())[0]
                self.valid_nodes = [first_node]
            else:
                # If no nodes exist yet, create node 0 as the root
                self.graph.add_node(0)
                self.pos[0] = (0.5, 0.5)
                self.node_colours[0] = 'lightblue'
                self.valid_nodes = [0]
                self.families[0] = []

        self.graph.add_node(value) # Add a new node with the new identifier
        self.pos[value] = (random.random(), random.random()) # Add new node position randomly
        self.node_colours[value] = 'lightblue'

        parent = random.choice(self.valid_nodes)

        self.graph.add_edge(parent, value)

        self.families[parent].append(value) # Add child node to family dictionary for the current parent
        self.valid_nodes.append(value)
        self.families[value] = [] # Initialise the new child node into the families dictionary

        if len(self.families[parent]) == 2:
            self.valid_nodes.remove(parent)

        if len(self.graph) > 1:
            # Use hierarchical layout tp adjust positions after deleting the node correctly - only needed for more than one node 
            self.pos = self.hierarchical_layout()

        self.draw_graph()

    def delete_node(self, entry_value):
        self.cancel_animation()

        if not self.graph.nodes():
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
        
        if value == 0:
            self.clear_graph()
            self.output_message("Tried to delete node 0 (root) so the whole tree is deleted other than the root")
            return

        remove_nodes = [] # Track the nodes removed (for subtree) for node_colours
        queue = [value]
        while queue: # Traverse self.directed_tree to get children, remove child nodes from self.graph - since the position function updates the self.directed tree using self.graph
            # Get current node
            current = queue.pop(0)

            # Get children of current node
            children = list(self.directed_tree.successors(current))

            # Add children to the queue
            queue += children

            # Remove current node from self.graph
            self.graph.remove_node(current)
            self.families.pop(current, None)
            if current in self.valid_nodes:
                self.valid_nodes.remove(current)

            remove_nodes.append(current)

        for node in remove_nodes:
            self.node_colours[node] = ""
        self.output_message(f"Node {value} and its subtree has been deleted")

        if len(self.graph) > 1:
            # Use hierarchical layout tp adjust positions after deleting the node correctly - only needed for more than one node 
            self.pos = self.hierarchical_layout()

        self.draw_graph()


def main(master, window):
    window.geometry("1360x1070")
    window.minsize(1360, 1070)
    
    # Create tabview widget
    tabview = ctk.CTkTabview(master)
    tabview.pack(padx=20, pady=20, fill="both", expand=True)

    # Create tabs
    tab1 = tabview.add("Basic Tree")
    tab2 = tabview.add("Binary Tree")

    vis1 = TreeVisualiser(tab1)
    vis1.pack(fill="both", expand=True)
    # Variables for animation
    vis1.reset_animation_variables()
    # Set GUI components
    vis1.setVis()
    # Generate an initial random graph
    vis1.generate_random_tree()

    vis2 = BinaryTreeVisualiser(tab2)
    vis2.pack(fill="both", expand=True)
    # Variables for animation
    vis2.reset_animation_variables()
    # Set GUI components
    vis2.setVis()
    # Generate an initial random graph
    vis2.generate_random_tree()
