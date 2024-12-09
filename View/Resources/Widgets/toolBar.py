import tkinter as tk
from tkinter import PhotoImage

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Creating a gap between icons by setting "minsize=100" every two column initializations
        self.columnconfigure(0)
        self.columnconfigure(1, minsize=100)
        self.columnconfigure(2)

        self.rowconfigure(0, minsize=30)

        # Load images
        mouse_image = PhotoImage(file="Data/Assets/mouse.png")  # Assurez-vous que l'image existe
        pencil_image = PhotoImage(file="Data/Assets/pencil.png")
        eraser_image = PhotoImage(file="Data/Assets/eraser.png")

        # Tool 1 - Mouse
        mouseButton = tk.Button(self, image=mouse_image, height=80, width=80)
        mouseButton.image = mouse_image  # Nécessaire pour empêcher l'image d'être collectée par le garbage collector
        mouseButton.grid(row=0, column=0)

        # Tool 2 - Pencil
        pencilButton = tk.Button(self, image=pencil_image, height=80, width=80)
        pencilButton.image = pencil_image
        pencilButton.grid(row=0, column=1)

        # Tool 3 - Eraser
        eraser = tk.Button(self, image=eraser_image, height=80, width=80)
        eraser.image = eraser_image
        eraser.grid(row=0, column=2)

# Fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    toolbar = ToolBar(root)
    toolbar.pack()
    root.mainloop()
