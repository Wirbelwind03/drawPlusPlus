import tkinter as tk
from tkinter import ttk
import os
import json

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Créer un widget Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Initialiser la variable pour suivre la date de modification
        self.last_modified_time = None

        settings = self.load_settings()
        font = settings.get("font", "Helvetica")
        font_size = settings.get("font_size", 24)

        # Charger les paramètres initiaux pour le mode sombre et la police
        dark_mode = settings.get("dark_mode", False)
        self.background_color = "#2E2E2E" if dark_mode else "#636363"
        self.text_color = "white" if dark_mode else "black"

        # Ajouter 18 onglets avec des éditeurs de texte
        self.editor_tabs = [] 
        self.add_editor_tab(f"Fenêtre 1", font, font_size)

        # Vérifier les changements toutes les 500 ms
        self.check_for_changes()
    
    @property
    def openedTab(self) -> tk.Text:
        current_tab_index = self.notebook.index("current")  # Get the index of the current tab
        current_text_widget = self.editor_tabs[current_tab_index]  # Get the corresponding Text widget
        return current_text_widget

    def get_file_modification_time(self):
        """Retourne la date de modification du fichier JSON ou None si le fichier n'existe pas."""
        if os.path.exists(self.json_file):
            return os.path.getmtime(self.json_file)
        return None
    
    def load_settings(self):
        json_file = "View/Resources/Widgets/gear.json"
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            with open(json_file, "r") as file:
                settings = json.load(file)
            return settings
        else:
            print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
            exit(1)

    def add_editor_tab(self, title, font, font_size):
        """
        Crée un nouvel onglet avec un éditeur de texte.
        """
        # Créer un cadre pour le nouvel onglet
        frame = tk.Frame(self.notebook)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Créer un widget Text avec barre de défilement
        text = tk.Text(frame, wrap="word", bg=self.background_color, fg=self.text_color)
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=20)
        text.configure(yscrollcommand=vsb.set)
        
        text.tag_configure("custom_font", font=(font, font_size))

        # Appliquer dynamiquement le style pour tout texte nouvellement tapé
        def on_key(event):
            text.tag_add("custom_font", "1.0", "end")

        text.bind("<KeyRelease>", on_key)  # Lier la saisie utilisateur

        # Bloquer la redimension automatique liée au texte
        text.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Ajouter à la liste des éditeurs
        self.editor_tabs.append(text)

        # Ajouter l'onglet au Notebook
        self.notebook.add(frame, text=title)

    def check_for_changes(self):
        json_file = "View/Resources/Widgets/gear.json"

        # Vérifier si le fichier existe et si la date de modification a changé
        if os.path.exists(json_file):
            current_modified_time = os.path.getmtime(json_file)
            
            if self.last_modified_time is None or current_modified_time != self.last_modified_time:
                self.last_modified_time = current_modified_time

                settings = self.load_settings()
                dark_mode = settings.get("dark_mode", False)
                background_color = "black" if dark_mode else "white"
                text_color = "white" if dark_mode else "black"
                font = settings.get("font", "Helvetica")
                font_size = settings.get("font_size", 24)

                for editor in self.editor_tabs:
                    editor.config(bg=background_color,fg=text_color)
                    editor.tag_configure("custom_font", font=(font, font_size))  


        # Planifier la vérification suivante dans 500 ms
        self.after(500, self.check_for_changes)