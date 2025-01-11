import tkinter as tk

from Controller.scriptEditorController import ScriptEditorController

class MenuBarController:
    def __init__(self, view: tk.Menu, SEC: ScriptEditorController) -> None:
        self.view = view
        self.SEC = SEC

        menuFile = tk.Menu(self.view, tearoff=0)
        # Add button "File" in the menu bar
        self.view.add_cascade(label="File", menu=menuFile)
        # Ajoute les button dans le menu déroulant
        menuFile.add_command(label="New", command=self.SEC.create_new_file)
        menuFile.add_command(label="Open", command=self.SEC.load_file)
        menuFile.add_command(label="Save", command=self.SEC.save_file)
        # Add a separator
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.view.master.quit)  # Option Quitter

        menuExecute = tk.Menu(self.view, tearoff=0)
        # Add button "Execution" in the mnu bar
        self.view.add_cascade(label="Execution", menu=menuExecute)
        menuExecute.add_command(label="Execute", command=self.SEC.executeCode)