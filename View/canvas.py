import tkinter as tk

class Canvas(tk.Canvas):
    def __init__(self, parentFrame) -> None:
        tk.Canvas.__init__(self, parentFrame, width=800, height=600)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)