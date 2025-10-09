# Inheritance of Pages:                     Lines 343 - 467
# dsa_frame class with filtering of DSAs:   Lines 236 - 342
# search frame with linear search:          Lines 143 - 226

# basic python import modules
from customtkinter import *
from tkinter import *
from PIL import Image
from tkinter import messagebox
import ast
import math

# my own python files
import Quiz

import stack_vis
import array_vis
import graph_vis
import sorting_vis
import searching_vis
import queue_vis
import linked_list_vis
import tree_vis

# this is the header class for the main page
class header(CTkFrame):
    def __init__(self, root, state, DSA, window):
        super().__init__(root, corner_radius=0)
        self.root = root # This is the master for the header (the page)
        self.state = state # This is to identify what type of page it is in
        self.DSA = DSA # The DSA that is in use
        self.window = window # This is the actual CTK window: passed into search_frame, heading btn, and the left and right button in the header.
            
            # widgets
        self.heading = CTkButton(self, text="Algolytics", font=("Arial Black", 24, "bold"), hover_color=["gray85", "gray15"], fg_color="transparent", command=lambda: self.main_page(self.window))
        self.search_frame = search_frame(self, self.root, self.window)
        self.left_btn = CTkButton(self, fg_color="gray", height=30, width=20, corner_radius=1000, border_width=3)
        self.right_btn = CTkButton(self, fg_color="gray", height=30, width=20, corner_radius=1000, border_width=3)
        
            # define a grid
        self.grid_columnconfigure(0, weight = 1) ##empty for spacing and cleaner layout
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 3) ##empty for spacing and cleaner layout
        self.grid_columnconfigure(3, weight = 1)
        self.grid_columnconfigure(4, weight = 7) ##empty for spacing and cleaner layout
        self.grid_columnconfigure(5, weight = 3)
        self.grid_columnconfigure(6, weight = 2) ##empty for spacing and cleaner layout
        self.grid_columnconfigure(7, weight = 1)
        self.grid_columnconfigure(8, weight = 1) ##empty for spacing and cleaner layout                                             
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        
            # place widgets
        self.heading.grid(row = 1, column = 3, pady=25)
        
        if self.state != "main":
            self.search_frame.grid(row = 1, column = 5)
            
        if self.state != "quiz":
            self.left_btn.grid(row = 1, column = 1)
            self.left_btn.configure(text="Quiz")
            self.left_btn.configure(command=lambda: self.quiz(self.DSA, window))
        
        if self.state == "revision" or self.state == "visualiser":
            self.right_btn.grid(row = 1, column = 7)
        
        if self.state == "revision":
            self.right_btn.configure(text="Visualiser")
            self.right_btn.configure(command=lambda: self.visualiser(self.DSA, window))
            
        if self.state == "visualiser":
            self.right_btn.configure(text="Revision")
            self.right_btn.configure(command=lambda: self.revision(self.DSA, window))

    def main_page(self, window):
        self.root.clear_page()
        
        # Main menu
        self.main_page = main_page(window, "main")
        self.main_page.pack(expand=True, fill="both")
    
    def revision(self, name, window):
        self.root.clear_page()
        
        # Revision page
        self.revision_page = revision_page(window, name, "revision")
        self.revision_page.pack(expand=True, fill="both")
        
    def visualiser(self, name, window):
        self.root.clear_page()
        
        # Visualiser page
        self.visualiser_page = visualiser_page(window, name, "visualiser")
        self.visualiser_page.pack(expand=True, fill="both")
        
    def quiz(self, name, window):
        self.root.clear_page()
        
        # Quiz page
        self.quiz_page = quiz_page(window, "quiz", name)
        self.quiz_page.pack(expand=True, fill="both")
    
