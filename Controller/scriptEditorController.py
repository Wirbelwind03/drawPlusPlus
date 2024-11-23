import tkinter as tk
from tkinter import filedialog

from Controller.canvasController import CanvasController

from View.Resources.Widgets.terminal import Terminal
from View.Resources.Widgets.textEditor import TextEditor

class ScriptEditorController:
    def __init__(self, textEditor: TextEditor, terminal: Terminal, CC: CanvasController) -> None:
        self.textEditor = textEditor
        self.terminal = terminal
        self.CC = CC

    def executeCode(self):
        # Retrieve the entire text content from the text editor starting at line 1, character 0, to the end
        code = self.textEditor.text.get("1.0", tk.END)

        # Clear the terminal widget before executing the code
        self.terminal.delete("1.0", tk.END)

        # Remove all previously highlighted "error" tags from the text editor
        self.textEditor.text.tag_remove("error", "1.0", tk.END)

        try:
            # Clear all elements on the canvas to remove any previous drawings
            self.CC.deleteAll()

            # Loop through each line of code, keeping track of the line number
            for line_number, line in enumerate(code.splitlines(), start=1):
                # Parse and execute each line, passing the line content and its number to the compiler
                #self.compiler.parse_instruction(line, line_number)
                pass

            # Indicate successful execution in the terminal
            self.terminal.insert(tk.END, "Exécution réussie !\n")

        except Exception as e:
            # Display the error message in the terminal
            self.terminal.insert(tk.END, str(e) + "\n")

            # Highlight the line where the error occurred in the text editor
            self.highlight_error(e, line_number)

    # Fonction pour souligner la ligne contenant une erreur
    def highlight_error(self, error, line_number):
        error_message = str(error)
        # On extrait le numéro de ligne de l'erreur
        self.textEditor.text.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.textEditor.text.tag_config("error", background="red")  # Configurer le surlignement

    # Fonction pour charger un fichier
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.textEditor.text.delete("1.0", tk.END)
                self.textEditor.text.insert(tk.END, file.read())

    # Fonction pour sauvegarder le fichier
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.textEditor.text.get("1.0", tk.END))

    # Fonction de création de fichier (pour l'instant vide)
    def create_new_file(self):
        self.textEditor.text.delete("1.0", tk.END)