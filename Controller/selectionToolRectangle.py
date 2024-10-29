import tkinter as tk
from PIL import Image

from enum import Enum

from Core.Math.vector2 import Vector2
from Core.Collision.aabb import AABB

class Action(Enum):
    CREATE = 0
    MOVE = 1
    RESIZE = 2
    ROTATE = 3

class SelectionToolRectangle:
    """
    A class for the selection tool used in the canvas.

    Attributes:
    -----------
    __canvas : tk.Canvas
        The canvas widget where the selection tool is used
    bbox : Rectangle
        A rectangle called Bounding Box that define the minimum and maximum coordinates
    _canvasSelectionRectangle : int
        The ID of the rectangle drawn on the Canvas
    _action : Action
        What the user want to do with the selection tool, like deleting, moving, etc.
    """

    def __init__(self, canvas: tk.Canvas):
        self.bbox = AABB()

        self.__canvas = canvas
        
        self._canvasSelectionRectangle = None
        self._debugBbox = None
        self._action = Action.CREATE

        self._startGapOffset = 0
        self._endGapOffset = 0
        
    def createDebugBbox(self):
        if self._debugBbox:
            self.__canvas.delete(self._debugBbox)

        self._debugBbox = self.__canvas.create_rectangle(self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, self.bbox.endCoordinates.x, self.bbox.endCoordinates.y, outline="black", width=2)

    def on_mouse_over(self, event):
        """
        A event for when the mouse is over the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._canvasSelectionRectangle:
            # Check if the cursor is inside the selection rectangle
            if self.bbox.isInside(mouseCoords):
                # If it is, change that the action we want to do is moving the selection rectangle
                self._action = Action.MOVE
                self.__canvas.config(cursor="fleur")
            else:
                # If it's not, change that the action we want to do is creating a selection rectangle
                self._action = Action.CREATE
                self.__canvas.config(cursor="arrow")

    def on_button_press(self, event):
        """
        A event for when the user left click on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self._startGapOffset = self.bbox.startCoordinates - mouseCoords
            self._endGapOffset = self.bbox.endCoordinates - mouseCoords
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self._canvasSelectionRectangle:
            self.__canvas.delete(self._canvasSelectionRectangle)

        # Save the starting point for the rectangle
        self.bbox.startCoordinates = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self._canvasSelectionRectangle = self.__canvas.create_rectangle(self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        """
        A event for when the mouse is dragged over on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            # Update the coordinates and move the selection rectangle
            self.bbox.startCoordinates = mouseCoords + self._startGapOffset
            self.bbox.endCoordinates = mouseCoords + self._endGapOffset
            self.__canvas.moveto(self._canvasSelectionRectangle, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y)
            return

        # Update the rectangle as the mouse is dragged
        self.__canvas.coords(self._canvasSelectionRectangle, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, mouseCoords.x, mouseCoords.y)

    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            self.createDebugBbox()
            return

        # On release, finalize the rectangle selection by setting its end coordinates
        self.bbox.endCoordinates = mouseCoords

        # Check if the origin is at the top left, if its isn't, change it to that
        self.bbox.changeOriginToTopLeft()

        self.createDebugBbox()

    def on_control_x(self, event):

        
        selectionToolRectangleBbox = self.bbox
        
        for imageId, image in self.__canvas.canvasImagesManager.images.items():
            # check overlap with image and selection tool
            if selectionToolRectangleBbox.isIntersecting(image.bbox):
                x1 = max(selectionToolRectangleBbox.topLeft.x, image.bbox.topLeft.x)
                y1 = max(selectionToolRectangleBbox.topRight.y, image.bbox.topRight.y)
                x2 = min(selectionToolRectangleBbox.topRight.x, image.bbox.topRight.x)
                y2 = min(selectionToolRectangleBbox.bottomRight.y, image.bbox.bottomRight.y)
                #intersectRectangle = selectionToolBbox.getIntersectRectangle(canvasImage.bbox)
                image.cutImage(x1, y1, x2 - x1, y2 - y1)
                self.__canvas.canvasImagesManager.update()
                #self.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
                
        self.delete(self.selectionToolRectangle._debugBbox)