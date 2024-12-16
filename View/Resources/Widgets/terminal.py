import tkinter as tk
from tkinter import scrolledtext

class Terminal(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Enlarged scroll bar
        self.vsb = self.vbar 
        self.vsb.config(width=20)
