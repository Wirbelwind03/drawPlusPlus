import tkinter as tk

class MenuBar(tk.Menu):
    """
    A class to represent the Menu Bar
    """

    def __init__(self, menuBarViewModel, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.menuBarViewModel = menuBarViewModel

        self.parentFrame = self.master

        menuFile = tk.Menu(self, tearoff=0)
        # Add button "File" in the menu bar
        self.add_cascade(label="File", menu=menuFile)
        # Ajoute les button dans le menu déroulant
        menuFile.add_command(label="New", command=menuBarViewModel.create_new_file)
        menuFile.add_command(label="Open", command=menuBarViewModel.load_file)
        menuFile.add_command(label="Save", command=menuBarViewModel.save_file)
        # Add a separator
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.parentFrame.quit)  # Option Quitter

        menuEdit = tk.Menu(self, tearoff=0)
        # Add button "Edit" in the menu bar
        self.add_cascade(label="Edit", menu=menuEdit)
        menuEdit.add_command(label="Cut")
        menuEdit.add_command(label="Copy")
        menuEdit.add_command(label="Paste")

        menuExecute = tk.Menu(self, tearoff=0)
        # Add button "Execution" in the mnu bar
        self.add_cascade(label="Execution", menu=menuExecute)
        menuExecute.add_command(label="Execute")
        menuExecute.add_command(label="Compile C", command=menuBarViewModel.execute_code)
        
                