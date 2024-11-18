import tkinter as tk

from DrawLibrary.Core.Math.vector2 import Vector2

from ViewModel.canvasVievModel import CanvasViewModel

from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

class SelectionRectangleCanvasViewModel:
    def __init__(self, canvasViewModel):
        self.CVM: CanvasViewModel = canvasViewModel
        self.selectionRectangle = None

    def setSelectionRectangle(self, selectionRectangle: SelectionRectangle) -> None:
        self.selectionRectangle = selectionRectangle

    def hasSelectionRectangle(self) -> bool:
        return self.selectionRectangle is not None
    
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
        self.selectionRectangle.canvasIdRectangle = self.CVM.canvas.create_rectangle(self.selectionRectangle.x, self.selectionRectangle.y, self.selectionRectangle.x + self.selectionRectangle.width, self.selectionRectangle.y + self.selectionRectangle.height, outline="black", width=2, dash=(2, 2))
        
        # Draw the selection corners of the selection rectangle
        for corner in self.selectionRectangle.cornersBbox:
            self.selectionRectangle.canvasIdCorners.append(self.CVM.canvas.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        self.CVM.canvas.delete(self.selectionRectangle.canvasIdRectangle)
        for canvasCorner in self.selectionRectangle.canvasIdCorners:
            self.CVM.canvas.delete(canvasCorner)

    def delete(self) -> None:
        if self.selectionRectangle.attachedImage:
            self.CVM.deleteImage(self.selectionRectangle.attachedImage)
        self.deSelect()

    def deSelect(self) -> None:
        self.selectionRectangle.erase(self.CVM.canvas)
        self.selectionRectangle = None
        self.CVM.canvas.config(cursor="arrow")

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

        if self.selectionRectangle.isInside(mouseCoords):
            if (self.selectionRectangle.isInsideCorners(mouseCoords)):
                self.selectionRectangle.action = SelectionRectangleAction.RESIZE
                self.CVM.canvas.config(cursor="arrow")
                return

            # If it is, change that the action we want to do is moving the selection rectangle
            self.selectionRectangle.action = SelectionRectangleAction.MOVE
            self.CVM.canvas.config(cursor="fleur")
        else:
            if (self.selectionRectangle.isInsideCorners(mouseCoords)):
                self.selectionRectangle.action = SelectionRectangleAction.RESIZE
                self.CVM.canvas.config(cursor="arrow")
                return

            # If it's not, change that the action we want to do is creating a selection rectangle
            self.selectionRectangle.action = SelectionRectangleAction.NONE
            self.CVM.canvas.config(cursor="arrow")

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

        if self.selectionRectangle.action == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.selectionRectangle.min = mouseCoords + self.startGapOffset
            self.selectionRectangle.max = mouseCoords + self.endGapOffset
            
            # Update the corners coordinates
            corners = [self.selectionRectangle.topLeft, self.selectionRectangle.topRight, self.selectionRectangle.bottomLeft, self.selectionRectangle.bottomRight]
            for i in range(len(self.selectionRectangle.cornersBbox)):
                cornerBbox = self.selectionRectangle.cornersBbox[i]
                cornerBbox.min = corners[i] - self.cornerSize
                cornerBbox.max = corners[i] + self.cornerSize
            
            # Update the image coordinates
            if self.selectionRectangle.attachedImage:
                self.selectionRectangle.attachedImage.bbox.min = self.selectionRectangle.min
                self.selectionRectangle.attachedImage.bbox.max = self.selectionRectangle.max

            ## Render the shapes drawn on the canvas
            
            # Render the selection rectangle to the new position
            self.CVM.canvas.moveto(self.selectionRectangle.canvasIdRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            
            # Render the corners to the new position
            for i in range(len(self.selectionRectangle.canvasIdCorners)):
                self.CVM.canvas.moveto(self.selectionRectangle.canvasIdCorners[i], self.selectionRectangle.cornersBbox[i].min.x, self.selectionRectangle.cornersBbox[i].min.y)
            
            # Render the image to the new position
            if self.selectionRectangle.attachedImage:
                self.CVM.canvas.moveto(self.selectionRectangle.attachedImage.id, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
    