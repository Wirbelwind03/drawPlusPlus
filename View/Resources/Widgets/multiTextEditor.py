import tkinter as tk
from tkinter import ttk
import os
import json

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a Notebook Widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add 4 tabs with text editors
        for i in range(1, 19):
            self.add_editor_tab(f"Fenêtre {i}")

    def add_editor_tab(self, title):

        # Create an independent text editor

        frame = tk.Frame(self.notebook)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Chemin du fichier JSON
        json_file = "View/Resources/Widgets/gear.json"

        # Fonction pour charger les paramètres depuis le fichier JSON
        def load_settings():
            # Vérifie si le fichier existe et n'est pas vide
            if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                with open(json_file, "r") as file:
                    settings = json.load(file)
                return settings
            else:
                print("Erreur dans le fichier JSON : gear.json est introuvable, vide ou corrompu.")
                exit(1)

        # Charger les paramètres
        settings = load_settings()

        # Charger les paramètres sauvegardés ou utiliser les valeurs par défaut
        font = settings.get("font", "Helvetica")
        font_size = settings.get("font_size", 24)
        dark_mode = settings.get("dark_mode", False)
        
        text = tk.Text(frame, wrap="word")
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=20)
        text.configure(yscrollcommand=vsb.set)
        text.tag_configure("custom_font", font=(font,font_size))

        # Appliquer dynamiquement le tag "custom_font" à chaque caractère tapé
        def on_key(event):
            # Applique le style de police et taille à chaque caractère
            text.tag_add("custom_font", "1.0", "end")

        # Lier l'événement de saisie au texte
        text.bind("<KeyRelease>", on_key)
        
        text.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Add it as a new "tab" to the Notebook
        self.notebook.add(frame, text=title)

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    textEditor = MultiTextEditor(root)
    textEditor.pack()
    root.mainloop()