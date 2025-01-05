import tkinter as tk
from tkinter import filedialog

from Controller.canvasController import CanvasController

from DrawScript.Core.drawScriptTokenizer import DrawScriptTokenizer
from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Core.drawScriptSemanticAnalyzer import SemanticAnalyzer
from DrawScript.Core.drawScriptDeserializerC import DrawScriptDeserializerC

from View.Resources.Widgets.terminal import Terminal
from View.Resources.Widgets.multiTextEditor import MultiTextEditor

class ScriptEditorController:
    """
    Controller that handle the drawScript.
    It also communicate with the canvasController since when the drawScript is read, it's modify the canvas.
    It's where the file operations (open, save, edit) are made,
    but also where the drawScript is going to be written, in the textEditor.
    It's also manage the compilation of the drawScript, and when compiled succesfully, then draw to the canvas
    The terminal is used to show the errors of the code if it fail to compile

    Attributes
    -----------
    textEditor : TextEditor
        The TextEditor where the controller is going to be attached to
        It's where the script is going to be written.
    terminal : Terminal
        The Terminal where the controller is attached to.
        It's used to show the errors of the code in details
        for example the line number, the specific position at the line, etc.
    CC : CanvasController
        The CanvasController manage everything tied to a canvas
        Since this controller erase the canvas when the script is run, it's needed here
    """

    def __init__(self, textEditor: MultiTextEditor, terminal: Terminal, CC: CanvasController) -> None:
        """
            Constructs a new ScriptEditorController.

            Parameters
            -----------
            textEditor : TextEditor
                The TextEditor where the controller is going to be attached to
                It's where the script is going to be written.
            terminal : Terminal
                The Terminal where the controller is attached to.
                It's used to show the errors of the code in details
                for example the line number, the specific position at the line, etc.
            CC : CanvasController
                The CanvasController manage everything tied to a canvas
                Since this controller erase the canvas when the script is run, it's needed here
        """
        self.textEditor = textEditor
        self.terminal = terminal
        self.CC = CC
        self.tokenizer = DrawScriptTokenizer()

    def executeCode(self):
        # Retrieve the entire text content from the text editor starting at line 1, character 0, to the end
        code = self.textEditor.openedTab.get("1.0", tk.END)

        # Clear the terminal widget before executing the code
        self.terminal.delete("1.0", tk.END)

        # Remove all previously highlighted "error" tags from the text editor
        self.textEditor.openedTab.tag_remove("error", "1.0", tk.END)

        try:
            # Clear all elements on the canvas to remove any previous drawings
            self.CC.deleteAll()

            tokenizer = DrawScriptTokenizer()
            tokens, errors = tokenizer.tokenize(code)

            parser = DrawScriptParser(tokens)
            ast_nodes, parse_errors = parser.parse()

            # -- Vérification: si le parseur a retourné des erreurs, on les affiche:
            if parse_errors:
                print("=== Erreurs de parsing détectées ===")
                for err in parse_errors:
                    # Chaque err est un dict: {"message": str(e), "line": line}
                    print(f"Ligne {err['line']}: {err['message']}")
                print("Impossible de poursuivre l'analyse sémantique.")
                raise Exception
            else:
                print("Aucune erreur de parsing.")
                # Si pas d'erreur de parsing, on effectue l'analyse sémantique
                analyzer = SemanticAnalyzer()
                semantic_errors = analyzer.analyze(ast_nodes)

                if semantic_errors:
                    print("=== Erreurs sémantiques détectées ===")
                    for err in semantic_errors:
                        print(err)
                    print("Annulation de la génération du code C.")
                    raise Exception
                else:
                    print("Aucune erreur sémantique, génération du code C en cours.")
                    interpreter = DrawScriptDeserializerC(ast_nodes)
                    interpreter.write_c()

            # Indicate successful execution in the terminal
            self.terminal.insert(tk.END, "Exécution réussie !\n")

        except Exception as e:
            # Display the error message in the terminal
            self.terminal.insert(tk.END, str(e) + "\n")

            # Highlight the line where the error occurred in the text editor
            #self.highlight_error(e, line_number)

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

""" 
    Mettre ici les fonctions liés à l'éditeur de texte et au terminal
    Cela peut etre par exemple des opérations liés au fichiers qui est communiqué à l'éditeur de texte
    Si vous avez besoin de communiqué avec un autre widget (bon il y a pas vraiment de widget pour prendre exemple
    mais genre avec la barre d'outils), il faudra crée un controller et l'ajoutée comme attribut
    C'est le cas avec le CanvasController, lorsqu'on execute le code, cela efface le canvas, et le
    CanvasController gère tout ce qui est par rapport au Canvas.
    Le seul controller à ne pas mettre comme attribut est le MainController
"""