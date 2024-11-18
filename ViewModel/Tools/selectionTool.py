from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from config import DEBUG

from ViewModel.canvasVievModel import CanvasViewModel
from ViewModel.selectionRectangleCanvasViewModel import SelectionRectangleCanvasViewModel

from Model.canvasImage import CanvasImage
from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class SelectionTool:
    def __init__(self, canvasViewModel):
        self.CVM: CanvasViewModel = canvasViewModel
        self.SRCVM: SelectionRectangleCanvasViewModel = SelectionRectangleCanvasViewModel(self.CVM)

        self.selectionRectangle : SelectionRectangle = None

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.selectionRectangle:
            self.selectionRectangle.on_mouse_over(event, self.CVM.canvas)

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.selectionRectangle:
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.selectionRectangle and self.selectionRectangle.isOutside(mouseCoords):
            self.selectionRectangle.erase(self.CVM.canvas)
            self.selectionRectangle = None
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.selectionRectangle and self.selectionRectangle.action == SelectionRectangleAction.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.selectionRectangle.on_button_press(event)
            return
           
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.selectionRectangle and self.selectionRectangle.action == SelectionRectangleAction.MOVE:
            self.selectionRectangle.on_mouse_drag(event, self.CVM.canvas)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        self.selectionRectangle.action = SelectionRectangleAction.NONE

    def on_delete(self, event):
        if self.selectionRectangle:
            if self.selectionRectangle.attachedImage:
                self.CVM.deleteImage(self.selectionRectangle.attachedImage)
            self.selectionRectangle.erase(self.CVM.canvas)

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.CVM.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.selectionRectangle = SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y)
                self.selectionRectangle.draw(self.CVM.canvas)
                self.selectionRectangle.attachedImage = image

                # Check the action to move since the cursor is inside the image
                self.selectionRectangle.action = SelectionRectangleAction.NONE
                self.CVM.canvas.config(cursor="fleur")
                return


