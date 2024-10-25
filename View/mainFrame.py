import tkinter as tk

from Controller.drawScriptParser import DrawScriptParser

from .menuBar import *
from .textEditor import *
from .terminal import *
from .canvas import *
from .toolBar import *


class MainFrame(tk.Frame):
    """
    A class to represent the Main Frame widget, the frame that contains all the widget

    Attributes:
    -----------
    menuBar : MenuBar
        Widget at the top of this one that contains operations tied to the file
    textEditor : TextEditor
        Widget where the code is written
    toolBar : ToolBar
        Widget that contains the tools to modify drawings that are on the canvas
    terminal : Terminal
        Widget which show if the code has a error or has been executed succesfully
    canvas : Canvas
        Widget where the drawing take place from the code
    compiler : Compiler
        The program which compile the text editor code to C
    """
    def __init__(self, *args, **kwargs) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        
        # Use grid for the main frame layout
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Add menu bar (this doesn't use grid or pack, it's set on master)
        self.menuBar = MenuBar(self)
        self.master.config(menu=self.menuBar)

        # Configure rows and columns for grid layout in MainFrame
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2) 

        # # Create and grid the widgets
        # self.toolBar = ToolBar(self, bg="black")
        # self.toolBar.grid(row=0, column=0, columnspan=2, sticky="new")  # ToolBar spans across both columns

        # TextEditor on the left side, expands vertically
        self.textEditor = TextEditor(self, bg="white")
        self.textEditor.grid(row=1, column=0, sticky="nsew")  # Left side, expands in all directions

        # Canvas on the right side, expands vertically and horizontally
        self.canvas = Canvas(self, width=800, height=600, bg="white")
        self.canvas.grid(row=1, column=1, rowspan=2, sticky="nsew")  # Right side, expands in all directions
        self.canvas.drawImage("View/circle.jpg")

        # Terminal at the bottom
        self.terminal = Terminal(self, height=10, wrap="word", bg="lightgrey", fg="black")
        self.terminal.grid(row=2, column=0, sticky="sew")

        # Assume you have some parser class initialized here
        self.compiler = DrawScriptParser(self.canvas)