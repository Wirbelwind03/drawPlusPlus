import tkinter as tk

from DrawLibrary.Core.Math.vector2 import Vector2

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.canvasImages import CanvasImages
from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

class SelectionRectangleCanvasController:
    def __init__(self, view: tk.Canvas, model: CanvasImages):
        # Connect the controller to the canvas
        self.view = view
        self.model = model
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
        self.selectionRectangle.canvasIdRectangle = self.view.create_rectangle(self.selectionRectangle.x, self.selectionRectangle.y, self.selectionRectangle.x + self.selectionRectangle.width, self.selectionRectangle.y + self.selectionRectangle.height, outline="black", width=2, dash=(2, 2))
        
        # Draw the selection corners of the selection rectangle
        for corner in self.selectionRectangle.cornersBbox:
            self.selectionRectangle.canvasIdCorners.append(self.view.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        self.view.delete(self.selectionRectangle.canvasIdRectangle)
        for canvasCorner in self.selectionRectangle.canvasIdCorners:
            self.view.delete(canvasCorner)

    def deleteSelectionRectangle(self) -> None:
        if self.selectionRectangle.attachedImage:
            self.model.deleteImage(self.selectionRectangle.attachedImage)
        self.deSelect()

    def deSelect(self) -> None:
        self.erase()
        self.selectionRectangle = None
        self.view.config(cursor="arrow")

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
            self.selectionRectangle.action = SelectionRectangleAction.RESIZE
            self.view.config(cursor="umbrella")
        elif self.selectionRectangle.isInside(mouseCoords):
            # If it is, change that the action we want to do is moving the selection rectangle
            self.selectionRectangle.action = SelectionRectangleAction.MOVE
            self.view.config(cursor="fleur")
        else:
            # If it's not, change that the action we want to do is creating a selection rectangle
            self.selectionRectangle.action = SelectionRectangleAction.NONE
            self.view.config(cursor="arrow")

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

        if self.selectionRectangle.action == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.selectionRectangle.min = mouseCoords + self.startGapOffset
            self.selectionRectangle.max = mouseCoords + self.endGapOffset
            
            # Update the corners coordinates
            corners = [self.selectionRectangle.topLeft, self.selectionRectangle.topRight, self.selectionRectangle.bottomLeft, self.selectionRectangle.bottomRight]
            for i in range(len(self.selectionRectangle.cornersBbox)):
                cornerBbox = self.selectionRectangle.cornersBbox[i]
                cornerBbox.min = corners[i] - self.selectionRectangle.cornerSize
                cornerBbox.max = corners[i] + self.selectionRectangle.cornerSize
            
            # Update the image coordinates
            if self.selectionRectangle.attachedImage:
                self.selectionRectangle.attachedImage.bbox.min = self.selectionRectangle.min
                self.selectionRectangle.attachedImage.bbox.max = self.selectionRectangle.max
    
        elif self.selectionRectangle.action == SelectionRectangleAction.RESIZE:
            #self.selectionRectangle.min = mouseCoords + self.startGapOffset + self.selectionRectangle.cornerSize
            #self.selectionRectangle.max = mouseCoords + self.endGapOffset + self.selectionRectangle.cornerSize
            #self.selectionRectangle.topLeft = mouseCoords + self.startGapOffset + self.selectionRectangle.cornerSize 
            pass

        ## Render the shapes drawn on the canvas
        
        # Render the selection rectangle to the new position
        self.view.moveto(self.selectionRectangle.canvasIdRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
        
        # Render the corners to the new position
        for i in range(len(self.selectionRectangle.canvasIdCorners)):
            self.view.moveto(self.selectionRectangle.canvasIdCorners[i], self.selectionRectangle.cornersBbox[i].min.x, self.selectionRectangle.cornersBbox[i].min.y)
        
        # Render the image to the new position
        if self.selectionRectangle.attachedImage:
            self.view.moveto(self.selectionRectangle.attachedImage.id, self.selectionRectangle.min.x, self.selectionRectangle.min.y)