class footer(CTkFrame):
    def __init__(self, root, height):
        super().__init__(root, height=height, corner_radius=0)
        self.root = root
        self.corner_radius = 0
        self.height = height
        
        if get_appearance_mode() == "light":
            self.appearance_mode = True
        else:
            self.appearance_mode = False
        
            # widgets
        self.appearance_mode_image = CTkImage(light_image=Image.open("light-mode-sun.webp"),
                                            dark_image=Image.open("dark-mode-moon.webp"),
                                            size=(30,30))
        self.text = StringVar(value="dark")
        self.mode = CTkButton(self, textvariable=self.text, image=self.appearance_mode_image, fg_color="gray", height=35, width=20, corner_radius=1000, border_width=3, command=self.changeAppearance)
        
            # place widgets
        self.mode.place(relx=0.1, rely=0.5, anchor="center")

            # widgets
        self.description = CTkLabel(self, fg_color="transparent", text="Data Structure and Algorithms\nVisualiser and Learning Tool")
        self.owner = CTkLabel(self, fg_color="transparent", text="Brandon Jake Nuñez")

            # place widgets
        self.description.place(relx=0.5, rely=0.3, anchor="center")
        self.owner.place(relx=0.5, rely=0.8, anchor="center")

    def changeAppearance(self):
        if self.appearance_mode:
            set_appearance_mode("dark")
            self.text.set(value="dark")
        else:
            set_appearance_mode("light")
            self.text.set(value="light")
        self.appearance_mode = not self.appearance_mode

class search_frame(CTkFrame):
    def __init__(self, root, page, window, corner_radius=0):
        super().__init__(root)
        self.root = root
        self.page = page
        self.window = window
        
        self.search_entry = CTkEntry(self, placeholder_text="Type to search...", corner_radius=0)
        self.search_entry.bind("<KeyRelease>", self.update_recommendations)  # Bind key release to update recommendations
        
        self.search_icon = CTkImage(Image.open("magnifying-glass-icon.png"),
                                            size=(21,21))
        self.search_btn = CTkButton(self, image=self.search_icon, width=8, text="", hover=False, state="disabled", corner_radius=0)
        
        self.search_entry.pack(side=LEFT)
        self.search_btn.pack(side=LEFT)
        
        self.x = self.winfo_rootx()
        self.y = self.winfo_rooty() + self.winfo_height()
        
        # Listbox widget for dropdown recommendations (using Tkinter)
        self.recommendation_listbox = Listbox(self.window, width=50, height=5)
        self.recommendations = DSAs_array
        
        # Bind selection event to the listbox
        self.recommendation_listbox.bind("<<ListboxSelect>>", self.handle_selection)

        # Bind window resize event
        self.window.bind("<Configure>", self.on_window_resize)
        
    def update_recommendations(self, event):
        # Update the dropdown list based on user input.
        query = self.search_entry.get().strip().lower()
        
        # Show dropdown only if there is input
        if query:
            # Filter recommendations that contain the query string
            matching_recommendations = [item for item in self.recommendations if query in item.lower()]

            # Update the listbox
            if matching_recommendations:
                self.recommendation_listbox.delete(0, "end")  # Clear previous items
                for item in matching_recommendations:
                    self.recommendation_listbox.insert("end", item)
            else:
                self.recommendation_listbox.delete(0, "end")
                self.recommendation_listbox.insert("end", "No matches")  # Output message if no match
                # Optionally keep the dropdown visible to show "No matches"
            
            self.update_listbox_position()
        else:
            self.recommendation_listbox.place_forget()  # Hide dropdown if no input

    def update_listbox_position(self):
        # Get the absolute position of the search frame and do some math to get the place coordinates
        # Calculate position for the listbox to appear directly under the search frame
        x = self.search_entry.winfo_rootx() - self.window.winfo_rootx()
        y = self.search_entry.winfo_rooty() - self.window.winfo_rooty() + self.search_entry.winfo_height()
        
        # Place the listbox at the calculated position
        self.recommendation_listbox.place(x=x, y=y, width=self.search_entry.winfo_width())
    
    def on_window_resize(self, event):
        # If the recommendation listbox is already placed, update its position when the windo is resized
        if self.recommendation_listbox.winfo_viewable():
            self.update_listbox_position()

    def handle_selection(self, event):
        # Handle when a user selects an option from the dropdown
        selected_index = self.recommendation_listbox.curselection()
        if selected_index:
            selected_value = self.recommendation_listbox.get(selected_index[0])
            if selected_value != "No matches":
                try:
                    self.revision_page(selected_value)
                except:
                    pass
        
    def revision_page(self, name):
        self.page.clear_page()
        
        # Revision page
        self.revision_page = revision_page(self.window, name, "revision")
        self.revision_page.pack(expand=True, fill="both") 

