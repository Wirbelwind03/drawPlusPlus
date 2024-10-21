import tkinter as tk

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)