import tkinter as tk

from Controller.canvasController import CanvasController

from DrawLibrary.Core.Math.vector2 import Vector2
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
            self.startGapOffset = self.selectionRectangle.min - mouseCoords
            self.endGapOffset = self.selectionRectangle.max - mouseCoords

        elif self.selectionRectangle.action == SelectionRectangleAction.RESIZE:
            self.startGapOffset = self.selectionRectangle.selectedCorner.min - mouseCoords
            self.endGapOffset = self.selectionRectangle.selectedCorner.max - mouseCoords

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
            self.selectionRectangle.min = mouseCoords + self.startGapOffset
            self.selectionRectangle.max = mouseCoords + self.endGapOffset
            
            # Update the corners coordinates
            corners = [self.selectionRectangle.topLeft, self.selectionRectangle.topRight, self.selectionRectangle.bottomLeft, self.selectionRectangle.bottomRight]
            for i in range(len(self.selectionRectangle.cornersBbox)):
                cornerBbox = self.selectionRectangle.cornersBbox[i]
                cornerBbox.min = corners[i] - self.selectionRectangle.cornerSize
                cornerBbox.max = corners[i] + self.selectionRectangle.cornerSize
            
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
            self.selectionRectangle.max = mouseCoords - self.selectionRectangle.cornerSize
            #self.CC.view.moveto(self.selectionRectangle.canvasIdCorners[2], self.selectionRectangle.bottomLeft.x - self.selectionRectangle.cornerSize, self.selectionRectangle.bottomRight.y - self.selectionRectangle.cornerSize)
            self.CC.view.coords(self.selectionRectangle.canvasIdRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y, mouseCoords.x - self.selectionRectangle.cornerSize, mouseCoords.y - self.selectionRectangle.cornerSize)
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
            self.selectionRectangle.max = mouseCoords - self.selectionRectangle.cornerSize
            self.CC.view.create_rectangle(self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.max.x, self.selectionRectangle.max.y, outline="black", width=2)
            pass

