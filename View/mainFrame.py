import tkinter as tk

from DrawLibrary.Graphics.canvasImage import CanvasImage

from .Resources.Widgets.terminal import *
from .Resources.Widgets.multiTextEditor import *
from .Resources.Widgets.toolBar import *
from .Resources.Widgets.mainBar import *


class MainFrame(tk.Frame):
    """
    A class to represent the Main Frame widget, the frame that contains all the widget

    Attributes
    -----------
    mainBar : MainBar
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
        super().__init__(*args, **kwargs)
        
        # Use grid for the main frame layout
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Add menu bar (this doesn't use grid or pack, it's set on master)
        self.menuBar = tk.Menu()
        self.master.config(menu=self.menuBar)

        # Configure rows and columns for grid layout in MainFrame
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) 

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # Menu Bar at the top
        self.mainBar = MainBar(self, bg="#636363") # Same background color as for window.py
        self.mainBar.grid(row=0, column=1, sticky="new", padx=10, pady=10)  # ToolBar spans across both columns

        # Create and grid the widgets
        self.toolBar = ToolBar(self, bg="#636363") # Same background color as for window.py
        self.toolBar.grid(row=1, column=1, sticky="new", padx=10, pady=10)  # ToolBar spans across both columns

        # TextEditor on the left side, expands vertically
        self.textEditor = MultiTextEditor(self)
        self.textEditor.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10, pady=10)  # Left side, expands in all directions

        # Canvas on the right side, expands vertically and horizontally
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)  # Right side, expands in all directions
        
        # Terminal at the bottom
        self.terminal = Terminal(self, height=10, wrap="word", bg="lightgrey", fg="black")
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)