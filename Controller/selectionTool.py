import tkinter as tk
from PIL import Image

from enum import Enum

from Core.Math.vector2 import Vector2
from Core.Shapes.rectangle import Rectangle

class Action(Enum):
    CREATE = 0
    MOVE = 1

class SelectionTool:
    """
    A class for the selection tool used in the canvas.

    Attributes:
    -----------
    canvas : Canvas
        The canvas widget where the selection tool is used
    bbox : Rectangle
        A rectangle called Bounding Box that define the minimum and maximum coordinates
    canvasSelectionRectangle : int
        The ID of the rectangle drawn on the Canvas
    action : Action
        What the user want to do with the selection tool, like deleting, moving, etc.
    """

    def __init__(self, canvas):
        self.canvas = canvas
        self.bbox = Rectangle()
        self.canvasSelectionRectangle = None
        self.action = Action.CREATE

    def on_mouse_over(self, event):
        if self.canvasSelectionRectangle:
            # Check if the cursor is inside the selection rectangle
            if event.x > self.bbox.startCoordinates.x and event.x < self.bbox.endCoordinates.x and event.y > self.bbox.startCoordinates.y and event.y < self.bbox.endCoordinates.y:
                self.action = Action.MOVE
                self.canvas.config(cursor="fleur")

            else:
                self.action = Action.CREATE
                self.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.gap_offset = self.bbox.startCoordinates - mouseCoordinates
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.canvasSelectionRectangle:
            self.canvas.delete(self.canvasSelectionRectangle)

        # Save the starting point for the rectangle
        self.bbox.startCoordinates = mouseCoordinates

        # Create a rectangle (but don't specify the end point yet)
        self.canvasSelectionRectangle = self.canvas.create_rectangle(self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        # Modify the coordinates of the rectangle
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.bbox.startCoordinates = mouseCoordinates + self.gap_offset
            self.canvas.moveto(self.canvasSelectionRectangle, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y)
            return

        # Update the rectangle as the mouse is dragged
        self.canvas.coords(self.canvasSelectionRectangle, self.bbox.startCoordinates.x, self.bbox.startCoordinates.y, mouseCoordinates.x, mouseCoordinates.y)

    def on_button_release(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.bbox.endCoordinates = Vector2(self.bbox.startCoordinates.x + self.bbox.width, self.bbox.startCoordinates.y + self.bbox.height)
            return

        # On release, finalize the rectangle selection
        self.bbox.endCoordinates = mouseCoordinates

        self.bbox.width = self.bbox.endCoordinates.x - self.bbox.startCoordinates.x
        self.bbox.height = self.bbox.endCoordinates.y - self.bbox.startCoordinates.y