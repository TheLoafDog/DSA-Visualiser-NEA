# Priority Queue:   301 - 358

# Question class:   12 - 18
# Timer class:      98 - 129
# Quiz Page class:  132 - 444


import customtkinter as ctk
import tkinter as tk
import random

class Question:
    def __init__(self, question_text, difficulty, topics, options, answer_position):
        self.question_text = question_text
        self.difficulty = difficulty
        self.topics = topics
        self.options = options
        self.answer_position = answer_position

# List of questions
question_pool = [
    # Array and Sorting
    Question("What is the average-case time complexity of a binary search on a sorted array?", 2, ["Sorting", "Array"], ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "O(log n)"),
    Question("Which sorting algorithm works best when the array is nearly sorted?", 2, ["Sorting", "Array"], ["Insertion Sort", "Quick Sort", "Bubble Sort", "Merge Sort"], "Insertion Sort"),
    Question("In an array-based implementation of quicksort, what is the purpose of the pivot?", 3, ["Sorting", "Array"], ["Divide array", "Sort elements", "Identify mid-point", "None of these"], "Divide array"),
    Question("Which of the following allows both efficient random access and sorting?", 3, ["Array", "Sorting"], ["Heap Sort", "Array Sort", "Linked List Sort", "Hashing"], "Array Sort"),
    Question("What is the worst-case time complexity of bubble sort?", 1, ["Sorting", "Array"], ["O(n)", "O(n^2)", "O(log n)", "O(n log n)"], "O(n^2)"),
    Question("Which sorting algorithm is stable and works in O(n log n) time?", 3, ["Sorting", "Array"], ["Merge Sort", "Quick Sort", "Heap Sort", "Bubble Sort"], "Merge Sort"),
    Question("Why is the space complexity of merge sort O(n)?", 2, ["Sorting", "Array"], ["Auxiliary arrays", "Recursive calls", "Unsorted data", "In-place operations"], "Auxiliary arrays"),
    Question("What data structure is typically used for iterative in-place quicksort?", 3, ["Sorting", "Array"], ["Stack", "Queue", "Heap", "Tree"], "Stack"),
    Question("What is the benefit of using insertion sort over merge sort for small datasets?", 2, ["Sorting", "Array"], ["Simpler implementation", "Lower space complexity", "Faster for small arrays", "Stable sorting"], "Faster for small arrays"),
    Question("Which sort algorithm uses a partitioning process to sort an array?", 2, ["Sorting", "Array"], ["Quick Sort", "Insertion Sort", "Merge Sort", "Bubble Sort"], "Quick Sort"),
    Question("In a sorted array, what is the best big O time complexity to search for an element?", 1, ["Sorting", "Array"], ["O(log n)", "O(n)", "O(n^2)", "O(1)"], "O(log n)"),
    Question("What is the advantage of using heap sort over quick sort?", 3, ["Sorting", "Array"], ["O(1) space", "Stability", "In-place sorting", "Lower average case time"], "O(1) space"),
    Question("Which sorting algorithm is best suited for external sorting (large files)?", 3, ["Sorting", "Array"], ["Merge Sort", "Insertion Sort", "Quick Sort", "Bubble Sort"], "Merge Sort"),


    # Graph and Tree
    Question("In an adjacency list representation of a Tree, what is the space complexity? (V = Vertices, E = Edges)", 3, ["Graph", "Tree"], ["O(V+E)", "O(V)", "O(V^2)", "O(log V)"], "O(V+E)"),
    Question("Which algorithm can be used to find the shortest path in both Graph and Tree?", 2, ["Graph", "Tree"], ["Dijkstra’s", "BFS", "DFS", "Kruskal’s"], "BFS"),
    Question("Which traversal method is shared between Tree and Graph structures?", 1, ["Graph", "Tree"], ["DFS", "Inorder", "Postorder", "Level-order"], "DFS"),
    Question("What is the difference between a Tree and a connected Graph?", 2, ["Graph", "Tree"], ["Tree are acyclic", "Graph are rooted", "Tree contain cycles", "Graph contain no leaves"], "Tree are acyclic"),
    Question("What is the time complexity of Depth First Search on a graph?", 2, ["Graph", "Tree"], ["O(V+E)", "O(V^2)", "O(log V)", "O(V)"], "O(V+E)"),
    Question("What type of graph does Kruskal’s algorithm work on?", 3, ["Graph", "Tree"], ["Weighted undirected", "Directed acyclic", "Unweighted", "Rooted graph"], "Weighted undirected"),
    Question("Which traversal algorithm uses a queue?", 2, ["Graph", "Tree"], ["BFS", "DFS", "Inorder", "Postorder"], "BFS"),
    Question("How many edges does a tree with V vertices contain?", 2, ["Graph", "Tree"], ["V-1", "V", "2V", "V/2"], "V-1"),
    Question("Which algorithm is best for finding a Minimum Spanning Tree?", 3, ["Graph", "Tree"], ["Prim's", "Dijkstra's", "DFS", "BFS"], "Prim's"),
    Question("What is the degree of a vertex in an undirected graph?", 1, ["Graph", "Tree"], ["Number of edges", "Number of vertices", "Connected components", "Cycle count"], "Number of edges"),
    Question("What data structure is used to implement Prim's algorithm?", 3, ["Graph", "Tree"], ["Priority Queue", "Stack", "Queue", "Heap"], "Priority Queue"),
    Question("Which graph traversal algorithm is used to detect cycles?", 3, ["Graph", "Tree"], ["DFS", "BFS", "Kruskal's", "Dijkstra's"], "DFS"),
    Question("What property does a binary search tree satisfy?", 2, ["Graph", "Tree"], ["Left < Root < Right", "Root < Left < Right", "All nodes equal", "Unsorted order"], "Left < Root < Right"),
    Question("Which graph representation uses adjacency matrices?", 2, ["Graph", "Tree"], ["Dense graphs", "Sparse graphs", "Weighted trees", "Unconnected graphs"], "Dense graphs"),

    # Stacks and Queues
    Question("Which data structure is best for implementing recursive function calls?", 1, ["Stack", "Queue"], ["Stack", "Queue", "Array", "Linked List"], "Stack"),
    Question("How can you reverse a queue using a stack?", 3, ["Stack", "Queue"], ["Push each element", "Pop and push all elements", "Sort elements", "Swap ends"], "Pop and push all elements"),
    Question("Which data structure is best suited for breadth-first traversal?", 2, ["Stack", "Queue"], ["Queue", "Stack", "Tree", "Array"], "Queue"),
    Question("Which operation is used to add an element to a stack?", 1, ["Stack", "Queue"], ["Push", "Pop", "Enqueue", "Dequeue"], "Push"),
    Question("What is the time complexity of dequeue operation in a circular queue?", 1, ["Stack", "Queue"], ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "O(1)"),
    Question("How does a priority queue differ from a normal queue?", 2, ["Stack", "Queue"], ["Elements ordered by priority", "Faster dequeue", "LIFO order", "Uses arrays"], "Elements ordered by priority"),
    Question("Which data structure supports both enqueue and dequeue in O(1)?", 3, ["Stack", "Queue"], ["Deque", "Stack", "Queue", "Heap"], "Deque"),
    Question("What is the primary use of a circular queue?", 2, ["Stack", "Queue"], ["Memory-efficient queue", "Faster searching", "FIFO replacement", "Sorted data"], "Memory-efficient queue"),
    Question("In a queue, what operation removes an element?", 1, ["Stack", "Queue"], ["Dequeue", "Enqueue", "Push", "Pop"], "Dequeue"),
    Question("What does a double-ended queue (Deque) allow?", 2, ["Stack", "Queue"], ["Insertion/removal at both ends", "Faster dequeue", "Priority order", "Single-ended access"], "Insertion/removal at both ends"),
    Question("Which operation removes the top element of a stack?", 1, ["Stack", "Queue"], ["Pop", "Push", "Dequeue", "Enqueue"], "Pop"),
    Question("What is the key property of a stack data structure?", 1, ["Stack", "Queue"], ["LIFO order", "FIFO order", "Random access", "Priority order"], "LIFO order"),

    # Linked List and Stack
    Question("In a singly linked list, which structure can be used to reverse it efficiently?", 3, ["Linked List", "Stack"], ["Stack", "Queue", "Array", "Graph"], "Stack"),
    Question("A stack implemented with a linked list provides efficient time complexity for which operations?", 2, ["Linked List", "Stack"], ["Push and Pop", "Insert and Delete", "Access and Search", "Traverse"], "Push and Pop"),
    Question("Which data structure is most efficient for maintaining browser history?", 1, ["Linked List", "Stack"], ["Stack", "Queue", "Linked List", "Array"], "Stack"),
    Question("Which structure is used to implement undo functionality in many software?", 2, ["Linked List", "Stack"], ["Stack", "Queue", "Linked List", "Tree"], "Stack"),

    # Array and Queues
    Question("In a circular queue implemented with an array, when is the queue full?", 3, ["Array", "Queue"], ["(rear+1) % size == front", "rear == front", "rear == size-1", "front == 0"], "(rear+1) % size == front"),
    Question("How can a fixed-size array be used to implement a dynamic circular queue?", 3, ["Array", "Queue"], ["Wrap-around with modulo", "Use linked list", "Extend array", "Heapify array"], "Wrap-around with modulo"),
    Question("Which data structure allows FIFO access using an array?", 1, ["Array", "Queue"], ["Queue", "Stack", "Linked List", "Binary Tree"], "Queue"),
    Question("What is the purpose of using a queue to handle arrays in scheduling?", 3, ["Array", "Queue"], ["Efficient resource allocation", "Increased space", "Reduced complexity", "Lower memory"], "Efficient resource allocation"),

    # Array and Linked List
    Question("What is the advantage of a linked list over an array in terms of memory?", 2, ["Array", "Linked List"], ["Dynamic memory allocation", "Lower space complexity", "Random access", "None of these"], "Dynamic memory allocation"),
    Question("Which structure allows O(1) insertion at both head and tail without shifting?", 3, ["Array", "Linked List"], ["Doubly linked list", "Array", "Binary Tree", "Stack"], "Doubly linked list"),
    Question("What data structure would best suit an expanding list with frequent insertions?", 2, ["Array", "Linked List"], ["Linked List", "Array", "Stack", "Tree"], "Linked List"),
    Question("Inserting at an arbitrary position in which structure is more efficient?", 3, ["Array", "Linked List"], ["Linked List", "Array", "Stack", "Tree"], "Linked List"),
    Question("What is the time complexity to insert at the head of a linked list?", 2, ["Linked List"], ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "O(1)"),
    Question("How is memory allocated in a linked list?", 3, ["Linked List"], ["Dynamic allocation", "Contiguous allocation", "Heap allocation", "Static allocation"], "Dynamic allocation"),
    Question("What is the advantage of a doubly linked list over a singly linked list?", 3, ["Linked List"], ["Traversal in both directions", "Lower space usage", "Faster search", "Simpler structure"], "Traversal in both directions"),
    Question("How many pointers are needed to implement a singly linked list?", 2, ["Linked List"], ["One per node", "Two per node", "Three per node", "None"], "One per node"),
    Question("What is the main disadvantage of linked lists compared to arrays?", 2, ["Linked List"], ["No random access", "Higher space complexity", "Faster searching", "Static size"], "No random access"),
    Question("Which operation has O(1) time complexity in a singly linked list?", 3, ["Linked List"], ["Insertion at head", "Traversal", "Deletion at tail", "Searching"], "Insertion at head"),
    Question("What is a circular linked list?", 2, ["Linked List"], ["Last node points to head", "Doubly linked nodes", "Sorted linked list", "Head points to tail"], "Last node points to head"),
    Question("What type of linked list has no NULL pointers?", 2, ["Linked List"], ["Circular linked list", "Singly linked list", "Doubly linked list", "Static linked list"], "Circular linked list"),
    Question("Which data structure does not require shifting elements on deletion?", 1, ["Linked List"], ["Linked List", "Array", "Stack", "Queue"], "Linked List"),
    Question("What is the space complexity of a doubly linked list node?", 2, ["Linked List"], ["O(2)", "O(1)", "O(n)", "O(log n)"], "O(2)"),
]

