# Hash table frame (inherits the shared playback base class in playback_frame.py):  Lines 18 - 152
# Control frame (speed slider):   Lines 154 - 164
# Message frame:                  Lines 167 - 181
# main():                         Lines 184 - 202

# Insert / search / delete steps:  hash_table_steps.insert_steps / search_steps / delete_steps

import random
import customtkinter as ctk

from playback_frame import PlaybackFrame
import hash_table_steps

TABLE_SIZE = 10      # Number of slots drawn
MAX_KEY = 99         # Keys are 0 – MAX_KEY


class HashTableFrame(PlaybackFrame):
    """One hash table with Insert / Search buttons; the steps are animated with the playback controls."""
    show_index_labels = True

    def __init__(self, master, speed_var, message_box):
        super().__init__(master, speed_var, message_box)

        self.table = [None] * TABLE_SIZE

        self.controls = ctk.CTkFrame(master=self, fg_color="transparent")
        self.controls.pack(pady=5)

        self.value_entry = ctk.CTkEntry(master=self.controls, placeholder_text=f"Key (0-{MAX_KEY})", width=110)
        self.value_entry.pack(side="left", padx=5)

        self.insert_button = ctk.CTkButton(master=self.controls, text="Insert", width=80, command=lambda: self.start_operation("insert"))
        self.insert_button.pack(side="left", padx=5)

        self.search_button = ctk.CTkButton(master=self.controls, text="Search", width=80, command=lambda: self.start_operation("search"))
        self.search_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(master=self.controls, text="Delete", width=80, command=lambda: self.start_operation("delete"))
        self.delete_button.pack(side="left", padx=5)

        self.generate_button = ctk.CTkButton(master=self.controls, text="Generate Random", width=130, command=self.generate_random_table)
        self.generate_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(master=self.controls, text="Clear", width=70, command=self.clear_table)
        self.clear_button.pack(side="left", padx=5)

        self.title.configure(text="Hash Table (linear probing)")
        self.draw_table(self.table, [hash_table_steps.EMPTY] * TABLE_SIZE)

    # --- PlaybackFrame hooks ---------------------------------------------------

    def unpack_state(self, state): # Hash table states are [table, colours, text]
        return state[0], state[1], state[2]

    def show_state(self, index):
        table, colours, text = self.unpack_state(self.states[index])
        self.message_box.change_message(text)
        self.draw_table(table, colours)

    def cancel_animation(self):
        super().cancel_animation()
        # The canvas was cleared; show the current table so it never looks empty
        self.draw_table(self.table, [hash_table_steps.EMPTY] * TABLE_SIZE)

    # --- drawing --------------------------------------------------------------

    def draw_table(self, table, colours):
        """Draw the slots as a row of boxes: the key inside, the index underneath."""
        self.canvas.delete("all")
        c_width = 580
        slot_width = c_width / len(table)
        box = min(slot_width - 6, 60)
        top = 140
        offset = 10 + (c_width - slot_width * len(table)) / 2

        for i, key in enumerate(table):
            x0 = offset + i * slot_width + (slot_width - box) / 2
            x1 = x0 + box
            if colours[i] != hash_table_steps.EMPTY:
                fill = colours[i]
            elif key is None:
                fill = "white"
            elif key is hash_table_steps.DELETED:
                fill = "dimgray"
            else:
                fill = "lightgrey"
            self.canvas.create_rectangle(x0, top, x1, top + box, fill=fill, outline="black", width=2)
            if key is not None:
                text_colour = "white" if fill in ("black", "dimgray") else "black"
                self.canvas.create_text((x0 + x1) / 2, top + box / 2, text=str(key), fill=text_colour, font=("Arial", 14, "bold"))
            self.canvas.create_text((x0 + x1) / 2, top + box + 14, text=str(i), fill="black", font=("Arial", 10))

        self.canvas.create_text(300, 60, text=f"hash(key) = key mod {len(table)}", fill="black", font=("Arial", 14))
        used = sum(1 for slot in table if slot is not None)
        deleted = sum(1 for slot in table if slot is hash_table_steps.DELETED)
        text = f"Load factor: {used}/{len(table)} = {hash_table_steps.load_factor(table):.2f}"
        if deleted:
            text += f"   (includes {deleted} deleted marker{'s' if deleted != 1 else ''}, X)"
        self.canvas.create_text(300, 250, text=text, fill="black", font=("Arial", 12))
        self.update_idletasks()

    # --- actions --------------------------------------------------------------

    def read_key(self):
        """The key typed in the entry as an int, or None (with a message) if invalid."""
        value = self.value_entry.get().strip()
        try:
            key = int(value)
        except ValueError:
            self.message_box.change_message(f"Please enter a whole number between 0 and {MAX_KEY}.")
            return None
        if not 0 <= key <= MAX_KEY:
            self.message_box.change_message(f"Keys must be between 0 and {MAX_KEY}.")
            return None
        return key

    def start_operation(self, operation):
        key = self.read_key()
        if key is None:
            return

        self.reset_animation() # Stop any ongoing animation and clear the previous steps

        if operation == "insert":
            steps = hash_table_steps.insert_steps(self.table, key) # Modifies self.table
        elif operation == "delete":
            steps = hash_table_steps.delete_steps(self.table, key) # Leaves a tombstone in self.table
        else:
            steps = hash_table_steps.search_steps(self.table, key)

        self.load_states(steps)
        self.begin_animation()

    def generate_random_table(self):
        """Fill about half the slots with random keys (inserted with linear probing)."""
        self.reset_animation()
        self.table = [None] * TABLE_SIZE
        for key in random.sample(range(MAX_KEY + 1), TABLE_SIZE // 2):
            hash_table_steps.insert_steps(self.table, key)
        self.draw_table(self.table, [hash_table_steps.EMPTY] * TABLE_SIZE)
        self.message_box.change_message("Random table generated: " + ", ".join(str(k) for k in self.table if k is not None))

    def clear_table(self):
        self.reset_animation()
        self.table = [None] * TABLE_SIZE
        self.playback_slider.configure(state="disabled")
        for button in self.edit_buttons:
            button.configure(state="disabled")
        self.draw_table(self.table, [hash_table_steps.EMPTY] * TABLE_SIZE)
        self.message_box.change_message("Table cleared.")


class controlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=800, height=100)
        self.propagate(False)

        self.speed_var = ctk.DoubleVar(value=600)  # Speed variable in milliseconds
        self.speed_label = ctk.CTkLabel(master=self, text="Speed Control (ms)")
        self.speed_label.pack(side="left", padx=10, pady=10)

        self.speed_slider = ctk.CTkSlider(master=self, from_=10, to=1500, variable=self.speed_var)
        self.speed_slider.pack(side="left", padx=10, pady=10, fill="x", expand=True)


class messageFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, width=800, height=150)
        self.title = title

        self.propagate(False) # Completely static, does not change

        self.title_label = ctk.CTkLabel(master=self, font=("Arial", 22, "bold"), text=self.title)
        self.title_label.pack(padx=10, pady=10)

        self.message_box = ctk.CTkLabel(master=self, font=("Arial", 14), text="", wraplength=700)
        self.message_box.pack(expand=True)

    def change_message(self, text):
        self.message_box.configure(text=text)


def main(master, window):
    window.geometry("1080x1080")
    window.minsize(1080, 1080)
    master.configure(fg_color="gray")

    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)

    control_frame = controlFrame(master=master)
    control_frame.grid(row=1, column=0, padx=20, pady=10)

    message_box = messageFrame(master=master, title="Hash Table Log")
    message_box.grid(row=2, column=0, padx=20, pady=10)

    table_frame = HashTableFrame(master=master, speed_var=control_frame.speed_var, message_box=message_box)
    table_frame.grid(row=0, column=0, padx=20, pady=10)

    message_box.change_message(f"Type a key (0-{MAX_KEY}) then Insert, Search or Delete. hash(key) = key mod {TABLE_SIZE}; collisions are resolved by linear probing.")
    return table_frame
