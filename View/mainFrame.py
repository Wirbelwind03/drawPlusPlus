import tkinter as tk


from Controller.drawScriptParser import DrawScriptParser

from .menuBar import *
from .textEditor import *
from .terminal import *
from .canvas import *


class MainFrame(tk.Frame):
    def __init__(self, window) -> None:
        tk.Frame.__init__(self, window, bg = "#636363")
        self.pack(fill=tk.BOTH, expand=True)

        self.menuBar = MenuBar(self)
        window.config(menu=self.menuBar)

        self.canvas = Canvas(self)
        self.textEditor = TextEditor(self)
        self.terminal = Terminal(self)

        self.compiler = DrawScriptParser(self.canvas)