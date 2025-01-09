import tkinter as tk
from tkinter import PhotoImage

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Spacing between icons
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1)
        self.columnconfigure(2,minsize=100)
        self.columnconfigure(3)
        self.columnconfigure(4,minsize=100)
        self.columnconfigure(5,weight=1)
        self.rowconfigure(0, minsize=30)

        # Load images
        mouse_image = PhotoImage(file="Data/Assets/mouse.png")
        rectangle_image = PhotoImage(file="Data/Assets/rectangle.png")
        rotation_image = PhotoImage(file="Data/Assets/rotation.png")
        trash_image = PhotoImage(file="Data/Assets/trash.png")

        # 1-Mouse button
        mouseButton = tk.Button(self, image=mouse_image, height=80, width=80)
        mouseButton.image = mouse_image
        mouseButton.grid(row=0, column=1)

        # 2-Selection rectangle button
        rectangleButton = tk.Button(self, image=rectangle_image, height=80, width=80)
        rectangleButton.image = rectangle_image
        rectangleButton.grid(row=0, column=2)

        # 3-Rotation button
        rotationButton = tk.Button(self, image=rotation_image, height=80, width=80)
        rotationButton.image = rotation_image
        rotationButton.grid(row=0, column=3)

        #   4-Trash button
        trashButton= tk.Button(self, image=trash_image, height=80, width=80)
        trashButton.image = trash_image
        trashButton.grid(row=0, column=4)
