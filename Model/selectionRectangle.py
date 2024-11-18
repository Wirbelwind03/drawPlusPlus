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
    """
    A class representing a selection rectangle (like the tool used in Paint)

    Attributes
    -----------
    canvasIdRectangle : int
        The ID of the rectangle rendered on a tk.Canvas, and is used to render the selection rectangle
    canvasIdCorners : list
        The IDs of the rectangles rendered on a tk.Canvas, and is used to render the corners of the selection rectangle
    attachedImage : CanvasImage
        The image attached to the selection rectangle
    action : SelectionRectangleAction
        The action the user is going to do with the selection rectangle
    """

    def __init__(self, *args, cornerSize: int=10, cornerCanvasSize:int =5, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.startGapOffset: int = 0
        self.endGapOffset: int = 0
        
        self.cornerSize: int = cornerSize
        self.cornerCanvasSize: int = cornerCanvasSize

        self.cornersBbox = []
        
        self.canvasIdRectangle: int = -1
        self.canvasIdCorners: list = []
        self.attachedImage: CanvasImage = None

        self.action: SelectionRectangleAction = SelectionRectangleAction.NONE

    @classmethod
    def fromCoordinates(cls, x1: int, y1: int, x2: int, y2: int, cornerSize: int=10, cornerCanvasSize: int=5) -> 'SelectionRectangle':
        """
        Create a SelectionRectangle from start and end coordinates
        The function also take the corner size as argument

        Parameters
        --------
        x1 : int
            The x start coordinate of the rectangle
        y1 : int
            The y start coordinate of the rectangle
        x2 : int
            The x end coordinate of the rectangle
        y2 : int
            The y end coordinate of the rectangle
        cornerSize : int
            The size of the corner, where the program is going to detect collision
        cornerCanvasSize : int
            The size of the corner rendered on the canvas

        Returns
        --------
        SelectionRectangle
            The new SelectionRectangle created from the arguments
        """
        instance: 'SelectionRectangle' =  super().fromCoordinates(x1, y1, x2, y2)
        instance.cornerSize = cornerSize
        instance.cornerCanvasSize = cornerCanvasSize
        instance.initializeCorners()
        return instance
    
    def initializeCorners(self) -> None:
        """
        Construct the corners rectangle of the selection rectangle
        """
        corners = [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
        for i in range(len(corners)):
            self.cornersBbox.append(AABB.fromCoordinates(corners[i].x - self.cornerSize, corners[i].y - self.cornerSize, corners[i].x + self.cornerSize, corners[i].y + self.cornerSize)) 
    
    def isInsideCorners(self, coords: Vector2) -> bool:
        """
        Check if a coordinates is inside the corners of the selection rectangle

        Parameters
        -----------
        coords : Vector2
            The coords that is going to be checked for every corner

        Return
        -----------
        bool
            Boolean if the coords are inside the corners
        """
        for corner in self.cornersBbox:
            if corner.isInside(coords):
                return True
        return False

    def draw(self, canvas: tk.Canvas) -> None:
        """
        Draw a selection rectangle on a canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection is going to be drawn
        """
        # Draw the main frame of the selection rectangle
        self.canvasIdRectangle = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, outline="black", width=2, dash=(2, 2))
        
        # Draw the selection corners of the selection rectangle
        for corner in self.cornersBbox:
            self.canvasIdCorners.append(canvas.create_rectangle(corner.x, corner.y, corner.x + corner.width, corner.y + corner.height, outline="black", width=2))

    def erase(self, canvas: tk.Canvas) -> None:
        """
        Erase all the drawn shapes tied to the selection rectangle on the canvas

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
        """
        canvas.delete(self.canvasIdRectangle)
        for canvasCorner in self.canvasIdCorners:
            canvas.delete(canvasCorner)

    def on_mouse_over(self, event, canvas: tk.Canvas) -> None:
        """
        A event for when the mouse is hovering on the selection rectangle

        Parameters
        -----------
        event : 
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
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

        Parameters
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

        Parameters
        -----------
        event : 
        canvas : tk.Canvas
            The canvas where the selection rectangle is drawn
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

            ## Render the shapes drawn on the canvas
            
            # Render the selection rectangle to the new position
            canvas.moveto(self.canvasIdRectangle, self.min.x, self.min.y)
            
            # Render the corners to the new position
            for i in range(len(self.canvasIdCorners)):
                canvas.moveto(self.canvasIdCorners[i], self.cornersBbox[i].min.x, self.cornersBbox[i].min.y)
            
            # Render the image to the new position
            if self.attachedImage:
                canvas.moveto(self.attachedImage.id, self.min.x, self.min.y)
    