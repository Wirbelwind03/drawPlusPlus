import tkinter as tk

from .Resources.Widgets.terminal import Terminal
from .Resources.Widgets.multiTextEditor import MultiTextEditor
from .Resources.Widgets.toolBar import ToolBar
from .Resources.Widgets.mainBar import MainBar
from .Resources.Widgets.canvas import Canvas

from View.theme import Theme

class MainFrame(tk.Frame):
    """
    A class to represent the Main Frame widget, the frame that contains all the widget
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Use grid for the main frame layout
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Add menu bar (this doesn't use grid or pack, it's set on master)
        self.menuBar = tk.Menu(self, background="blue")
        self.master.config(menu=self.menuBar)

        # Configure rows and columns for grid layout in MainFrame
        self.grid_columnconfigure(0, weight=2)  # Plus grand poids pour la colonne de l'éditeur
        self.grid_columnconfigure(1, weight=1)  # Poids plus faible pour la colonne du terminal

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # Menu Bar at the top
        self.mainBar = MainBar(self)  # Background color for the mainBar
        self.mainBar.grid(row=0, column=1, sticky="new", padx=10, pady=10)

        # Create and grid the widgets
        self.toolBar = ToolBar(self)  # Background color for the toolBar
        self.toolBar.grid(row=1, column=1, sticky="new", padx=10, pady=10)

        # TextEditor on the left side, expands vertically
        self.textEditor = MultiTextEditor(self)
        self.textEditor.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10, pady=10)
        
        # Canvas on the right side, expands vertically and horizontally
        self.canvas = Canvas(self, bg="white", highlightthickness=1, width=800, height=600)
        self.canvas.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Terminal at the bottom, non-editable, fixed size, with customized style
        self.terminal = Terminal(self, highlightthickness=1)
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)

    def refresh_widgets(self, settings):
        self.configure(bg=Theme.MainBackgroundColor(settings))
