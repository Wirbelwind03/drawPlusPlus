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
        self.add_cascade(label="File", menu=menuFile)
        menuFile.add_command(label="New", command=self.create_new_file)
        menuFile.add_command(label="Open", command=self.load_file)
        menuFile.add_command(label="Save", command=self.save_file)
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=self.parentFrame.quit)  # Option Quitter

        menuEdit = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=menuEdit)
        menuEdit.add_command(label="Cut")
        menuEdit.add_command(label="Copy")
        menuEdit.add_command(label="Paste")

        menuExecute = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Execution", menu=menuExecute)
        menuExecute.add_command(label="Execute")
        menuExecute.add_command(label="Compile C", command=self.execute_code)  # Ajout de la compilation C

    # Fonction pour compiler et exécuter les instructions
    def execute_code(self):
        code = self.parentFrame.textEditor.get("1.0", tk.END)
        self.parentFrame.terminal.delete("1.0", tk.END)  # Effacer le terminal avant d'exécuter
        self.parentFrame.textEditor.tag_remove("error", "1.0", tk.END)  # Effacer les surlignements d'erreur
        try:
            # Effacer le dessin précédent
            self.parentFrame.canvas.delete("all")  # Utilisez canvas pour effacer tout
            for line_number, line in enumerate(code.splitlines(), start=1):
                self.parentFrame.compiler.parse_instruction(line, line_number)  # Passer le numéro de ligne
            self.parentFrame.terminal.insert(tk.END, "Exécution réussie !\n")
        except Exception as e:
            # Afficher l'erreur dans le terminal et souligner la ligne
            self.parentFrame.terminal.insert(tk.END, str(e) + "\n")
            self.parentFrame.textEditor.highlight_error(e)

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

        
                