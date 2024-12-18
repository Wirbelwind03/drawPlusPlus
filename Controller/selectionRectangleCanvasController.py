import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from Controller.canvasController import CanvasController

from DrawLibrary.Core.Shapes.rectangle import RectangleCorners
from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.canvasEntities import CanvasEntities
from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

class SelectionRectangleCanvasController:
    """
    A class to manage the selection rectangle in the Canvas

    Attributes
    -----------
    CC : CanvasController
        A Controller used to communicate with the Canvas
    """

    def __init__(self, CC: CanvasController):
        # Connect the controller to the canvas
        self.CC = CC
        self.selectionRectangle: SelectionRectangle = None
        self.startGapOffset: int = 0
        self.endGapOffset: int = 0

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
        
        # Draw the selection corners of the selection rectangle
        for corner in self.selectionRectangle.cornersBbox:
            self.selectionRectangle.canvasIdCorners.append(self.CC.view.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas.
        """
        self.CC.view.delete(self.selectionRectangle.canvasIdRectangle)
        for canvasCorner in self.selectionRectangle.canvasIdCorners:
            self.CC.view.delete(canvasCorner)

    def render(self) -> None:
        sr = self.selectionRectangle

        self.CC.view.coords(sr.canvasIdRectangle, sr.topLeft.x, sr.topLeft.y, sr.bottomRight.x,  sr.bottomRight.y)
        
        # Render the corners to the new position
        for i in range(len(self.selectionRectangle.canvasIdCorners)):
            self.CC.view.moveto(self.selectionRectangle.canvasIdCorners[i], self.selectionRectangle.cornersBbox[i].min.x, self.selectionRectangle.cornersBbox[i].min.y)

        # Render the image to the new position
        if self.selectionRectangle.attachedImage:
            self.CC.view.coords(self.selectionRectangle.attachedImage.id, self.selectionRectangle.center.x, self.selectionRectangle.center.y)

    def deleteSelectionRectangle(self) -> None:
        """
        Delete completly the selection rectangle on the canvas.
        (Probs just put deleteSelectionRectangle and deselect together)
        """
        # If there is a attached image in the selection rectangle
        if self.selectionRectangle.attachedImage:
            # Delete the image first
            self.CC.deleteImage(self.selectionRectangle.attachedImage)
        # Deselect from the selection rectangle
        self.deSelect()

    def deSelect(self) -> None:
        """
        Deselect completly the selection rectangle on the canvas.
        """
        # Erase the rendering of the selection rectangle
        self.erase()
        # Completly remove the selection rectangle
        self.selectionRectangle = None
        # Set the cursor to default (arrow)
        self.CC.view.config(cursor="arrow")

    #endregion Public Methods

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
        
        # Check if the mouse is inside the corners bbox
        if self.selectionRectangle.isInsideCorners(mouseCoords):
            self.setAction(SelectionRectangleAction.RESIZE)
        # Check if the mouse is inside the selection rectangle    
        elif self.selectionRectangle.isInside(mouseCoords):
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
            self.startGapOffset: Vector2 = mouseCoords - self.selectionRectangle.min
            self.endGapOffset: Vector2 = mouseCoords - self.selectionRectangle.max

        elif self.getAction() == SelectionRectangleAction.RESIZE and self.selectionRectangle.selectedCornerIndex != -1:
            self.startGapOffset: Vector2 = mouseCoords - self.selectionRectangle.min
            self.endGapOffset: Vector2 = mouseCoords - self.selectionRectangle.max

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
            self.selectionRectangle.setCoords(mouseCoords - self.startGapOffset, mouseCoords - self.endGapOffset)
            
            # Render the selection rectangle to the new position
            self.render()

        elif self.getAction() == SelectionRectangleAction.RESIZE:
            corners = {
                0: "topLeft",
                1: "topRight",
                2: "bottomLeft",
                3: "bottomRight",
            }

            selected_corner = corners.get(self.selectionRectangle.selectedCornerIndex)
            # Set new coordinates for the corner
            if selected_corner:
                setattr(self.selectionRectangle, selected_corner, mouseCoords)

            # Check if 
            if (self.selectionRectangle.ToName()):
                return
            
            self.CC.resizeImage(self.selectionRectangle.attachedImage, self.selectionRectangle.width, self.selectionRectangle.height)
            
            # Render the selection rectangle to the new position
            self.render()

        if DEBUG:
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

        self.update()
        # Render the selection rectangle to the new position
        self.render()

        if DEBUG:
            self.CC.DCC.drawCanvasImageDebugInfos(self.selectionRectangle.attachedImage)

    #endregion Event
