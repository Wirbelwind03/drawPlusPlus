import tkinter as tk
from tkinter import PhotoImage

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=100)
        self.columnconfigure(2, minsize=100)

        self.rowconfigure(0, minsize=30)

        # Charger les images
        pencil_image = PhotoImage(file="Data/Assets/pencil.png")  # Assurez-vous que l'image existe
        eraser_image = PhotoImage(file="Data/Assets/pencil.png")
        highlighter_image = PhotoImage(file="Data/Assets/pencil.png")

        # Tool 1 - Pencil
        pencilButton = tk.Button(self, image=pencil_image, height=80, width=100)
        pencilButton.image = pencil_image  # Nécessaire pour empêcher l'image d'être collectée par le garbage collector
        pencilButton.grid(row=0, column=0)

        # Tool 2 - Eraser
        eraserButton = tk.Button(self, image=eraser_image, height=80, width=100)
        eraserButton.image = eraser_image
        eraserButton.grid(row=0, column=1)

        # Tool 3 - Highlighter
        HighButton = tk.Button(self, image=highlighter_image, height=80, width=100)
        HighButton.image = highlighter_image
        HighButton.grid(row=0, column=2)

# Fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    toolbar = ToolBar(root)
    toolbar.pack()
    root.mainloop()
