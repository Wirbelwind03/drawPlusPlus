import tkinter as tk
from tkinter import scrolledtext

from View.theme import Theme

class Terminal(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create the Text widget
        self.text_widget = tk.Text(self, height=10, wrap="word", state=tk.DISABLED)
        
        # Create a vertical scrollbar
        self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.vsb.config(width=20)  # Enlarged scrollbar
        
        # Configure the Text widget to work with the scrollbar
        self.text_widget.configure(yscrollcommand=self.vsb.set)

        # Grid layout for the Text widget and scrollbar
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")

        # Configure grid to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh(self, settings):
        self.text_widget.configure(font=(settings["font"], settings["font_size"]))
        self.text_widget.configure(bg=Theme.BackgroundColor(settings))
        self.text_widget.configure(foreground=Theme.FontColor(settings))
        self.configure(highlightbackground=Theme.HighLightBackgroundColor(settings))