import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from DrawLibrary.Graphics.imageUtils import ImageUtils

from Model.toolManager import ToolManager

from View.Resources.Widgets.toolBar import ToolBar

class ToolBarController:
    def __init__(self, toolBar: ToolBar, toolManager : ToolManager):
        self.view = toolBar
        self.toolManager = toolManager

        self.view.mouseButton.configure(command=self.on_mouse_button_click)
        self.view.rectangleButton.configure(command=self.on_rectangle_button_click)
        
    def on_mouse_button_click(self):
        self.__reset_buttons()
        self.toolManager.setActiveTool("SELECTION_TOOL")
        self.view.mouseButton.configure(bg="#A9A9A9")

    def on_rectangle_button_click(self):
        self.__reset_buttons()
        self.toolManager.setActiveTool("SELECTION_TOOL_RECTANGLE")
        self.view.rectangleButton.configure(bg="#A9A9A9")

    def handle_button_activation(self, buttonName: str, activate: bool, command: callable = None) -> None:
        """
        Handles the activation or deactivation of a clipboard button.

        Parameters
        -----------
        buttonName : str
            The name of the button.
        activate : bool
            Set the state of the button to activate or deactive it
        command : callable
            The command to assign when activated.
        """
        icon = f"{buttonName}_on.png" if activate else f"{buttonName}_off.png"
        button: tk.Button = getattr(self.view, f"{buttonName}Button")
        image = ImageUtils.resizePhotoImageFromPath(
            f"Data/Assets/{icon}",
            button.image.width(),
            button.image.height()
        )
        button.configure(
            image=image, 
            command=command if activate else None, 
            state="active" if activate else "disabled"
        )
        button.image = image

        if DEBUG:
            print(f"{buttonName} button {'activated' if activate else 'deactivated'}")

    def __reset_buttons(self):
        # self.view.pasteButton.configure(state="disabled")
        # self.view.copyButton.configure(state="disabled")
        # self.view.cutButton.configure(state="disabled")
        # self.view.trashButton.configure(state="disabled")

        self.view.mouseButton.configure(bg="#f0f0f0")
        self.view.rectangleButton.configure(bg="#f0f0f0")



