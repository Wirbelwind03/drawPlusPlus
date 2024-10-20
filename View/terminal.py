import tkinter as tk
from tkinter import scrolledtext

class Terminal(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs) -> None:
        scrolledtext.ScrolledText.__init__(self, *args, **kwargs)
        self.pack(side=tk.BOTTOM, fill=tk.X)