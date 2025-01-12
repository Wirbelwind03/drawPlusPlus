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

        self.refresh_widgets_event = None  # Callback attribute

    def set_event_refresh_widgets(self, event: callable) -> None:
        """
        Set the event for refreshing the widgets

        Parameters
        -----------
        event : callable
            The event to set for refreshing the widgets
        """
        self.refresh_widgets_event = event

    def executeCode(self):
        """
        Execute the code inside the textEditor
        """
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
            tokens, errors = tokenizer.tokenize(code)

            parser = DrawScriptParser(tokens)
            ast_nodes, parse_errors = parser.parse()

            # -- If the parser has error, show them
            if parse_errors:
                print("=== Parsing errors detected ===")
                for err in parse_errors:
                    # Each error is a dict: {"message": str(e), "line": line}
                    ligne = err["line"]
                    message = err["message"]
                    self.terminal.text_widget.insert(tk.END, f"Ligne {ligne}: {message}\n")
                    print(f"Ligne {ligne}: {message}")

                    # Put the error line in red
                    self.highlight_error(message, ligne)
                print("Impossible to continue with the semantic analysis.")
                raise Exception
            else:
                print("No parsing errors.")
                # Do the semantic analysis
                analyzer = SemanticAnalyzer()
                semantic_errors = analyzer.analyze(ast_nodes)

                if semantic_errors:
                    print("=== Semantic errors detected ===")
                    for err in semantic_errors:
                        self.terminal.text_widget.insert(tk.END, err)
                        print(err)
                    print("Cancel generation of code C")
                    raise Exception
                else:
                    print("No semantic errors, generating code C")
                    interpreter = DrawScriptDeserializerC(ast_nodes, self.CC)
                    interpreter.write_c()

                    # Indicate successful execution in the terminal
                    self.terminal.text_widget.insert(tk.END, "Compilation successful !\n")

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
                    Utils.RemoveFilesInDirectory(output_folder, ".gitignore")

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

            # Highlight the line where the error occurred in the text editor
            #self.highlight_error(e, line_number)

        self.terminal.text_widget.config(state=tk.DISABLED)  # Disable editing again

    # Fonction pour souligner la ligne contenant une erreur
    def highlight_error(self, error, line_number):
        error_message = str(error)
        # On extrait le numéro de ligne de l'erreur
        self.textEditor.openedTab.tag_add("error", f"{line_number}.0", f"{line_number}.end")
        self.textEditor.openedTab.tag_config("error", underlinefg="red", underline=True)

    def load_file(self):
        """
        Event when the user click on load on the menu bar
        """
        # Open a file dialog to ask where the user want to load the file
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                # Open the file in a new tab
                self.textEditor.add_editor_tab(Path(file_path).stem)
                # Select the open tab
                self.textEditor.notebook.select(len(self.textEditor.editor_tabs) - 1)
                # Write the text in the new tab
                self.textEditor.openedTab.insert(tk.END, file.read())
                # Refresh the widgets so they take the settings font and color
                if self.refresh_widgets_event:
                    self.refresh_widgets_event()

    def save_file(self) -> None:
        """
        Event when the user click on save on the menu bar
        """
        # Open a file dialog to ask where the user want to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                # Open a new tab in the textEditor
                file.write(self.textEditor.openedTab.get("1.0", tk.END))

    def create_new_file(self):
        # "+ 1" because the new tab has not been added yet
        self.textEditor.add_editor_tab(f'Fenêtre {len(self.textEditor.editor_tabs) + 1}')
        # "- 1" because the new tab has been added
         # Select the new tab
        self.textEditor.notebook.select(len(self.textEditor.editor_tabs) - 1)
        # Refresh the widgets so they take the settings font and color
        if self.refresh_widgets_event:
            self.refresh_widgets_event()

