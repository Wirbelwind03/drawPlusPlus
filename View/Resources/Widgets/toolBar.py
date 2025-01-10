import tkinter as tk
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk  # Import Pillow for resize

from DrawLibrary.Graphics.imageUtils import ImageUtils

from View.Resources.Widgets.numericSpinBox import NumericSpinBox

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
        mouse_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/mouse.png", 48, 48)
        rectangle_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/rectangle.png", 48, 48)
        trash_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/trash.png", 48, 48)

        clipboardOperationsFrame = tk.Frame(self)
        clipboardOperationsFrame.grid(row=0, column=0)
        self.__construct_clipboard_operations_frame(clipboardOperationsFrame)

        # Tool 1 - Mouse
        self.mouseButton = tk.Button(self, image=mouse_image, height=48, width=48)
        self.mouseButton.image = mouse_image
        self.mouseButton.grid(row=0, column=1)

        # Tool 2 - Rectangle selection
        self.rectangleButton = tk.Button(self, image=rectangle_image, height=48, width=48)
        self.rectangleButton.image = rectangle_image
        self.rectangleButton.grid(row=0, column=2)

        # Tool 3 - Rotation
        rotateFrame = tk.Frame(self)
        rotateFrame.grid(row=0, column=3)
        self.__construct_rotate_frame(rotateFrame)

        # Tool 4 & Input Group - Resize
        resizeFrame = tk.Frame(self)
        resizeFrame.grid(row=0, column=4)
        self.__construct_resize_frame(resizeFrame)

        # Tool 5 - Trash
        self.trashButton = tk.Button(self, image=trash_image, height=48, width=48, state="disabled")
        self.trashButton.image = trash_image
        self.trashButton.grid(row=0, column=5)

    def __construct_clipboard_operations_frame(self, clipboardOperationsFrame: tk.Frame):
        cut_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/cut_off.png", 16, 16)
        copy_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/copy_off.png", 16, 16)
        paste_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/paste_off.png", 48, 48)

        ##### Column 0
        pasteFrame = tk.Frame(clipboardOperationsFrame)
        pasteFrame.grid(row=0, column=0)

        self.pasteButton = tk.Button(pasteFrame, image=paste_image, height=48, width=48, state="disabled")
        self.pasteButton.image = paste_image
        self.pasteButton.grid(row=0, column=0, padx=(0, 5))

        pasteLabel = tk.Label(pasteFrame, text="Coller")
        pasteLabel.grid(row=1, column=0, pady=(0, 2))  # Label above the input

        ##### Column 1
        otherFrame = tk.Frame(clipboardOperationsFrame)
        otherFrame.grid(row=0, column=1, sticky="n")  # Align the frame itself to the top

        otherFrame.grid_rowconfigure(0, weight=1)  # Ensure top alignment for content
        otherFrame.grid_rowconfigure(1, weight=0)  # Avoid distributing space to this row

        ###
        self.cutButton = tk.Button(
            otherFrame, 
            image=cut_image, 
            text="Couper", 
            compound="left",
            state="disabled"
        )
        self.cutButton.image = cut_image
        self.cutButton.grid(row=0, column=0, sticky="n", pady=(0, 5))  # Align to the top with padding

        ###
        self.copyButton = tk.Button(
            otherFrame, 
            image=copy_image, 
            text="Copier", 
            compound="left",
            state="disabled"
        )
        self.copyButton.image = copy_image
        self.copyButton.grid(row=1, column=0, sticky="n", pady=(0, 5))  

        ##### Column 2
        separator_after = ttk.Separator(clipboardOperationsFrame, orient="vertical")
        separator_after.grid(row=0, column=2, sticky="ns", padx=(5, 5))

    def __construct_rotate_frame(self, rotateFrame: tk.Frame):
        rotation_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/rotation.png", 48, 48)
        
        # Separator before Resize Frame
        separator_before = ttk.Separator(rotateFrame, orient="vertical")
        separator_before.grid(row=0, column=0, sticky="ns", padx=(5, 5))

        descriptionFrame = tk.Frame(rotateFrame)
        descriptionFrame.grid(row=0, column=1)

        self.rotationImageLabel = tk.Label(descriptionFrame, image=rotation_image, height=64, width=64)
        self.rotationImageLabel.image = rotation_image
        self.rotationImageLabel.grid(row=0, column=0)

        descriptionLabel = tk.Label(descriptionFrame, text="Rotation")
        descriptionLabel.grid(row=1, column=0, pady=(0, 2))  # Label above the input
        
        # Vertical Frame for Inputs (Width & Height)
        inputFrame = tk.Frame(rotateFrame)
        inputFrame.grid(row=0, column=2)

        #
        degreesLabel = tk.Label(inputFrame, text="Degrees")
        degreesLabel.grid(row=0, column=0, sticky="w", pady=(0, 2))  # Label above the input
        self.selectionRectangleDegrees = tk.IntVar(rotateFrame, 0)
        self.widthInput = NumericSpinBox(inputFrame, width=6, justify="left", from_=0, to=360, textvariable=self.selectionRectangleDegrees, state="disabled")
        self.widthInput.grid(row=1, column=0)

    def __construct_resize_frame(self, resizeFrame: tk.Frame):
        resize_image = ImageUtils.resizePhotoImageFromPath("Data/Assets/resize.png", 48, 48)

        # Separator before Resize Frame
        separator_before = ttk.Separator(resizeFrame, orient="vertical")
        separator_before.grid(row=0, column=0, sticky="ns", padx=(5, 5))

        descriptionFrame = tk.Frame(resizeFrame)
        descriptionFrame.grid(row=0, column=1)

        self.resizeLabel = tk.Label(descriptionFrame, image=resize_image, height=64, width=64)
        self.resizeLabel.image = resize_image
        self.resizeLabel.grid(row=0, column=0, padx=(0, 5))  # Place the button to the left of inputs

        descriptionLabel = tk.Label(descriptionFrame, text="Zoom")
        descriptionLabel.grid(row=1, column=0, pady=(0, 2))  # Label above the input

        # Vertical Frame for Inputs (Width & Height)
        inputFrame = tk.Frame(resizeFrame)
        inputFrame.grid(row=0, column=2)

        # Width Input
        widthLabel = tk.Label(inputFrame, text="Width")
        widthLabel.grid(row=0, column=0, sticky="w", pady=(0, 2))  # Label above the input
        self.selectionRectangleWidth = tk.IntVar(resizeFrame, 0)
        self.widthInput = NumericSpinBox(inputFrame, width=6, justify="left", from_=0, to=9999, textvariable=self.selectionRectangleWidth, state="disabled")
        self.widthInput.grid(row=1, column=0)

        # Height Input
        heightLabel = tk.Label(inputFrame, text="Height")
        heightLabel.grid(row=2, column=0, sticky="w", pady=(0, 2))  # Label above the input
        self.selectionRectangleHeight = tk.IntVar(resizeFrame, 0)
        self.heightInput = NumericSpinBox(inputFrame, width=6, justify="left", from_=0, to=9999, textvariable=self.selectionRectangleHeight, state="disabled")
        self.heightInput.grid(row=3, column=0)

        # Separator after Resize Frame
        separator_after = ttk.Separator(resizeFrame, orient="vertical")
        separator_after.grid(row=0, column=3, sticky="ns", padx=(5, 5))
