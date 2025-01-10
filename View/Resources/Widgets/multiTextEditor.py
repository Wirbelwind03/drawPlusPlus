import tkinter as tk
from tkinter import ttk

from View.theme import Theme

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Créer un widget Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Ajouter 18 onglets avec des éditeurs de texte
        self.editor_tabs = [] 
        self.add_editor_tab(f"Fenêtre 1")
    
    @property
    def openedTab(self) -> tk.Text:
        current_tab_index = self.notebook.index("current")  # Get the index of the current tab
        current_text_widget = self.editor_tabs[current_tab_index]  # Get the corresponding Text widget
        return current_text_widget

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
        
        text.tag_configure("custom_font")

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

    def refresh(self, settings):
        # style = ttk.Style()
        # style.configure('TNotebook.Tab', background=Theme.MainBackgroundColor(settings))
        # style.map('TNotebook.Tab', background=[('selected', 'blue')], foreground=[('selected', 'white')])  # Selected tab
        for text in self.editor_tabs:
            text.configure(font=(settings["font"], settings["font_size"]))
            text.configure(bg=Theme.BackgroundColor(settings))
            text.configure(insertbackground=Theme.InsertBackgroundColor(settings))
            text.configure(foreground=Theme.FontColor(settings))