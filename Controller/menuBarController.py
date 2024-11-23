import tkinter as tk

class MenuBarController:
    def __init__(self, view, model) -> None:
        self.view = view

        menuFile = tk.Menu(self, tearoff=0)
        # Add button "File" in the menu bar
        self.view.add_cascade(label="File", menu=menuFile)
        # Ajoute les button dans le menu déroulant
        menuFile.add_command(label="New")
        menuFile.add_command(label="Open")
        menuFile.add_command(label="Save")
        # Add a separator
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.view.master.quit)  # Option Quitter

        menuEdit = tk.Menu(self, tearoff=0)
        # Add button "Edit" in the menu bar
        self.view.add_cascade(label="Edit", menu=menuEdit)
        menuEdit.add_command(label="Cut")
        menuEdit.add_command(label="Copy")
        menuEdit.add_command(label="Paste")

        menuExecute = tk.Menu(self, tearoff=0)
        # Add button "Execution" in the mnu bar
        self.view.add_cascade(label="Execution", menu=menuExecute)
        menuExecute.add_command(label="Execute")
        menuExecute.add_command(label="Compile C")