class dsa_frame(CTkFrame):
    def __init__(self, root, page, window):
        super().__init__(root)
        self.root = root
        self.page = page
        self.window = window

        self.corner_radius = 30
        self.fg_color="transparent"
        
        ##########''''''''''''''''''
                    
        # The filter frame that can filter the DSAs in the scroll frame
        self.filter_frame = CTkFrame(self, width = 280, height = 500, corner_radius = 20, fg_color = "gray")
        self.filter_frame.pack(side=LEFT, padx = 10, pady = 10, fill="y")
        
        # Configure grid for the filter frame
        self.filter_frame.grid_columnconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(1, weight=1)
        self.filter_frame.grid_rowconfigure(0, weight=1)
        self.filter_frame.grid_rowconfigure(1, weight=2)
        for i in range(15):  #15 rows in total including the 12 options and the 3 extra rows
            self.filter_frame.grid_rowconfigure(i+1, weight=1)
        
        self.filter_title = CTkLabel(self.filter_frame, text="Filter", font=("Arial Black", 20, "bold"), text_color="black")
        self.apply_btn = CTkButton(self.filter_frame, text="Apply", font=("Arial Black", 12, "bold"), width=9, corner_radius = 10, command=self.filterScrollFrame)
        self.reset_btn = CTkButton(self.filter_frame, text="Reset", font=("Arial", 12, "bold"), text_color="lightgray", fg_color="transparent", width=9, corner_radius = 10, command=self.reset_filter)
        self.types_title = CTkLabel(self.filter_frame, text="Types", font=("Arial Black", 16), fg_color="transparent")
        self.categories_title = CTkLabel(self.filter_frame, text="Categories", font=("Arial Black", 16), fg_color="transparent")
        
        self.filter_title.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.apply_btn.grid(row=15, column=0, padx=10, pady=10)
        self.reset_btn.grid(row=15, column=1, padx=10, pady=10, sticky="w")
        self.types_title.grid(row=1, column=0, sticky="nw", padx=10, pady=3)
        self.categories_title.grid(row=1, column=1, sticky="nw", padx=10, pady=3, rowspan=2)
        
        self.checked_filters = []
        
        for i, dsa_type in enumerate(types):
            # add checkboxes to the types
            self.option_checkbox = CTkCheckBox(self.filter_frame, width = 10, height = 10, corner_radius=20, text=dsa_type, command=lambda name=dsa_type : self.change_filter(name))
            self.option_checkbox.grid(row=i+2, column = 0, sticky="w", padx=10, pady=3)
            
        for i, dsa_category in enumerate(categories):
            # add checkboxes to the categories
            self.option_checkbox = CTkCheckBox(self.filter_frame, width = 10, height = 10, corner_radius=20, text=dsa_category, command=lambda name=dsa_category : self.change_filter(name))
            self.option_checkbox.grid(row=i+2, column = 1, sticky="w", padx=10, pady=3)
            
        ##########''''''''''''''''''''''''''
    
        # The Scroll Frame that holds the actual buttons
        self.dsaScrollFrame = CTkScrollableFrame(self, width = 660, height = 500, fg_color = "gray")
        self.dsaScrollFrame.pack(side=LEFT, padx = 10, pady = 10)
        
        self.remakeScrollFrame(DSAs_array)
    
    def change_filter(self, name):
        if name in self.checked_filters:
            self.checked_filters.remove(name)
        else:
            self.checked_filters.append(name)
            
    def reset_filter(self):
        self.remakeScrollFrame(DSAs_array) # reset scroll frame
        self.checked_filters = [] # reset checked_filters array
        
        for child in self.filter_frame.winfo_children(): # reset each checkbox in the filter frame
            try:
                child.deselect()
            except:
                pass

    def filterScrollFrame(self):
        newListDSA = []
        for DSA in DSAs_array:  # Iterates each DSA to check with filters
            for f in self.checked_filters:  # Iterates each filter
                if DSA not in newListDSA:  # Check to see if DSA is already checked (more than one category or type can match)
                    if f in hashDataRetrieve(DSA)['categories'] or f in hashDataRetrieve(DSA)['types']:  # Check categories and types
                        newListDSA.append(DSA)
        self.remakeScrollFrame(newListDSA)
        
    def remakeScrollFrame(self, newListDSA):
        for child in self.dsaScrollFrame.winfo_children():
            child.destroy()
        # clears the scroll frame
        
        for i, DSA in enumerate(newListDSA):
            self.dsaButtonFrame = CTkFrame(self.dsaScrollFrame, width = 650, height = 75, corner_radius = 6, fg_color = "#676b68")
            # Add the categories and types in the text of the description
            categories_text = " | ".join(hashDataRetrieve(DSA)['categories'])
            types_text = " | ".join(hashDataRetrieve(DSA)['types'])
            description_text = categories_text + ' | ' + types_text
            self.dsaButtonDescription = CTkLabel(self.dsaButtonFrame, text = description_text, width = 150, height = 50, font = ("Arial", 11), fg_color = "transparent")
            self.dsaButton = CTkButton(self.dsaButtonFrame, width = 200, height = 55, corner_radius = 6, text = hashDataRetrieve(DSA)['name'], text_color = "white", fg_color = "lightblue", font = ("Arial Black", 18), command = lambda name=hashDataRetrieve(DSA)['name']: self.showInfo(name, self.window))
            self.dsaButtonDescription.place(relx = 0.35, rely = 0.5, anchor = W)
            self.dsaButton.place(x = 10, y = 10)
            self.dsaButtonFrame.grid(row = i, column = 0, padx = 10, pady = 10)
    
    def showInfo(self, name, window):
        self.window = window
        self.name = name
        self.page.clear_page()
        # Call the clear page method from the page class to remove all the frames
        
        self.revision_page = revision_page(self.window, self.name, "revision")
        self.revision_page.pack(expand=True, fill="both")
        
