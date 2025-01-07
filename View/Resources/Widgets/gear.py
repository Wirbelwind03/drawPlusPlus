import tkinter as tk
from tkinter import ttk
from .multiTextEditor import *

class GearWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.vars = {}

        self.title("Fenêtre de Paramètres")
        self.geometry("600x400")

        # Label principal
        self.label = tk.Label(self, text="Settings")
        self.label.pack(pady=20)

        # Cadre pour les paramètres
        self.frame = tk.LabelFrame(self, text="Personnalisation", padx=10, pady=10)
        self.frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Choix de la police
        self.label_font = tk.Label(self.frame, text="Choisir la police :")
        self.label_font.grid(row=1, column=0, sticky="w", padx=10)

        font_options = ["Helvetica", "Arial", "Courier New", "Times New Roman", "Verdana"]
        self.vars["Font"] = tk.StringVar()
        font_menu = ttk.Combobox(self.frame, textvariable=self.vars["Font"], values=font_options)
        font_menu.grid(row=1, column=1, padx=10)

        # Choix de la taille de caractère
        self.label_size = tk.Label(self.frame, text="Choisir la taille de caractère :")
        self.label_size.grid(row=2, column=0, sticky="w", padx=10)

        font_size_options = [8, 10, 12, 14, 16, 18, 20, 22 , 24 , 26 , 28 , 30]
        self.vars["FontSize"] = tk.IntVar()
        font_size_menu = ttk.Combobox(self.frame, textvariable=self.vars["FontSize"], values=font_size_options)
        font_size_menu.grid(row=2, column=1, padx=10)

        # Choix du mode sombre
        self.vars["DarkMode"] = tk.BooleanVar()
        self.dark_mode_check = tk.Checkbutton(self.frame, text="Mode sombre", variable=self.vars["DarkMode"])
        self.dark_mode_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Texte centré entre le label et le bouton
        self.example_text = tk.Label(self, text="Example Text")
        self.example_text.pack(pady=10, anchor='center')  # Centrer le texte

        # Bouton Enregistrer
        self.save_button = tk.Button(self, text="Enregistrer")
        self.save_button.pack(pady=10)

