import tkinter as tk

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)