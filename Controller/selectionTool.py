import tkinter as tk
from PIL import Image

from enum import Enum

from Core.Math.vector2 import Vector2
from Core.Shapes.rectangle import Rectangle

class Action(Enum):
    CREATE = 0
    MOVE = 1

class SelectionTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.boundingBox = Rectangle()
        self.canvasSelectionRectangle = None
        self.action = Action.CREATE

    def on_mouse_over(self, event):
        if self.canvasSelectionRectangle:
            # Check if the cursor is inside the selection rectangle
            if event.x > self.boundingBox.startCoordinates.x and event.x < self.boundingBox.endCoordinates.x and event.y > self.boundingBox.startCoordinates.y and event.y < self.boundingBox.endCoordinates.y:
                self.action = Action.MOVE
                self.canvas.config(cursor="fleur")

            else:
                self.action = Action.CREATE
                self.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.gap_offset = self.boundingBox.startCoordinates - mouseCoordinates
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.canvasSelectionRectangle:
            self.canvas.delete(self.canvasSelectionRectangle)

        # Save the starting point for the rectangle
        self.boundingBox.startCoordinates = mouseCoordinates

        # Create a rectangle (but don't specify the end point yet)
        self.canvasSelectionRectangle = self.canvas.create_rectangle(self.boundingBox.startCoordinates.x, self.boundingBox.startCoordinates.y, self.boundingBox.startCoordinates.x, self.boundingBox.startCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.boundingBox.startCoordinates = mouseCoordinates + self.gap_offset
            self.canvas.moveto(self.canvasSelectionRectangle, self.boundingBox.startCoordinates.x, self.boundingBox.startCoordinates.y)
            return

        # Update the rectangle as the mouse is dragged
        # Modify the coordinates of the rectangle
        self.canvas.coords(self.canvasSelectionRectangle, self.boundingBox.startCoordinates.x, self.boundingBox.startCoordinates.y, mouseCoordinates.x, mouseCoordinates.y)

    def on_button_release(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.boundingBox.endCoordinates = Vector2(self.boundingBox.startCoordinates.x + self.boundingBox.width, self.boundingBox.startCoordinates.y + self.boundingBox.height)
            return

        # On release, finalize the rectangle selection
        self.boundingBox.endCoordinates = mouseCoordinates

        self.boundingBox.width = self.boundingBox.endCoordinates.x - self.boundingBox.startCoordinates.x
        self.boundingBox.height = self.boundingBox.endCoordinates.y - self.boundingBox.startCoordinates.y