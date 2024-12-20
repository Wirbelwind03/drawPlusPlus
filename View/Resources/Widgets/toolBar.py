import tkinter as tk
from tkinter import PhotoImage

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Creating a gap between icons by setting "minsize=100" every two column initializations
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1)
        self.columnconfigure(2,minsize=100)
        self.columnconfigure(3)
        self.columnconfigure(4,minsize=100)
        self.columnconfigure(5,weight=1)

        self.rowconfigure(0, minsize=30)

        # Load images
        mouse_image = PhotoImage(file="Data/Assets/mouse.png")  # Assurez-vous que l'image existe
        rectangle_image = PhotoImage(file="Data/Assets/rectangle.png")
        rotation_image = PhotoImage(file="Data/Assets/rotation.png")
        trash_image = PhotoImage(file="Data/Assets/trash.png")

        # Tool 1 - Mouse
        mouseButton = tk.Button(self, image=mouse_image, height=80, width=80)
        mouseButton.image = mouse_image  # Nécessaire pour empêcher l'image d'être collectée par le garbage collector
        mouseButton.grid(row=0, column=1)

        # Tool 2 - Rectangle de selection
        rectangleButton = tk.Button(self, image=rectangle_image, height=80, width=80)
        rectangleButton.image = rectangle_image
        rectangleButton.grid(row=0, column=2)

        # Tool 3 - Rotation
        rotationButton = tk.Button(self, image=rotation_image, height=80, width=80)
        rotationButton.image = rotation_image
        rotationButton.grid(row=0, column=3)

        # Tool 4 - Trash
        trashButton= tk.Button(self, image=trash_image, height=80, width=80)
        trashButton.image = trash_image
        trashButton.grid(row=0, column=4)

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    toolbar = ToolBar(root)
    toolbar.pack()
    root.mainloop()
