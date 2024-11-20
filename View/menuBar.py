import tkinter as tk
from tkinter import filedialog

class MenuBar(tk.Menu):
    """
    A class to represent the Menu Bar
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parentFrame = self.master

        menuFile = tk.Menu(self, tearoff=0)
        # Add button "File" in the menu bar
        self.add_cascade(label="File", menu=menuFile)
        # Ajoute les button dans le menu déroulant
        menuFile.add_command(label="New", command=self.create_new_file)
        menuFile.add_command(label="Open", command=self.load_file)
        menuFile.add_command(label="Save", command=self.save_file)
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
        menuExecute.add_command(label="Compile C", command=self.execute_code)

    # Fonction pour compiler et exécuter les instructions
    def execute_code(self):
        # Retrieve the entire text content from the text editor starting at line 1, character 0, to the end
        code = self.parentFrame.textEditor.text.get("1.0", tk.END)

        # Clear the terminal widget before executing the code
        self.parentFrame.terminal.delete("1.0", tk.END)

        # Remove all previously highlighted "error" tags from the text editor
        self.parentFrame.textEditor.text.tag_remove("error", "1.0", tk.END)

        try:
            # Clear all elements on the canvas to remove any previous drawings
            self.parentFrame.canvas.delete("all")

            # Loop through each line of code, keeping track of the line number
            for line_number, line in enumerate(code.splitlines(), start=1):
                # Parse and execute each line, passing the line content and its number to the compiler
                self.parentFrame.compiler.parse_instruction(line, line_number)

            # Indicate successful execution in the terminal
            self.parentFrame.terminal.insert(tk.END, "Exécution réussie !\n")

        except Exception as e:
            # Display the error message in the terminal
            self.parentFrame.terminal.insert(tk.END, str(e) + "\n")

            # Highlight the line where the error occurred in the text editor
            self.parentFrame.textEditor.highlight_error(e, line_number)


    # Fonction pour charger un fichier
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.parentFrame.textEditor.delete("1.0", tk.END)
                self.parentFrame.textEditor.insert(tk.END, file.read())

    # Fonction pour sauvegarder le fichier
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.parentFrame.textEditor.get("1.0", tk.END))

    # Fonction de création de fichier (pour l'instant vide)
    def create_new_file(self):
        self.parentFrame.textEditor.delete("1.0", tk.END)

        
                