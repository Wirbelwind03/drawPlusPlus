import tkinter as tk

from Controller.canvasController import CanvasController

from DrawLibrary.Core.Shapes.rectangle import RectangleCorners
from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.canvasEntities import CanvasEntities
from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

class SelectionRectangleCanvasController:
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
        return self.selectionRectangle is not None
    
    def setAction(self, action: SelectionRectangleAction) -> None:
        self.selectionRectangle.action = action
        if self.getAction() == SelectionRectangleAction.RESIZE:
            self.CC.view.config(cursor="umbrella")
        elif self.getAction() == SelectionRectangleAction.MOVE:
            self.CC.view.config(cursor="fleur")
        else:
            self.CC.view.config(cursor="arrow")

    def getAction(self) -> SelectionRectangleAction:
        return self.selectionRectangle.action
    
    def draw(self) -> None:
        """
        Draw a selection rectangle on a canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection is going to be drawn
        """
        # Draw the main frame of the selection rectangle
        self.selectionRectangle.canvasIdRectangle = self.CC.view.create_rectangle(self.selectionRectangle.x, self.selectionRectangle.y, self.selectionRectangle.x + self.selectionRectangle.width, self.selectionRectangle.y + self.selectionRectangle.height, outline="black", width=2, dash=(2, 2))
        
        # Draw the selection corners of the selection rectangle
        for corner in self.selectionRectangle.cornersBbox:
            self.selectionRectangle.canvasIdCorners.append(self.CC.view.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        self.CC.view.delete(self.selectionRectangle.canvasIdRectangle)
        for canvasCorner in self.selectionRectangle.canvasIdCorners:
            self.CC.view.delete(canvasCorner)

    def deleteSelectionRectangle(self) -> None:
        if self.selectionRectangle.attachedImage:
            self.CC.deleteImage(self.selectionRectangle.attachedImage)
        self.deSelect()

    def deSelect(self) -> None:
        self.erase()
        self.selectionRectangle = None
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
        
        if self.selectionRectangle.isInsideCorners(mouseCoords):
            self.setAction(SelectionRectangleAction.RESIZE)
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

        if self.selectionRectangle.action == SelectionRectangleAction.MOVE:
            # Get the gap between the cursor and the min and max of the AABB
            # So the user can move the rectangle by clicking anywhere inside
            self.startGapOffset = mouseCoords - self.selectionRectangle.min
            self.endGapOffset = mouseCoords - self.selectionRectangle.max

        elif self.selectionRectangle.action == SelectionRectangleAction.RESIZE and self.selectionRectangle.selectedCornerIndex != -1:
            selectedCorner: AABB = self.selectionRectangle.cornersBbox[self.selectionRectangle.selectedCornerIndex]
            self.startGapOffset = mouseCoords - self.selectionRectangle.min
            self.endGapOffset = mouseCoords - self.selectionRectangle.max

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

        if self.getAction() == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.selectionRectangle.min = mouseCoords - self.startGapOffset
            self.selectionRectangle.max = mouseCoords - self.endGapOffset
            
            ## Render the shapes drawn on the canvas
            
            # Render the selection rectangle to the new position
            self.CC.view.moveto(self.selectionRectangle.canvasIdRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            
            # Render the corners to the new position
            for i in range(len(self.selectionRectangle.canvasIdCorners)):
                self.CC.view.moveto(self.selectionRectangle.canvasIdCorners[i], self.selectionRectangle.cornersBbox[i].min.x, self.selectionRectangle.cornersBbox[i].min.y)
            
            # Render the image to the new position
            if self.selectionRectangle.attachedImage:
                self.CC.view.moveto(self.selectionRectangle.attachedImage.id, self.selectionRectangle.min.x, self.selectionRectangle.min.y)

            return
            
        elif self.getAction() == SelectionRectangleAction.RESIZE:
            corners = {
                0: "topLeft",
                1: "topRight",
                2: "bottomLeft",
                3: "bottomRight",
            }

            # if self.selectionRectangle.min.x >= self.selectionRectangle.max.x or self.selectionRectangle.max.y <= self.selectionRectangle.min.y:
            #     return

            selected_corner = corners.get(self.selectionRectangle.selectedCornerIndex)
            if selected_corner:
                setattr(self.selectionRectangle, selected_corner, mouseCoords)

            if (self.selectionRectangle.ToName()):
                return

            self.CC.view.coords(self.selectionRectangle.canvasIdRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.max.x,  self.selectionRectangle.max.y)
            
            # Render the corners to the new position
            for i in range(len(self.selectionRectangle.canvasIdCorners)):
                self.CC.view.moveto(self.selectionRectangle.canvasIdCorners[i], self.selectionRectangle.cornersBbox[i].min.x, self.selectionRectangle.cornersBbox[i].min.y)

            # Render the image to the new position
            if self.selectionRectangle.attachedImage:
                self.CC.view.moveto(self.selectionRectangle.attachedImage.id, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
                # Render the image resizing in the selection rectangle
                self.selectionRectangle.attachedImage.resize(self.selectionRectangle.max.x - self.selectionRectangle.min.x, self.selectionRectangle.max.y - self.selectionRectangle.min.y)
                self.CC.view.itemconfig(self.selectionRectangle.attachedImage.id, image=self.selectionRectangle.attachedImage.photoImage)

            return
        
    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.getAction() == SelectionRectangleAction.RESIZE:
            self.CC.view.create_rectangle(self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.max.x, self.selectionRectangle.max.y, outline="black", width=2)
            pass

    #endregion Event
