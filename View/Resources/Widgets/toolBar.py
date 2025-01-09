import tkinter as tk
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk  # Import Pillow for resize
from DrawLibrary.Graphics.imageUtils import ImageUtils

class ToolBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Creating a gap between icons by setting "minsize=100" every two column initializations
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=100)
        self.columnconfigure(2, minsize=100)
        self.columnconfigure(3, minsize=100)
        self.columnconfigure(4, minsize=100)
        self.columnconfigure(5, minsize=100)
        self.columnconfigure(7, weight=1)
        self.rowconfigure(0, minsize=30)

        # Load images
        mouse_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/mouse.png", 64, 64)
        rectangle_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/rectangle.png", 64, 64)
        rotation_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/rotation.png", 64, 64)
        trash_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/trash.png", 64, 64)

        clipboardOperationsFrame = tk.Frame(self)  # Frame for grouping the resize button and inputs
        clipboardOperationsFrame.grid(row=0, column=0, padx=10)
        self.__construct_clipboard_operations_frame(clipboardOperationsFrame)

        # Tool 1 - Mouse
        self.mouseButton = tk.Button(self, image=mouse_image, height=80, width=80)
        self.mouseButton.image = mouse_image
        self.mouseButton.grid(row=0, column=1)

        # Tool 2 - Rectangle selection
        self.rectangleButton = tk.Button(self, image=rectangle_image, height=80, width=80)
        self.rectangleButton.image = rectangle_image
        self.rectangleButton.grid(row=0, column=2)

        # Tool 3 - Rotation
        self.rotationButton = tk.Button(self, image=rotation_image, height=80, width=80)
        self.rotationButton.image = rotation_image
        self.rotationButton.grid(row=0, column=3)

        # Tool 4 & Input Group - Resize
        resizeFrame = tk.Frame(self)  # Frame for grouping the resize button and inputs
        resizeFrame.grid(row=0, column=4, padx=10)
        self.__construct_resize_frame(resizeFrame)

        # Tool 5 - Trash
        self.trashButton = tk.Button(self, image=trash_image, height=80, width=80)
        self.trashButton.image = trash_image
        self.trashButton.grid(row=0, column=5)

    def __construct_clipboard_operations_frame(self, clipboardOperationsFrame: tk.Frame):
        paste_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/clipboard_off.png", 64, 64)

        self.pasteButton = tk.Button(clipboardOperationsFrame, image=paste_image, height=80, width=80)
        self.pasteButton.image = paste_image
        self.pasteButton.grid(row=0, column=0, padx=(0, 5))

        separator_after = ttk.Separator(clipboardOperationsFrame, orient="vertical")
        separator_after.grid(row=0, column=1, sticky="ns", padx=(5, 5))

    def __construct_resize_frame(self, resizeFrame: tk.Frame):
        resize_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/resize.png", 64, 64)

        # Separator before Resize Frame
        separator_before = ttk.Separator(resizeFrame, orient="vertical")
        separator_before.grid(row=0, column=0, sticky="ns", padx=(5, 5))

        self.resizeButton = tk.Button(resizeFrame, image=resize_image, height=80, width=80)
        self.resizeButton.image = resize_image
        self.resizeButton.grid(row=0, column=1, padx=(0, 5))  # Place the button to the left of inputs

        # Vertical Frame for Inputs (Width & Height)
        inputFrame = tk.Frame(resizeFrame)
        inputFrame.grid(row=0, column=2)

        # Width Input
        widthLabel = tk.Label(inputFrame, text="Width")
        widthLabel.grid(row=0, column=0, sticky="w", pady=(0, 2))  # Label above the input
        self.selectionRectangleWidth = tk.IntVar()
        self.widthInput = tk.Entry(inputFrame, width=6, justify="left", textvariable=self.selectionRectangleWidth)
        self.widthInput.grid(row=1, column=0)

        # Height Input
        heightLabel = tk.Label(inputFrame, text="Height")
        heightLabel.grid(row=2, column=0, sticky="w", pady=(0, 2))  # Label above the input
        self.selectionRectangleHeight = tk.IntVar()
        self.heightInput = tk.Entry(inputFrame, width=6, justify="left", textvariable=self.selectionRectangleHeight)
        self.heightInput.grid(row=3, column=0)

        # Separator after Resize Frame
        separator_after = ttk.Separator(resizeFrame, orient="vertical")
        separator_after.grid(row=0, column=3, sticky="ns", padx=(5, 5))
