import tkinter as tk

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        self.columnconfigure(0, minsize=120)
        self.columnconfigure(1, minsize=120)
        self.columnconfigure(2, minsize=120)
        self.columnconfigure(3, minsize=120)
        self.columnconfigure(4, minsize=120)

        self.rowconfigure(0, minsize=30)

        label123 = tk.Label(self, text="TOOLS", borderwidth=1, relief=tk.SOLID, width=15)
        label123.grid(row=0, column=0)

        # Tool 1 - Pencil
        pencilButton = tk.Button(self, text="Pencil", height=1, width=12)
        pencilButton.grid(row=1, column=0)

        # Tool 2 - Eraser
        eraserButton = tk.Button(self, text="Eraser", height=1, width=12)
        eraserButton.grid(row=2, column=0)

        # Tool 3 - Color Change
        colorButton = tk.Button(
            self, text="Select Color", height=1, width=12
        )
        colorButton.grid(row=3, column=0)