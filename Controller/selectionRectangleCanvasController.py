import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from Controller.canvasController import CanvasController

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.Graphics.imageUtils import ImageUtils

from Model.canvasEntities import CanvasEntities
from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

from Controller.toolBarController import ToolBarController

class GapOffset:
    def __init__(self):
        self.start = Vector2(0, 0)
        self.end = Vector2(0, 0)

class SelectionRectangleCanvasController:
    """
    A class to manage the selection rectangle in the Canvas

    Attributes
    -----------
    CC : CanvasController
        A Controller used to communicate with the Canvas
    """

    def __init__(self, CC: CanvasController, TBC: ToolBarController):
        # Connect the controller to the canvas
        self.CC = CC
        self.TBC = TBC
        self.selectionRectangle: SelectionRectangle = None
        
        self.TBC.view.selectionRectangleHeight.trace_add("write", self.on_selection_rectangle_dimension_change)
        self.TBC.view.selectionRectangleWidth.trace_add("write", self.on_selection_rectangle_dimension_change)
        self.TBC.view.widthInput.configure(command=self.on_width_input_change)
        self.TBC.view.heightInput.configure(command=self.on_height_input_change)

        self.__gapOffset = GapOffset()

    #region Public Methods

    def setSelectionRectangle(self, selectionRectangle: SelectionRectangle, attachedImage: CanvasImage = None) -> None:
        self.selectionRectangle = selectionRectangle
        if attachedImage:
            self.selectionRectangle.attachedImage = attachedImage

    def hasSelectionRectangle(self) -> bool:
        """
        Check if the canvas has a selection rectangle

        Returns
        -----------
        Bool
            If there is a selection rectangle present on the canvas
        """
        return self.selectionRectangle is not None
    
    def setAction(self, action: SelectionRectangleAction) -> None:
        """
        Set the action of the selection rectangle.
        Also set the cursor.

        Parameters
        -----------
        action : SelectionRectangleAction
            What action to set for the selection rectangle
        """
        self.selectionRectangle.action = action
        if self.getAction() == SelectionRectangleAction.RESIZE:
            self.CC.view.config(cursor="umbrella")
        elif self.getAction() == SelectionRectangleAction.MOVE:
            self.CC.view.config(cursor="fleur")
        else:
            self.CC.view.config(cursor="arrow")

    def getAction(self) -> SelectionRectangleAction:
        """
        Get the current action of the selection rectangle.

        Returns
        -----------
        SelectionRectangleAction
            The current action of the selection rectangle
        """
        return self.selectionRectangle.action
    
    def create(self) -> None:
        """
        Create a selection rectangle on a canvas.
        """
        # Draw the main frame of the selection rectangle
        self.selectionRectangle.canvasIdRectangle = self.CC.view.create_rectangle(self.selectionRectangle.x, self.selectionRectangle.y, self.selectionRectangle.x + self.selectionRectangle.width, self.selectionRectangle.y + self.selectionRectangle.height, outline="black", width=2, dash=(2, 2))
    
    def erase(self) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas.
        """
        self.CC.view.delete(self.selectionRectangle.canvasIdRectangle)

    def render(self) -> None:
        sr = self.selectionRectangle

        self.CC.view.coords(sr.canvasIdRectangle, sr.topLeft.x, sr.topLeft.y, sr.bottomRight.x,  sr.bottomRight.y)
        
        # Render the image to the new position
        if self.selectionRectangle.attachedImage:
            self.CC.view.coords(self.selectionRectangle.attachedImage.id, self.selectionRectangle.center.x, self.selectionRectangle.center.y)

    def deleteSelectionRectangle(self) -> None:
        """
        Delete completly the selection rectangle and the image inside it if there's one on the canvas.
        """
        if not self.selectionRectangle:
            return

        # If there is a attached image in the selection rectangle
        if self.selectionRectangle.attachedImage:
            # Delete the image first
            self.CC.deleteImage(self.selectionRectangle.attachedImage)
            self.selectionRectangle.attachedImage = None
            self.handle_clipboard_activation(False)
        # Erase the selection rectangle
        self.deSelect()

        self.TBC.view.selectionRectangleWidth.set(0)
        self.TBC.view.selectionRectangleHeight.set(0)
        self.TBC.view.widthInput.configure(state="disabled")
        self.TBC.view.heightInput.configure(state="disabled")

    def deSelect(self) -> None:
        """
        Deselect the selection rectangle on the canvas.
        """
        # Erase the rendering of the selection rectangle
        self.erase()
        # Completly remove the selection rectangle
        self.selectionRectangle = None
        # Set the cursor to default (arrow)
        self.CC.view.config(cursor="arrow")

    def handle_clipboard_activation(self, activate: bool) -> None:
        icon = "clipboard_on.png" if activate else "clipboard_off.png"
        command = self.clipBoardPaste if activate else None
        image = ImageUtils.resizePhotoImageFromPath(f"Data/Assets/{icon}", 64, 64)
        self.TBC.view.pasteButton.configure(image=image, command=command)
        self.TBC.view.pasteButton.image = image

    #endregion Public Methods

    def on_selection_rectangle_dimension_change(self, *args):
        self.selectionRectangle.height = self.TBC.view.selectionRectangleHeight.get()
        self.selectionRectangle.width = self.TBC.view.selectionRectangleWidth.get()
        if self.selectionRectangle:
            self.CC.view.coords(
                self.selectionRectangle.canvasIdRectangle, 
                self.selectionRectangle.x, 
                self.selectionRectangle.y, 
                self.selectionRectangle.bottomRight.x, 
                self.selectionRectangle.bottomRight.y
            )

    def on_width_input_change(self):
        self.TBC.view.selectionRectangleWidth.set(int(self.TBC.view.widthInput.get()))

    def on_height_input_change(self):
        self.TBC.view.selectionRectangleHeight.set(int(self.TBC.view.heightInput.get()))

    #region Event

    def on_mouse_over(self, event) -> None:
        """
        A event for when the mouse is hovering on the selection rectangle

        Parameters
        -----------
        event : 
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        mouseCoords = Vector2(event.x, event.y)
        
        # Check if the mouse is inside the selection rectangle    
        if self.selectionRectangle.isInside(mouseCoords):
            # If it is, change that the action we want to do is moving the selection rectangle
            self.setAction(SelectionRectangleAction.MOVE)
        else:
            # If it's not, change that the action we want to do is creating a selection rectangle
            self.setAction(SelectionRectangleAction.NONE)

    def on_button_press(self, event):
        """
        A event for when a left click occur on the selection rectangle

        Parameters
        -----------
        event : 
        """
        mouseCoords = Vector2(event.x, event.y)

        self.drag_start = mouseCoords

        if self.getAction() == SelectionRectangleAction.MOVE:
            # Get the gap between the cursor and the min and max of the AABB
            # So the user can move the rectangle by clicking anywhere inside
            self.__gapOffset.start = mouseCoords - self.selectionRectangle.min
            self.__gapOffset.end = mouseCoords - self.selectionRectangle.max

    def on_mouse_drag(self, event):
        """
        A event for when the user drag the selection rectangle

        Parameters
        -----------
        event : 
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        mouseCoords = Vector2(event.x, event.y)

        sr = self.selectionRectangle

        if self.getAction() == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.selectionRectangle.setCoords(mouseCoords - self.__gapOffset.start, mouseCoords - self.__gapOffset.end)
            
            # Render the selection rectangle to the new position
            self.render()

        if DEBUG and self.CC.DCC != None:
            if self.selectionRectangle.attachedImage:
                self.CC.DCC.drawCanvasImageDebugInfos(self.selectionRectangle.attachedImage)

        self.drag_start = mouseCoords

    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

    def on_left(self, event):
        mouseCoords = Vector2(event.x, event.y)

        self.selectionRectangle.setCoords(self.selectionRectangle.attachedImage.bbox.topLeft, self.selectionRectangle.attachedImage.bbox.bottomRight)

        # Render the selection rectangle to the new position
        self.render()

        if DEBUG and self.CC.DCC != None:
            self.CC.DCC.drawCanvasImageDebugInfos(self.selectionRectangle.attachedImage)

    def clipBoardPaste(self):
        if self.selectionRectangle.attachedImage:
            self.CC.drawImage(self.selectionRectangle.attachedImage, self.selectionRectangle.min.x, self.selectionRectangle.min.y)

    #endregion Event
