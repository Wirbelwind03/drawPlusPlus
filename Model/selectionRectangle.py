import tkinter as tk

from enum import Enum

from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Core.Math.vector2 import Vector2

from Model.canvasImage import CanvasImage

class SelectionRectangleAction(Enum):
    NONE = 0
    MOVE = 1
    RESIZE = 2

class SelectionRectangle(AABB):
    def __init__(self, *args, cornerSize=10, cornerCanvasSize=5, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.startGapOffset = 0
        self.endGapOffset = 0
        
        self.cornerSize = cornerSize
        self.cornerCanvasSize = cornerCanvasSize

        self.cornersBbox = []
        
        self.canvasIdRectangle = -1
        self.canvasIdCorners = []
        self.attachedImage: CanvasImage = None

        self.action = SelectionRectangleAction.NONE

    @classmethod
    def fromCoordinates(cls, x1, y1, x2, y2, cornerSize=10, cornerCanvasSize=5) -> 'SelectionRectangle':
        instance: 'SelectionRectangle' =  super().fromCoordinates(x1, y1, x2, y2)
        instance.cornerSize = cornerSize
        instance.cornerCanvasSize = cornerCanvasSize
        instance.initializeCorners()
        return instance
    
    def initializeCorners(self) -> None:
        corners = [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
        for i in range(len(corners)):
            self.cornersBbox.append(AABB.fromCoordinates(corners[i].x - self.cornerSize, corners[i].y - self.cornerSize, corners[i].x + self.cornerSize, corners[i].y + self.cornerSize)) 
    
    def isInsideCorners(self, coords: Vector2) -> bool:
        for corner in self.cornersBbox:
            if corner.isInside(coords):
                return True
        return False

    def draw(self, canvas: tk.Canvas) -> None:
        """
        Draw a selection rectangle on a canvas

        Parameters:
        -----------
        canvas : tk.Canvas
        """
        # Draw the main frame of the selection rectangle
        self.canvasIdRectangle = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, outline="black", width=2, dash=(2, 2))
        
        # Draw the selection corners of the selection rectangle
        for corner in self.cornersBbox:
            self.canvasIdCorners.append(canvas.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self, canvas: tk.Canvas) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas

        Parameters:
        -----------
        event : 
        """
        canvas.delete(self.canvasIdRectangle)
        for canvasCorner in self.canvasIdCorners:
            canvas.delete(canvasCorner)

    def on_mouse_over(self, event, canvas: tk.Canvas) -> None:
        """
        A event for when the mouse is hovering on the selection rectangle

        Parameters:
        -----------
        event : 
        """
        mouseCoords = Vector2(event.x, event.y)

        if self.isInside(mouseCoords):
            if (self.isInsideCorners(mouseCoords)):
                self.action = SelectionRectangleAction.RESIZE
                canvas.config(cursor="arrow")
                return

            # If it is, change that the action we want to do is moving the selection rectangle
            self.action = SelectionRectangleAction.MOVE
            canvas.config(cursor="fleur")
        else:
            if (self.isInsideCorners(mouseCoords)):
                self.action = SelectionRectangleAction.RESIZE
                canvas.config(cursor="arrow")
                return

            # If it's not, change that the action we want to do is creating a selection rectangle
            self.action = SelectionRectangleAction.NONE
            canvas.config(cursor="arrow")

    def on_button_press(self, event):
        """
        A event for when a left click occur on the selection rectangle

        Parameters:
        -----------
        event : 
        """
        mouseCoords = Vector2(event.x, event.y)

        if self.action == SelectionRectangleAction.MOVE:
            # Get the gap between the cursor and the min and max of the AABB
            # So the user can move the rectangle by clicking anywhere inside
            self.startGapOffset = self.min - mouseCoords
            self.endGapOffset = self.max - mouseCoords

    def on_mouse_drag(self, event, canvas: tk.Canvas):
        """
        A event for when the user drag the selection rectangle

        Parameters:
        -----------
        event : 
        """
        mouseCoords = Vector2(event.x, event.y)

        if self.action == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.min = mouseCoords + self.startGapOffset
            self.max = mouseCoords + self.endGapOffset
            
            # Update the corners coordinates
            corners = [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
            for i in range(len(self.cornersBbox)):
                cornerBbox = self.cornersBbox[i]
                cornerBbox.min = corners[i] - self.cornerSize
                cornerBbox.max = corners[i] + self.cornerSize
            
            # Update the image coordinates
            if self.attachedImage:
                self.attachedImage.bbox.min = self.min
                self.attachedImage.bbox.max = self.max

            # Move the shapes drawn on the canvas
            
            # Draw the selection rectangle to the new position
            canvas.moveto(self.canvasIdRectangle, self.min.x, self.min.y)
            
            # Draw the corners to the new position
            for i in range(len(self.canvasIdCorners)):
                canvas.moveto(self.canvasIdCorners[i], self.cornersBbox[i].min.x, self.cornersBbox[i].min.y)
            
            # Draw the image to the new position
            if self.attachedImage:
                canvas.moveto(self.attachedImage.id, self.min.x, self.min.y)
    