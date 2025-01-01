import tkinter as tk
from tkinter import ttk


class GearWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Fenêtre de Paramètres")
        self.geometry("400x300")

        # Fonction pour enregistrer les paramètres (mais sans affichage ou changement visible)
        def save_settings():
            # Les paramètres sont simplement enregistrés sans retour visuel.
            language = language_var.get()
            font = font_var.get()
            font_size = font_size_var.get()
            dark_mode = dark_mode_var.get()
            print(f"Langue : {language}, Police : {font}, Taille : {font_size}, Mode sombre : {dark_mode}")

        # Label principal
        label = tk.Label(self, text="Paramètres de l'application", font=("Arial", 14))
        label.pack(pady=20)

        # Cadre pour les paramètres
        frame = tk.LabelFrame(self, text="Personnalisation", padx=10, pady=10)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Choix de la langue
        label_lang = tk.Label(frame, text="Choisir la langue :")
        label_lang.grid(row=0, column=0, sticky="w", padx=10)

        language_options = ["Français", "Anglais"]
        language_var = tk.StringVar(value="Français")
        language_menu = ttk.Combobox(frame, textvariable=language_var, values=language_options)
        language_menu.grid(row=0, column=1, padx=10)

        # Choix de la police
        label_font = tk.Label(frame, text="Choisir la police :")
        label_font.grid(row=1, column=0, sticky="w", padx=10)

        font_options = ["Arial", "Courier New", "Times New Roman", "Verdana"]
        font_var = tk.StringVar(value="Arial")
        font_menu = ttk.Combobox(frame, textvariable=font_var, values=font_options)
        font_menu.grid(row=1, column=1, padx=10)

        # Choix de la taille de caractère
        label_size = tk.Label(frame, text="Choisir la taille de caractère :")
        label_size.grid(row=2, column=0, sticky="w", padx=10)

        font_size_options = [8, 10, 12, 14, 16, 18, 20]
        font_size_var = tk.IntVar(value=12)
        font_size_menu = ttk.Combobox(frame, textvariable=font_size_var, values=font_size_options)
        font_size_menu.grid(row=2, column=1, padx=10)

        # Choix du mode sombre
        dark_mode_var = tk.BooleanVar()
        dark_mode_check = tk.Checkbutton(frame, text="Mode sombre", variable=dark_mode_var)
        dark_mode_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Bouton Enregistrer
        save_button = tk.Button(self, text="Enregistrer", command=save_settings)
        save_button.pack(pady=10)

        # Lancer l'application
        self.mainloop()


# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x150")  # Taille de la fenêtre principale
    main_button = tk.Button(root, text="Ouvrir paramètres", command=lambda: GearWindow(root))
    main_button.pack(pady=20)
    root.mainloop()
