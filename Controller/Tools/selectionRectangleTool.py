import tkinter as tk
from PIL import ImageGrab, Image, ImageTk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.Graphics.imageUtils import ImageUtils

from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController
from Controller.toolBarController import ToolBarController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

from View.Resources.Widgets.toolBar import ToolBar

class TempRectangleState:
    """
    Save the properties of the temporary rectangle created on the canvas

    Attributes
    -----------
    startCoords : Vector2
        Temporary variable to stock when the selection rectangle is going to be created
    canvasRectangleID : int
        The ID of the selection rectangle drawn on the canvas, when the user is still resizing it
    """
    def __init__(self) -> None:
        self.startCoords: Vector2 = None
        self.canvasRectangleID: int = -1

class SelectionRectangleTool:
    """
    A Controller to manage the selection rectangle tool inside a canvas

    Attributes
    -----------
    SRCC : SelectionRectangleCanvasController
        A Controller used to communicate with the selection rectangle
    TBC : ToolBarController
        A Controller used to communicate with the tools bar
    __tempRectangleState : Vector2
        Temporary variable to stock when the selection rectangle is going to be created
    """

    def __init__(self, srcc: SelectionRectangleCanvasController, TBC : ToolBarController):
        # Connect the selection rectangle controller to the tool
        self.SRCC = srcc
        self.TBC = TBC
        
        self.__tempRectangleState = TempRectangleState()

    @property
    def canvas(self) -> tk.Canvas:
        return self.SRCC.CC.view
    
    @property
    def canvasImages(self) -> CanvasImage:
        return self.SRCC.CC.model.images.items()
    
    @property
    def selectionRectangle(self) -> SelectionRectangle:
        return self.SRCC.selectionRectangle
    
    @property
    def toolBar(self) -> ToolBar:
        return self.TBC.view
        
    #region Event

    def on_mouse_over(self, event: tk.Event) -> None:
        """
        Triggered when the mouse is over the canvas

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the mouse event, such as position (x, y).
        """
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        self.SRCC.on_mouse_over(event)

    def on_button_press(self, event):
        """
        Triggered when the left mouse button is pressed on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button press event, such as position (x, y).
        """
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        # Check what action the user want to do with the rectangle
        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.SRCC.hasSelectionRectangle():
            self.SRCC.deSelect()
            # Then save the coordinates where the mouse has clicked

        # Save the starting point for the rectangle
        self.__tempRectangleState.startCoords = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self.__tempRectangleState.canvasRectangleID = self.canvas.create_rectangle(
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            outline="black", 
            width=2, 
            dash=(2, 2)
        )

    def on_mouse_drag(self, event):
        """
        Triggered when the mouse is dragged across the canvas while the mouse left click is hold.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the drag event, such as position (x, y) and button state.
        """
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            # Update the coordinates and move the selection rectangle
            self.SRCC.on_mouse_drag(event)
            return

        # Update the rectangle as the mouse is dragged
        self.canvas.coords(
            self.__tempRectangleState.canvasRectangleID, 
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            mouseCoords.x, 
            mouseCoords.y
        )

        # Update the values in the toolbar
        self.TBC.view.selectionRectangleWidth.set(abs(mouseCoords.x - self.__tempRectangleState.startCoords.x))
        self.TBC.view.selectionRectangleHeight.set(abs(mouseCoords.y - self.__tempRectangleState.startCoords.y))

        
    def on_button_release(self, event):
        """
        Triggered when the left mouse click is released on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button release event, such as position (x, y).
        """
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        # Since the selection rectangle has been created, stop this function
        if self.SRCC.hasSelectionRectangle() and self.SRCC.action != SelectionRectangleAction.NONE:
            return
        
        # On release, finalize the rectangle selection by setting its end coordinates
        # and draw the actual selection rectangle
        self.canvas.delete(self.__tempRectangleState.canvasRectangleID)

        # If the user has only clicked on the canvas and didn't resize the selection rectangle, 
        # don't create it
        if self.__tempRectangleState.startCoords == mouseCoords:
            return

        # Set the selection rectangle created to the SelectionRectangleCanvasController
        self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(self.__tempRectangleState.startCoords.x, self.__tempRectangleState.startCoords.y, mouseCoords.x, mouseCoords.y))

        self.TBC.view.selectionRectangleWidth.set(self.selectionRectangle.width)
        self.TBC.view.selectionRectangleHeight.set(self.selectionRectangle.height)
        self.SRCC.activate_operations()

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