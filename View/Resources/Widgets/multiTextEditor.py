import tkinter as tk
from tkinter import ttk
import os
import json

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Chemin du fichier JSON
        self.json_file = "View/Resources/Widgets/gear.json"

        # Dernière date de modification connue
        self.last_modified_time = self.get_file_modification_time()

        # Charger les paramètres
        self.settings = self.load_settings()

        # Créer un widget Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Ajouter un premier onglet qui contient un éditeur de texte
        self.editor_tabs = []
        self.add_editor_tab(f"Fenêtre {1}")

        # Lancer la surveillance du fichier JSON
        self.monitor_settings()

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
        """
        Charge les paramètres depuis le fichier gear.json.
        Retourne les paramètres ou des valeurs par défaut.
        """
        try:
            if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                with open(self.json_file, "r") as file:
                    return json.load(file)
            else:
                print("Fichier gear.json introuvable ou vide. Chargement des valeurs par défaut.")
        except json.JSONDecodeError:
            print("Erreur : gear.json est corrompu. Chargement des valeurs par défaut.")
        return {"font": "Helvetica", "font_size": 12, "dark_mode": False}

    def apply_settings(self):
        """Applique les paramètres à tous les éditeurs ouverts sans modifier la taille de la zone de texte."""
        font = self.settings.get("font", "Helvetica")
        font_size = self.settings.get("font_size", 12)
        for text in self.editor_tabs:
            text.tag_configure("custom_font", font=(font, font_size))
            text.tag_add("custom_font", "1.0", "end")

    def add_editor_tab(self, title):
        """
        Crée un nouvel onglet avec un éditeur de texte.
        """
        # Créer un cadre pour le nouvel onglet
        frame = tk.Frame(self.notebook)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Créer un widget Text avec barre de défilement
        text = tk.Text(frame, wrap="word")
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=20)
        text.configure(yscrollcommand=vsb.set)

        # Appliquer le style initial avec un tag
        font = self.settings.get("font", "Helvetica")
        font_size = self.settings.get("font_size", 12)
        text.tag_configure("custom_font", font=(font, font_size))
        text.tag_add("custom_font", "1.0", "end")

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

    def monitor_settings(self):
        """
        Surveille les modifications du fichier JSON.
        Si une modification est détectée, recharge les paramètres et les applique.
        """
        current_modified_time = self.get_file_modification_time()
        if current_modified_time and current_modified_time != self.last_modified_time:
            self.last_modified_time = current_modified_time
            self.settings = self.load_settings()
            self.apply_settings()
            print("Paramètres rechargés depuis gear.json")

        # Relancer la surveillance après un délai
        self.after(1000, self.monitor_settings)  # Vérifie toutes les secondes

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    textEditor = MultiTextEditor(root)
    textEditor.pack(fill="both", expand=True)
    root.mainloop()