class base_page(CTkFrame):
    def __init__(self, root, state):
        super().__init__(root)
        self.root = root
        self.state = state
        self.DSA = None
        
        # header
        self.header = header(self, self.state, self.DSA, self.root)
        
        # footer
        self.footer = footer(self, height=100)
        
        # main frame
        self.main_frame = CTkFrame(self, corner_radius=0)
        
    def clear_page(self):
        for child in self.root.winfo_children():
            child.forget()

# the reason for the base class is because packing the frames requires a specific order
# I decided to use pack instead of grid because of the dynamic layout being better

class quiz_page(base_page):
    def __init__(self, root, state, DSA): # error ocurred where i done __init instead of __init__ so a defualt frame was packed instead
        super().__init__(root, state)
        
        self.root.minsize(1080,920)
        
        self.root.title("Quiz!")
        
        # override the header with the new DSA
        self.header = header(self, self.state, self.DSA, self.root)
        self.header.pack(fill="x",side="top")
        self.main_frame.pack(expand=True, fill="both", side="top", anchor="center")
        
        self.setQuiz(DSA)
        
        # footer
        self.footer = footer(self.root, height=100)
        self.footer.pack(fill="x", side="bottom")
    
    def setQuiz(self, DSA):
        Quiz.main(self.main_frame, DSA)

class visualiser_page(base_page):
    def __init__(self, root, DSA, state):
        super().__init__(root, state)
        self.DSA = DSA # key for hashDataRetrieve
        
        self.root.minsize(1080,1080)
        self.root.title("Visualiser: " + self.DSA)
        
        # override the header with the new DSA
        self.header = header(self, self.state, self.DSA, self.root)
        self.header.pack(fill="x",side="top")
        self.main_frame.pack(expand=True, fill="both", side="top")

        self.setVis()
        
        # footer
        self.footer = footer(self.root, height=75)
        self.footer.pack(fill="x", side="bottom")
    
    def setVis(self):
        try:
            DSAs_dict[self.DSA].main(self.main_frame) # pass the root as a parameter
        except:
            DSAs_dict[self.DSA].main(self.main_frame, self.root)

