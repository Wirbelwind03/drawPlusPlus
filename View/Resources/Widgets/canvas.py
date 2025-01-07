import tkinter as tk

from View.theme import Theme

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def refresh(self, settings):
        self.configure(highlightbackground=Theme.HighLightBackgroundColor(settings))
