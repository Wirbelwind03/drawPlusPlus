import tkinter as tk

from Controller.drawScriptParser import DrawScriptParser

from .menuBar import *
from .textEditor import *
from .terminal import *
from .canvas import *


class MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)

        self.menuBar = MenuBar(self)
        self.master.config(menu=self.menuBar)

        self.canvas = Canvas(self, width=800, height=600)
        self.textEditor = TextEditor(self, width=50, bg="white")
        self.terminal = Terminal(self, height=10, wrap="word", bg="lightgrey", fg="black")

        self.compiler = DrawScriptParser(self.canvas)