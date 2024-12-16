import tkinter as tk

class TextEditor(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = tk.Text(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview, width=20)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))

        # Configure the grid of the Text Editor widget
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.vsb.grid(row=0, column=1, sticky="ns")  # Fill vertically
        self.text.grid(row=0, column=0, sticky="nsew")  # Fill both horizontally and vertically