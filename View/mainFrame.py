import tkinter as tk
import os
import json

from DrawLibrary.Graphics.canvasImage import CanvasImage
from .Resources.Widgets.terminal import Terminal
from .Resources.Widgets.multiTextEditor import MultiTextEditor
from .Resources.Widgets.toolBar import ToolBar
from .Resources.Widgets.mainBar import MainBar

class MainFrame(tk.Frame):
    """
    A class to represent the Main Frame widget, the frame that contains all the widget
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Charger les paramètres une seule fois
        self.settings = self.load_settings()

        # Initialiser la variable pour suivre la date de modification
        self.last_modified_time = None

        # Charger les paramètres initiaux pour le mode sombre et la police
        self.dark_mode = self.settings.get("dark_mode", False)
        self.background_color = "#2E2E2E" if self.dark_mode else "#636363"
        self.background_color_terminal = "black" if self.dark_mode else "white"
        self.text_color = "white" if self.dark_mode else "black"
        self.font = self.settings.get("font", "Helvetica")
        self.font_size = self.settings.get("font_size", 24)

        # Use grid for the main frame layout
        self.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Add menu bar (this doesn't use grid or pack, it's set on master)
        self.menuBar = tk.Menu()
        self.master.config(menu=self.menuBar)

        # Configure rows and columns for grid layout in MainFrame
        self.grid_columnconfigure(0, weight=2)  # Plus grand poids pour la colonne de l'éditeur
        self.grid_columnconfigure(1, weight=1)  # Poids plus faible pour la colonne du terminal

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        # Menu Bar at the top
        self.mainBar = MainBar(self, bg=self.background_color)  # Background color for the mainBar
        self.mainBar.grid(row=0, column=1, sticky="new", padx=10, pady=10)

        # Create and grid the widgets
        self.toolBar = ToolBar(self, bg=self.background_color)  # Background color for the toolBar
        self.toolBar.grid(row=1, column=1, sticky="new", padx=10, pady=10)

        # TextEditor on the left side, expands vertically
        self.textEditor = MultiTextEditor(self)
        self.textEditor.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=10, pady=10)
        
        # Canvas on the right side, expands vertically and horizontally
        self.canvas = tk.Canvas(self, width=800, height=600)
<<<<<<< HEAD
        self.canvas.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Terminal at the bottom, non-editable, fixed size, with customized style
        self.terminal = Terminal(self, height=10, wrap="word", bg=self.background_color_terminal, fg=self.text_color, font=(self.font, self.font_size))
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)

        # Planifier la vérification des changements dans 500 ms
        self.check_for_changes()

    def load_settings(self):
        """
        Fonction pour charger les paramètres depuis le fichier JSON.
        Charge une seule fois les paramètres pour l'ensemble de l'application.
        """
        json_file = "View/Resources/Widgets/gear.json"
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            with open(json_file, "r") as file:
                settings = json.load(file)
            return settings
        else:
            print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
            exit(1)

    def check_for_changes(self):
        json_file = "View/Resources/Widgets/gear.json"

        # Vérifier si le fichier existe et si la date de modification a changé
        if os.path.exists(json_file):
            current_modified_time = os.path.getmtime(json_file)

            if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time

                # Recharger les paramètres et mettre à jour la couleur de fond si nécessaire
                new_settings = self.load_settings()
                new_dark_mode = new_settings.get("dark_mode", False)

                if new_dark_mode != self.dark_mode:
                    self.dark_mode = new_dark_mode
                    self.background_color = "#2E2E2E" if self.dark_mode else "#636363"
                    self.background_color_terminal = "black" if self.dark_mode else "white"
                    self.text_color = "white" if self.dark_mode else "black"
                    self.font = new_settings.get("font", "Helvetica")
                    self.font_size = new_settings.get("font_size", 24)

                    # Mettre à jour les couleurs des widgets
                    self.config(bg=self.background_color)
                    self.mainBar.config(bg=self.background_color)
                    self.toolBar.config(bg=self.background_color)
                    self.menuBar.config(bg=self.background_color)
                    self.terminal.config(bg=self.background_color_terminal, fg=self.text_color, font=(self.font, self.font_size))

        # Planifier la vérification suivante dans 500 ms
        self.after(500, self.check_for_changes)
=======
        self.canvas.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)  # Right side, expands in all directions
        
        # Terminal at the bottom
        self.terminal = Terminal(self)
<<<<<<< HEAD
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)
>>>>>>> 831207dfd5369527ce091e8e22af9589f70d6f99
=======
        self.terminal.grid(row=3, column=0, sticky="sew", padx=10, pady=10)
>>>>>>> 831207dfd5369527ce091e8e22af9589f70d6f99