class revision_page(base_page):
    def __init__(self, root, DSA, state):
        super().__init__(root, state)
        self.DSA = DSA # key for hashDataRetrieve
        
        self.root.minsize(1080,920)
        self.root.title("Revision: " + self.DSA)
        
        # override the header with the new DSA
        self.header = header(self, self.state, self.DSA, self.root)
        self.header.pack(fill="x",side="top")
        self.main_frame.pack(expand=True, fill="both", side="top")
        
        self.ScrollFrame = CTkScrollableFrame(self.main_frame, fg_color = "transparent")
        self.ScrollFrame.pack(expand = True, fill = "both")
        
        # footer
        self.footer = footer(self.ScrollFrame, height=100)
        self.footer.pack(fill="x", side="bottom")

        self.title = CTkLabel(self.ScrollFrame, text="Revision: " + hashDataRetrieve(self.DSA)['name'], font=("Arial Black", 26, "bold"), width=30, height=10, fg_color="transparent", corner_radius=6)
        self.info = CTkFrame(self.ScrollFrame, width=750, height=800, corner_radius = 20, fg_color = "gray")
        self.info.grid_columnconfigure(0, weight=1)
        self.info.grid_columnconfigure(1, weight=4)
        
        self.content = hashDataRetrieve(self.DSA)['content']
        self.setContent(self.content)
                    
        self.title.pack(expand = True, padx = 10, pady = 20)
        self.info.pack(expand = True, padx = 10, pady = 30)
        
    def setContent(self, content):
        for i, datum in enumerate(content):
            self.datum_bold = CTkLabel(self.info, text=datum[0], font = ("Arial Black", 18, "bold"), wraplength=250)
            self.datum_normal = CTkLabel(self.info, text=datum[1], font = ("Arial", 18), wraplength=500)
                        
            self.datum_bold.grid(row = i, column = 0, padx = 10, pady = 15)
            self.datum_normal.grid(row = i, column = 1, padx = 10, pady = 15)

class main_page(base_page):
    def __init__(self, root, state):
        super().__init__(root, state)
        self.root.title("Main Page")
        self.root.minsize(1080,920)

        self.header.pack(fill="x",side="top")
        self.main_frame.pack(expand=True, fill="both", side="top")
        self.footer.pack(fill="x", side="bottom")

        # search and dsaframe
        self.search_frame = search_frame(self.main_frame, self, self.root) # Format: master, page, window
        self.search_frame.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.dsa_frame = dsa_frame(self.main_frame, self, self.root)
        self.dsa_frame.place(relx = 0.5, rely = 0.55, anchor=CENTER)
    
class App(CTk):
    def __init__(self):
        super().__init__()
        self.minsize(1080,920)
        set_default_color_theme("dark-blue.json")
                
        # window
        self.geometry("1080x920")

        # main-menu
        self.main_page = main_page(self, "main")
        self.main_page.pack(expand=True, fill="both")

        self.main_page.appearance_mode = False # initially dark
    
# the name acts as the key
# [:-1] is needed for the '\n' for the end of each line
def hashDataRetrieve(key):
    
    # hash function
    
    val = 1
    count = 1
    flip = True
    
    for letter in key:
        if flip == True:
            val *= (ord(letter)/1.5)
        else:
            val += (ord(letter)*2)
        flip = not flip
        count *= 2
    
    remainder = val % 3
    val = math.sqrt(val)
    val = round(val/count)
    val = str(val)
    
    hash_val = ""
    
    
    for i in val:
        hash_val += i
    hash_val = round(int(hash_val) * remainder)
    
    # ast.literal_eval() turns the string into a dictionary if it's in the correct form
    while ast.literal_eval(database_list[hash_val][:-1])["name"] != key:
        hash_val += 1
        
    return ast.literal_eval(database_list[hash_val][:-1])
    
database=open("DSA Types Database.txt", "r", encoding="utf-8")
database_list = database.readlines()

DSAs_array = ['Array', 'Queue', 'Stack', 'Graph', 'Tree', 'Linked List', 'Sorting', 'Searching']
DSAs_dict = {
    'Array': array_vis,
    'Queue': queue_vis,
    'Stack': stack_vis,
    'Graph': graph_vis,
    'Tree': tree_vis,
    'Linked List': linked_list_vis,
    'Sorting': sorting_vis,
    'Searching': searching_vis
    }
types = ["Normal", "Queue", "Stack", "Static", "Dynamic", "Priority", "Circular", "Binary", "Bubble", "Insertion", "Merge", "Linear", "Binary"]
categories = ["Static", "Linear Data Structures", "Dynamic", "Queue", "Non-Linear Data Structures", "DFS", "BFS", "Pre-order", "In-order", "Post-order", "Sorting", "Searching"]

if __name__ == "__main__":
    app = App()
    app.mainloop()

    set_appearance_mode("dark")