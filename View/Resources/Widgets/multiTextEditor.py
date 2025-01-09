import tkinter as tk
from tkinter import ttk
import os
import json

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a Notebook Widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Initialize variables
        self.last_modified_time = None
        self.json_file = "View/Resources/Widgets/gear.json"

        # Add 18 tabs with text editors
        self.editor_tabs = [] 
        for i in range(1,19):
            self.add_editor_tab(f"Fenêtre {i}")

        # Check if gear.json file is modified every 500ms
        self.check_for_changes()

    # Returns the last modification date of the JSON file or None if the file does not exist.
    def get_file_modification_time(self):
        if os.path.exists(self.json_file):
            return os.path.getmtime(self.json_file)
        return None
    
    # Function to load data from json file
    def load_settings(self):
        # Check if the file has not been manually modified and if so we close the IDE with an error message
        if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
            with open(self.json_file, "r") as file:
                settings = json.load(file)
            return settings
        else:
            print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
            exit(1)

    # Create a new text editor "tab"
    def add_editor_tab(self, title):

        # Create a frame for the new tab
        frame = tk.Frame(self.notebook)

        # Use grid for the text editor layout
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Create a vertical scrollbar
        text = tk.Text(frame, wrap="word")
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=20)
        text.configure(yscrollcommand=vsb.set)

        # Dynamically apply style to any newly typed text
        def on_key(event):
            text.tag_add("custom_font", "1.0", "end")

        # Bind on_key() to the user's keyboard
        text.bind("<KeyRelease>", on_key)  

        # Block automatic resizing related to text
        text.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.editor_tabs.append(text)

        # Add tab to Notebook
        self.notebook.add(frame, text=title)

    def check_for_changes(self):
        # Check if the file exists and if the modification date has changed
        if os.path.exists(self.json_file):
            current_modified_time = os.path.getmtime(self.json_file)
            if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time

                # If so, the new size, font and colors are applied to all text editor "tabs".
                settings = self.load_settings()
                dark_mode = settings.get("dark_mode", False)
                self.background_color = "black" if dark_mode else "white"
                self.text_color = "white" if dark_mode else "black"
                self.font = settings.get("font", "Helvetica")
                self.font_size = settings.get("font_size", 24)

                for editor in self.editor_tabs:
                    editor.config(bg=self.background_color,fg=self.text_color, insertbackground=self.text_color)
                    editor.tag_configure("custom_font", font=(self.font, self.font_size))  


        # Schedule next check in 500ms
        self.after(500, self.check_for_changes)