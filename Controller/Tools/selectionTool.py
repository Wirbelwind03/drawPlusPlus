import tkinter as tk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2

from Controller.canvasController import CanvasController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class SelectionTool:
    def __init__(self, CC: CanvasController, SRCC: SelectionRectangleCanvasController):
        # Connect the selection rectangle controller to the canvas
        self.CC = CC
        self.SRCC = SRCC

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle():
            self.SRCC.on_mouse_over(event)

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.SRCC.hasSelectionRectangle():
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.SRCC.hasSelectionRectangle() and self.SRCC.selectionRectangle.isOutside(mouseCoords):
            self.SRCC.deSelect()
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
           
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            self.SRCC.on_mouse_drag(event)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        if self.SRCC.hasSelectionRectangle():
            self.SRCC.setAction(SelectionRectangleAction.NONE)

    def on_delete(self, event):
        if self.SRCC.hasSelectionRectangle():
            self.SRCC.deleteSelectionRectangle()

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.CC.model.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y), image)
                self.SRCC.draw()

                # Check the action to move since the cursor is inside the image
                self.SRCC.setAction(SelectionRectangleAction.MOVE)
                self.CC.view.config(cursor="fleur")
                return


