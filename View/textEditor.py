import tkinter as tk
from tkinter import scrolledtext

class TextEditor(scrolledtext.ScrolledText):
    def __init__(self, parentFrame) -> None:
        scrolledtext.ScrolledText.__init__(self, parentFrame, wrap="none", width=50)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Fonction pour souligner la ligne contenant une erreur
    def highlight_error(self, error):
        error_message = str(error)
        # On extrait le numéro de ligne de l'erreur
        line_number = int(error_message.split(" ")[-1])  # On suppose que le numéro de ligne est à la fin
        self.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.tag_config("error", background="yellow")  # Configurer le surlignement