# Making a frame that hold the timer
class timer(ctk.CTkLabel):
    def __init__(self, root, callback=None):
        super().__init__(master=root, fg_color="transparent", font=("Arial Black", 20, "bold"))
        self.root = root
        self.callback = callback
        
        self.time =  0
        self.running = False
        
    def update_timer(self):
        if self.running and self.time > 0:
            self.time -= 1
            self.configure(text="Timer: " + str(self.time))
            self.after(1000, self.update_timer)  # Call this method again after 1 second
        elif self.time == 0:
            self.running = False
            self.configure(text="Time's up!")
            if self.callback:
                self.callback()
    
    def stop_timer(self):
        self.running = False
    
    def start_timer(self):
        if not self.running:  # Avoid starting multiple timers
            self.running = True
            self.update_timer()
            
    def set_time(self, difficulty):
        self.time = difficulty * 15 # Time taken to do a question based off difficulty increases by 15 seconds each
        self.configure(text="Timer: " +  str(self.time))
        self.start_timer()

class QuizPage(ctk.CTkFrame):
    def __init__(self, root, DSA=None):
        super().__init__(master=root, fg_color="transparent", height=600, width=600)
        self.root = root

        self.pack_propagate(False)  # Prevent resizing to fit content 
        self.DSAs = ['Array', 'Queue', 'Stack', 'Graph', 'Tree', 'Linked List', 'Sorting', 'Searching']

        if DSA:
            self.current_DSA = DSA
            self.initialise(self.current_DSA)
        else:
            # Initialise the unlimited mode page
            self.initialise()
            # During the initialisation, the variables needed for the quiz page will be made otherwise an error occurs
    
    def initialise(self, DSA=None):
        # Title
        self.title = ctk.CTkLabel(self, text="QUIZ!", font=("Arial Black", 30, "bold"))
        self.title.pack(pady=50)
        
        # Create the frame that will be in the middle of the page to hold options and mode
        self.create_selection_frame(DSA)
    
    def create_selection_frame(self, current_DSA=None):
        # Frame that will be in the middle of the page to hold options and mode
        self.selection_frame = ctk.CTkFrame(self, border_width=0)
        self.selection_frame.pack(pady=10)

        # Frame that will hold all the topics
        self.topics_frame = ctk.CTkFrame(self.selection_frame, width=200, height=300, border_width=0)
        self.topics_frame.grid_propagate(False)
        self.topics_frame.grid_rowconfigure(0, weight=2)
        self.topics_title = ctk.CTkLabel(self.topics_frame, text="DSA Topics List", font=("Arial Black", 20, "bold"))
        self.topics_title.grid(row=0, column=0, sticky="w", padx=10, pady=3)
        
        self.topics = [] # This is for the checked off topics
        for i, DSA in enumerate(self.DSAs):
            self.option_checkbox = ctk.CTkCheckBox(self.topics_frame, width = 10, height = 10, corner_radius=20, text=DSA, command=lambda topic=DSA : self.change_topics_filter(topic))
            self.option_checkbox.grid(row=i+1, column=0, sticky="w", padx=10, pady=3)
        
        # Frame that lets the user pick which mode to use
        self.mode_frame = ctk.CTkFrame(self.selection_frame, width=200, height=100, border_width=0)
        self.mode_frame.pack_propagate(False)
        self.mode_frame.pack(padx=10, pady=5, side="left")
        
        self.show_topics = tk.BooleanVar()
        self.quiz_radio_btn = ctk.CTkRadioButton(self.mode_frame, text="Quiz", variable=self.show_topics, value=True, command=lambda: self.toggle_topics_frame(self.topics_frame))
        self.quiz_radio_btn.pack(expand=True)
        self.unlimited_radio_btn = ctk.CTkRadioButton(self.mode_frame, text="Unlimited", variable=self.show_topics, value=False, command=lambda: self.toggle_topics_frame(self.topics_frame))
        self.unlimited_radio_btn.pack(expand=True)
        
        # Start button to start quiz
        self.start_button = ctk.CTkButton(self, text="Start", font=("Arial", 26), command=lambda: self.start_unlimited())
        self.start_button.pack(pady=50)
        
        if current_DSA != None: # If there is not "None" DSA
            # Changes from Quiz mode with the DSA being ticked off
            self.quiz_radio_btn.invoke()
            for checkbox in self.topics_frame.winfo_children():
                if current_DSA == checkbox.cget("text"):
                    checkbox.toggle()
    
    def change_topics_filter(self, topic): # Topics are just DSAs in this case
        if topic in self.topics:
            self.topics.remove(topic)
            if not self.topics:
                self.start_button.configure(state="disabled")
        else:
            self.topics.append(topic)
            self.start_button.configure(state="normal")
            
    
    def toggle_topics_frame(self, frame):
        if self.show_topics.get():
            frame.pack(padx=10, pady=5, side="left")
            if not self.topics:
                self.start_button.configure(state="disabled")
            self.start_button.configure(command=lambda: self.start_quiz())
        else:
            frame.pack_forget()
            self.start_button.configure(state="normal")
            self.start_button.configure(command=lambda: self.start_unlimited())
    
    def start_quiz(self):
        for child in self.winfo_children():
            child.destroy()
        # Initialise quiz variables
        self.front = -1  # Points to the highest priority element
        self.rear = -1   # Points to the last inserted position
        self.size = 7 # Fixed size of the array: 7

        self.selected_answer = ctk.StringVar()
        self.score = 0
        
        # Retrieve the questions using a priority queue
        self.questions = [None] * self.size # This will be the fixed priority queue
        self.get_sorted_questions(question_pool, self.topics, self.size) # Run procedure to get questions
        
        self.create_widgets("quiz")
        self.show_question("quiz")
        
    def start_unlimited(self):
        for child in self.winfo_children():
            child.destroy()
        # Initialise unlimited test variables
        random.shuffle(question_pool)
        self.questions = question_pool
        self.front = 0 # Single pointer (points to the current question
        self.selected_answer = ctk.StringVar()
        self.score = 0
        self.total = 0
        
        self.create_widgets("unlimited")
        self.show_question("unlimited")

    def create_widgets(self, state):
        # Question label
        self.question_label = ctk.CTkLabel(self, text="", wraplength=400, font=("Arial", 20))
        self.question_label.pack(pady=20, padx=20, expand=True)

        # Initialise the next button
        self.next_button = ctk.CTkButton(self, text="Next", command=lambda: self.finish_question(state))
        
        # Make the timer label
        self.timer = timer(self, callback=lambda: self.finish_question(state))
        self.timer.pack(pady=10, expand=True)
        
        # Radio buttons for options
        self.answer_holder = ctk.CTkFrame(self, fg_color="transparent", border_width=0)
        self.answer_holder.pack(pady=40, expand=True)
        self.radio_buttons = []
        for i in range(0, 4):  # Assuming max 4 options
            radio_button = ctk.CTkRadioButton(self.answer_holder, text="", font=("Arial", 18), value=i, variable=self.selected_answer, command=lambda: self.activate_next())
            radio_button.pack(anchor="w", padx=20, pady=5)
            self.radio_buttons.append(radio_button)
        
        # Score label
        if state == "quiz":
            string = "Score: " + str(self.score) + "/7"
        else:
            string = "Score: " + str(self.score) + "/" + str(self.total)
        
        self.score_label = ctk.CTkLabel(self, text=string, font=("Black Arial", 20))
        self.score_label.pack(expand=True)
        
        # Pack the next button
        self.next_button.pack(pady=20, expand=True)
        
        # Initialise the answer frame that will show up when an answer is submitted
        self.show_answer = ctk.CTkFrame(self)
        
        self.option_selected = ctk.CTkLabel(self.show_answer)
        self.option_selected.pack(pady=5, padx=5)
        self.actual_answer = ctk.CTkLabel(self.show_answer, text_color="green")
        self.actual_answer.pack(pady=5, padx=5)
        self.ok_button = ctk.CTkButton(self.show_answer, text="Ok", command=lambda: self.hide_answer(state))
        self.ok_button.pack(pady=5, padx=5)
    
    def hide_answer(self, state):
        self.show_answer.place_forget()
        self.next_question(state)
    
    def activate_next(self):# Activates the next button only if the user selects an answer
        self.next_button.configure(state="normal")

    def isEmpty(self):
        return self.front == -1

    def isFull(self):
        return self.rear == self.size - 1

    def enqueue(self, question, priority): # question is the object and priority is an attribute
        if self.isFull():
            return
        
        if self.isEmpty():
            # If the queue is empty, insert at the first position and initialise both pointers
            self.front = 0
            self.rear = 0
            self.questions[self.rear] = question
        else:
            # Insert in the correct position based on priority, shift elements one by one
            temp = self.rear
            while temp >= self.front and self.questions[temp].difficulty > priority:
                self.questions[temp + 1] = self.questions[temp]  # Shift element to the right
                temp -= 1
            self.questions[temp + 1] = question  # Insert the new question
            self.rear += 1
            
    def dequeue(self):
        if self.isEmpty():
            return None
        
        # Retrieve the element at the front
        question = self.questions[self.front]
        # Move the front pointer forward
        #self.front += 1 - this line is unecessary since self.front is incremented outside
        
        # Reset front and rear pointers if queue is empty
        if self.front > self.rear:
            self.front = -1
            self.rear = -1
        
        return question
            
    def filter_questions(self, questions, topics):
        filtered_questions = []
        # Multiple topics and questions are possible so a nested for loop is used
        for topic in topics:
            for q in questions:
                if topic in q.topics:
                    filtered_questions.append(q)
        return filtered_questions
    
    def get_sorted_questions(self, questions, topics, num_questions=7):
        # Step 1: Filter questions that contain the specified topic
        filtered_questions = self.filter_questions(questions, topics)
        # Step 2: Shuffle and insert by difficulty to create a priority queue
        random.shuffle(filtered_questions)  # Randomized order
        
        for i in range(num_questions):
            question = filtered_questions[i]
            self.enqueue(question, question.difficulty)

    def show_question(self, state):
        # Deactivate the self.next_button
        self.next_button.configure(state="disabled")
        
        if state == "unlimited":
            # Show the current question and options
            if self.front < len(self.questions):
                question = self.questions[self.front]
                self.change_question_widgets(question) # Output the question, options and time
            else:
                self.end_quiz()  # Show end screen if no more questions
        else: # Otherwise state == "quiz"
            # Show the current question and options
            if self.front <= self.rear:
                question = self.dequeue()
                self.change_question_widgets(question) # Output the question, options and time
            else:
                self.end_quiz()  # Show end screen if no more questions

    def change_question_widgets(self, question):
        self.timer.set_time(question.difficulty)
        self.question_label.configure(text=str(self.front+1) + ". " + question.question_text)
        self.selected_answer.set(None)  # Reset selected answer
        random.shuffle(question.options) # Randomise order of options
        for i, option in enumerate(question.options):
            self.radio_buttons[i].configure(text=option, state="normal") # Change text and reactivate them
            self.radio_buttons[i].pack()  # Show the option

    def finish_question(self, state):
        # Pause the time
        self.timer.stop_timer()
        
        for i in range(0,4):
            self.radio_buttons[i].configure(state="disabled") # Deactivate the radio buttons
        # If time runs out, the user may have not selected an answer (returns "None", so the selection to check if below
        try: # If an answer is selected
            option_selected = "Selected Answer: " + self.radio_buttons[int(self.selected_answer.get())].cget("text")
            # Check if answer is correct and adds 1 to score if it is.
            if self.radio_buttons[int(self.selected_answer.get())].cget("text") == self.questions[self.front].answer_position:
                self.score += 1
                self.option_selected.configure(text_color="green")
            else:
                self.option_selected.configure(text_color="red")
                if state == "unlimited":
                    self.questions.append(self.questions[self.front]) # Adds the question back into the questions
        except:
            option_selected = "No option selected"
            self.option_selected.configure(text_color="white")

        actual_answer = "Correct Answer: " + self.questions[self.front].answer_position
        
        # Above are the strings, whilst below are the CTk labels
        self.option_selected.configure(text=option_selected)
        self.actual_answer.configure(text=actual_answer)
            
        if state == "quiz":
            string = "Score: " + str(self.score) + "/7"
        else:
            self.total += 1
            string = "Score: " + str(self.score) + "/" + str(self.total)
        self.score_label.configure(text=string)
    
        self.show_answer.place(relx=0.5, rely=0.5, anchor="center")

    def next_question(self, state):
        # Proceed to the next question if an answer is selected
        self.front += 1 # Increments front pointer here so it works for both modes
        self.show_question(state)

    def end_quiz(self):
        for button in self.radio_buttons:
            button.pack_forget()
        self.timer.pack_forget()
        # Display end of quiz message
        display_msg = {1 : "Well done.", 2: "Practice makes perfect.", 3: "Come back again after some practice."}
        if self.score < 4:
            performance = 3
        elif self.score < 6:
            performance = 2
        else:
            performance = 1
        self.question_label.configure(text="Quiz Complete!\n" + display_msg[performance])
        self.next_button.configure(text="Back", state="normal", command=lambda: self.reset_quiz()) # Change next button so that the page is reset

    def reset_quiz(self):
        for child in self.winfo_children():
            child.destroy()
        self.initialise()

def main(root, DSA):
    Quiz_page = QuizPage(root, DSA)
    Quiz_page.pack(expand=True, anchor="center")

