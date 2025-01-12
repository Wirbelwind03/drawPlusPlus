import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from DrawLibrary.Graphics.imageUtils import ImageUtils

from Model.toolManager import ToolManager

from View.Resources.Widgets.toolBar import ToolBar

class ToolBarController:
    """
    The ToolBarController controller is used to communicate when the tools are pressed

    Attributes
    -----------
    view : ToolBar
        The canvas where the ViewModel is tied to
    toolManager : ToolManager
        The tools tied to this controller, for example, the selection tool, the selection rectangle creation tool, etc.
    """

    def __init__(self, toolBar: ToolBar, toolManager : ToolManager) -> None:
        self.view = toolBar
        self.toolManager = toolManager

        # Add events to the button
        self.view.mouseButton.configure(command=self.on_mouse_button_click)
        self.view.rectangleButton.configure(command=self.on_rectangle_button_click)
        
    def on_mouse_button_click(self):
        """
        Event when the button for selecting a image is clicked
        """
        # Change the others button color
        self.__reset_buttons()
        # Set the acitve tool
        self.toolManager.setActiveTool("SELECTION_TOOL")
        # Set active color for the button
        self.view.mouseButton.configure(bg="#A9A9A9")

    def on_rectangle_button_click(self):
        """
        Event when the button for creating the selection rectangle is clicked
        """
        # Change the others button color
        self.__reset_buttons()
        # Set the acitve tool
        self.toolManager.setActiveTool("SELECTION_TOOL_RECTANGLE")
        # Set active color for the button
        self.view.rectangleButton.configure(bg="#A9A9A9")

    def handle_button_activation(self, buttonName: str, activate: bool, command: callable = None) -> None:
        """
        Handles the activation or deactivation of a button.

        Parameters
        -----------
        buttonName : str
            The name of the button.
        activate : bool
            Set the state of the button to activate or deactivate it
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

    def __reset_buttons(self) -> None:
        """
        Reset the buttons color
        """
        self.view.mouseButton.configure(bg="#f0f0f0")
        self.view.rectangleButton.configure(bg="#f0f0f0")



