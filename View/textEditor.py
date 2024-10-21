import tkinter as tk

from .Resources.Widgets.customText import CustomText
from .Resources.Widgets.textLineNumbers import TextLineNumbers


class TextEditor(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

    # Fonction pour souligner la ligne contenant une erreur
    def highlight_error(self, error):
        error_message = str(error)
        # On extrait le numéro de ligne de l'erreur
        line_number = int(error_message.split(" ")[-1])  # On suppose que le numéro de ligne est à la fin
        self.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.tag_config("error", background="yellow")  # Configurer le surlignement