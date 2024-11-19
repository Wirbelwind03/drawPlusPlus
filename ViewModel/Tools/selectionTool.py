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

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCVM.hasSelectionRectangle():
            self.SRCVM.on_mouse_over(event)

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.SRCVM.hasSelectionRectangle():
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.SRCVM.hasSelectionRectangle() and self.SRCVM.selectionRectangle.isOutside(mouseCoords):
            self.SRCVM.deSelect()
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.SRCVM.hasSelectionRectangle() and self.SRCVM.getAction() == SelectionRectangleAction.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCVM.on_button_press(event)
            return
           
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCVM.hasSelectionRectangle() and self.SRCVM.getAction() == SelectionRectangleAction.MOVE:
            self.SRCVM.on_mouse_drag(event)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        if self.SRCVM.hasSelectionRectangle():
            self.SRCVM.setAction(SelectionRectangleAction.NONE)

    def on_delete(self, event):
        if self.SRCVM.hasSelectionRectangle():
            self.SRCVM.deleteSelectionRectangle()

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.CVM.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.SRCVM.setSelectionRectangle(SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y), image)
                self.SRCVM.draw()

                # Check the action to move since the cursor is inside the image
                self.SRCVM.setAction(SelectionRectangleAction.MOVE)
                self.CVM.canvas.config(cursor="fleur")
                return


