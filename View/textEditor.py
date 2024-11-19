import tkinter as tk

from tkinter import scrolledtext

from .Resources.Widgets.customText import CustomText
from .Resources.Widgets.textLineNumbers import TextLineNumbers


class TextEditor(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #self.text = CustomText(self)
        self.text = tk.Text(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        # self.linenumbers = TextLineNumbers(self, width=30)
        # self.linenumbers.attach(self.text)

        # Configure the grid of the Text Editor widget
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0) 

        self.vsb.grid(row=0, column=1, sticky="ns")  # Fill vertically
        # self.linenumbers.grid(row=0, column=0, sticky="ns") 
        self.text.grid(row=0, column=0, sticky="nsew")  # Fill both horizontally and vertically


        # self.text.bind("<<Change>>", self._on_change)
        # self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

    # Fonction pour souligner la ligne contenant une erreur
    def highlight_error(self, error, line_number):
        error_message = str(error)
        # On extrait le numéro de ligne de l'erreur
        self.text.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.text.tag_config("error", background="red")  # Configurer le surlignement