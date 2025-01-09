import tkinter as tk
import subprocess
import os
from tkinter import filedialog
from pathlib import Path

from Controller.canvasController import CanvasController

from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.utils import Utils

from DrawScript.Core.drawScriptTokenizer import DrawScriptTokenizer
from DrawScript.Core.drawScriptParser import DrawScriptParser
from DrawScript.Core.drawScriptSemanticAnalyzer import SemanticAnalyzer
from DrawScript.Core.drawScriptDeserializerC import DrawScriptDeserializerC

from View.Resources.Widgets.terminal import Terminal
from View.Resources.Widgets.multiTextEditor import MultiTextEditor

class ScriptEditorController:
    """
    The Script Editor Controller handle the drawScript and its compilation.
    When the drawScript is compiled, it's communicate to the canvasController, to draw the shapes given by the drawScript
    This controller also handle everything tied to file operations (open, save, edit) since the file is modified in the text editor.
    If the drawScript fail to compile, this controller communicate to the terminal to show the errors.

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

        self.refresh_widgets_event = None  # Callback attribute

    def set_event_refresh_widgets(self, event):
        self.refresh_widgets_event = event

    def executeCode(self):
        # Retrieve the entire text content from the text editor starting at line 1, character 0, to the end
        code = self.textEditor.openedTab.get("1.0", tk.END)

        # Temporarily enable editing
        self.terminal.text_widget.config(state=tk.NORMAL)  

        # Clear the terminal widget before executing the code
        self.terminal.text_widget.delete("1.0", tk.END)

        # Remove all previously highlighted "error" tags from the text editor
        self.textEditor.openedTab.tag_remove("error", "1.0", tk.END)

        try:
            # Clear all elements on the canvas to remove any previous drawings
            self.CC.deleteAll()

            tokenizer = DrawScriptTokenizer()
            tokens, tokenize_errors = tokenizer.tokenize(code)

            if tokenize_errors:
                print("=== Tokenizer errors detected ===")

            parser = DrawScriptParser(tokens)
            ast_nodes, parse_errors = parser.parse()

            # -- Vérification: si le parseur a retourné des erreurs, on les affiche:
            if parse_errors:
                print("=== Erreurs de parsing détectées ===")
                for err in parse_errors:
                    # Chaque err est un dict: {"message": str(e), "line": line}
                    self.terminal.text_widget.insert(tk.END, f"Ligne {err['line']}: {err['message']}\n")
                    print(f"Ligne {err['line']}: {err['message']}")
                print("Impossible de poursuivre l'analyse sémantique.")
                raise Exception # Stop the code
            
            print("Aucune erreur de parsing.")
            # Si pas d'erreur de parsing, on effectue l'analyse sémantique
            analyzer = SemanticAnalyzer()
            semantic_errors = analyzer.analyze(ast_nodes)

            if semantic_errors:
                print("=== Semantic errors detected ===")
                # Highlight the line where the error occurred in the text editor
                #self.highlight_error(line_number)
                for err in semantic_errors:
                    self.terminal.text_widget.insert(tk.END, err)
                    print(err)
                print("Annulation de la génération du code C.")
                raise Exception # Stop the code

            print("Aucune erreur sémantique, génération du code C en cours.")
            interpreter = DrawScriptDeserializerC(ast_nodes, self.CC)
            interpreter.write_c()

            # Indicate successful execution in the terminal
            self.terminal.text_widget.insert(tk.END, "Exécution réussie !\n")

            # Get the directory where the code is ran
            current_directory = os.getcwd()

                    gcc_command = [
                        "gcc",
                        f"-I{current_directory}/DrawLibrary/C/SDL2/src/include",
                        f"-I{current_directory}/DrawLibrary/C/SDL2_gfx",
                        f"-I{current_directory}/DrawLibrary/C/Utils",
                        f"{current_directory}/DrawLibrary/C/Utils/shapes.c",
                        f"{current_directory}/DrawLibrary/C/Utils/cursor.c",
                        f"{current_directory}/DrawLibrary/C/Utils/utils.c",
                        f"{current_directory}/main.c",
                        f"{current_directory}/DrawLibrary/C/SDL2_gfx/SDL2_gfxPrimitives.c",
                        f"{current_directory}/DrawLibrary/C/SDL2_gfx/SDL2_rotozoom.c",
                        f"-L{current_directory}/DrawLibrary/C/SDL2/src/lib",
                        "-lmingw32",
                        "-lSDL2main",
                        "-lSDL2",
                        f"-o{current_directory}/DrawLibrary/C/SDL2/main.exe",
                    ]

                    # Compile the C code
                    try:
                        subprocess.run(gcc_command, check=True)
                        print("Build successful!")
                    except subprocess.CalledProcessError as e:
                        print(f"Build failed: {e}")

                    output_folder = f'{current_directory}/Data/Outputs'
                    for filename in os.listdir(output_folder):
                        file_path = os.path.join(output_folder, filename)
                        if os.path.isfile(file_path) and filename != ".gitignore":
                            os.remove(file_path)

                    # Run the C code
                    try:
                        subprocess.run(f"{current_directory}/DrawLibrary/C/SDL2/main.exe", check=True)  # This will run the exe and wait for it to finish
                        print(f"Successfully launched {current_directory}/DrawLibrary/C/SDL2/main.exe")
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to launch {current_directory}/DrawLibrary/C/SDL2/main.exe: {e}")

                    with open(f'{current_directory}/Data/Outputs/drawing_positions.txt', "r") as file:
                        lines = file.readlines()

                    for i in range(0, len(lines)):
                        line = lines[i]
                        image = CanvasImage.fromPath(f'{output_folder}/drawing_{i + 1}.bmp')
                        image.removeWhiteBackground()
                        x, y = line.strip().split(',')
                        self.CC.drawImage(image, int(x), int(y))

        except Exception as e:
            # Display the error message in the terminal
            self.terminal.text_widget.insert(tk.END, str(e) + "\n")

        self.terminal.text_widget.config(state=tk.DISABLED)  # Disable editing again

    def highlight_error(self, line_number):
        """
            Highlight the first error in the text editor
        """
        # On extrait le numéro de ligne de l'erreur
        self.textEditor.openedTab.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.textEditor.openedTab.tag_config("error", background="red")  # Configurer le surlignement

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.textEditor.add_editor_tab(Path(file_path).stem)
                self.textEditor.notebook.select(len(self.textEditor.editor_tabs) - 1)
                self.textEditor.openedTab.insert(tk.END, file.read())
                if self.refresh_widgets_event:
                    self.refresh_widgets_event()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.textEditor.openedTab.get("1.0", tk.END))

    # Fonction de création de fichier (pour l'instant vide)
    def create_new_file(self):
        # "+ 1" because the new tab has not been added yet
        self.textEditor.add_editor_tab(f'Fenêtre {len(self.textEditor.editor_tabs) + 1}')
        # Select the new tab
        # "- 1" because the new tab has been added
        self.textEditor.notebook.select(len(self.textEditor.editor_tabs) - 1)
        if self.refresh_widgets_event:
            self.refresh_widgets_event()