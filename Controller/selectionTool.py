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
        self.start = None
        self.end = None
        self.width = None
        self.height = None
        self.canvasSelectionRectangle = None
        self.action = Action.CREATE

        # Bind mouse events to canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_mouse_over)

    def on_mouse_over(self, event):
        if self.canvasSelectionRectangle:
            # Check if the cursor is inside the selection rectangle
            if event.x > self.start.x and event.x < self.end.x and event.y > self.start.y and event.y < self.end.y:
                self.action = Action.MOVE
                self.canvas.config(cursor="fleur")

            else:
                self.action = Action.CREATE
                self.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.gap_offset = self.start - mouseCoordinates
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.canvasSelectionRectangle:
            self.canvas.delete(self.canvasSelectionRectangle)

        # Save the starting point for the rectangle
        self.start = mouseCoordinates

        # Create a rectangle (but don't specify the end point yet)
        self.canvasSelectionRectangle = self.canvas.create_rectangle(self.start.x, self.start.y, self.start.x, self.start.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.start = mouseCoordinates + self.gap_offset
            self.canvas.moveto(self.canvasSelectionRectangle, self.start.x, self.start.y)
            return

        # Update the rectangle as the mouse is dragged
        # Modify the coordinates of the rectangle
        self.canvas.coords(self.canvasSelectionRectangle, self.start.x, self.start.y, mouseCoordinates.x, mouseCoordinates.y)

    def on_button_release(self, event):
        mouseCoordinates = Vector2(event.x, event.y)

        if self.action == Action.MOVE:
            self.end = Vector2(self.start.x + self.width, self.start.y + self.height)
            return

        # On release, finalize the rectangle selection
        self.end = mouseCoordinates

        self.width = self.end.x - self.start.x
        self.height = self.end.y - self.start.y