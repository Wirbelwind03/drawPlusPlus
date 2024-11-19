import tkinter as tk

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        self.columnconfigure(0, minsize=120)

        self.rowconfigure(0, minsize=30)
        self.rowconfigure(1, minsize=30)
        self.rowconfigure(2, minsize=30)

        # Tool 1 - Pencil
        pencilButton = tk.Button(self, text="Pencil", height=1, width=12)
        pencilButton.grid(row=0, column=0)

        # Tool 2 - Eraser
        eraserButton = tk.Button(self, text="Eraser", height=1, width=12)
        eraserButton.grid(row=1, column=0)

        # Tool 2 - Eraser
        HighButton = tk.Button(self, text="Highlighter", height=1, width=12)
        HighButton.grid(row=2, column=0)
        #ceci est le desespoir