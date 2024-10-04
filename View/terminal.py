import tkinter as tk
from tkinter import scrolledtext

class Terminal(scrolledtext.ScrolledText):
    def __init__(self, parentFrame) -> None:
        scrolledtext.ScrolledText.__init__(self, parentFrame, height=5, wrap="word", bg="lightgrey", fg="black")
        self.pack(side=tk.BOTTOM, fill=tk.X)