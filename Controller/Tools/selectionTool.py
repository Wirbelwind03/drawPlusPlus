import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class SelectionTool:
    """
    A Controller to manage the selection tool inside a canvas

    Attributes
    -----------
    srcc : SelectionRectangleCanvasController
        A Controller used to communicate with the selection rectangle
    """

    def __init__(self, SRCC: SelectionRectangleCanvasController):
        # Connect the selection rectangle controller to the tool
        self.SRCC = SRCC

    @property
    def toolBar(self):
        return self.SRCC.TBC.view
    
    @property
    def canvas(self):
        return self.SRCC.CC.view

    def getClickedImage(self, mouseCoords: Vector2) -> bool:
        # Loop all the images present on the canvas
        for imageId, image in self.SRCC.CC.model.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.SRCC.selectImage(image)
                return True
            
        return False

    #region Event

    def on_mouse_over(self, event: tk.Event) -> None:
        """
        Triggered when the mouse is over the canvas

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the mouse event, such as position (x, y).
        """
        mouseCoords = Vector2(event.x, event.y)

        self.SRCC.on_mouse_over(event)

    def on_button_press(self, event: tk.Event) -> None:
        """
        Triggered when the left mouse click is clicked on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button release event, such as position (x, y).
        """
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.SRCC.hasSelectionRectangle():
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image/selection rectangle, deselect it
        if self.SRCC.hasSelectionRectangle() and self.SRCC.selectionRectangle.isOutside(mouseCoords):
            self.SRCC.deSelect()
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
           
    def on_mouse_drag(self, event: tk.Event) -> None:
        """
        Triggered when the mouse is dragged across the canvas while the mouse left click is hold.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the drag event, such as position (x, y) and button state.
        """
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            self.SRCC.on_mouse_drag(event)
            return
        
    def on_button_release(self, event: tk.Event) -> None:
        """
        Triggered when the left mouse click is released on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button release event, such as position (x, y).
        """
        mouseCoords = Vector2(event.x, event.y)
        
        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            self.SRCC.on_button_release(event)
            pass

    def on_delete(self, event: tk.Event) -> None:
        """
        Triggered when the "Del" key on the keyboard is pressed.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.deleteSelectionRectangle()

    def on_control_c(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+C" keyboard shortcut is pressed (Copy command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.on_control_c(event)

    def on_control_v(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+V" keyboard shortcut is pressed (Paste command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.on_control_v(event)

    def on_control_x(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+X" keyboard shortcut is pressed (Cut command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.on_control_x(event)

    def on_left(self, event: tk.Event) -> None:
        """
        Triggered when the left arrow key on the keyboard is pressed.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.on_left(event)

    def on_right(self, event: tk.Event) -> None:
        """
        Triggered when the right arrow key on the keyboard is pressed.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.SRCC.on_right(event)

    #endregion Event




