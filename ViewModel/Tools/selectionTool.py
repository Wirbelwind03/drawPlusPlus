from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from config import DEBUG

from ViewModel.canvasVievModel import CanvasViewModel

from Model.canvasImage import CanvasImage
from Model.selectionRectangle import SelectionRectangle

class Action(Enum):
    NONE = 0
    MOVE = 1

class SelectionTool:
    def __init__(self, canvasViewModel):
        self.canvasViewModel: CanvasViewModel = canvasViewModel
        self.__action = Action.NONE

        self.selectionRectangle : SelectionRectangle = None

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.selectionRectangle:
            if self.selectionRectangle.isInside(mouseCoords):
                self.__action = Action.MOVE
                self.canvasViewModel.canvas.config(cursor="fleur")
            else:
                self.__action = Action.NONE
                self.canvasViewModel.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.selectionRectangle:
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.selectionRectangle and self.selectionRectangle.isOutside(mouseCoords):
            self.canvasViewModel.canvas.delete(self.selectionRectangle.canvasRectangle)
            self.selectionRectangle = None
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.__action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.selectionRectangle.on_button_press(event)
            return

                
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.__action == Action.MOVE:
            self.selectionRectangle.on_mouse_drag(event)
            self.canvasViewModel.canvas.moveto(self.selectionRectangle.canvasRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            self.canvasViewModel.canvas.moveto(self.selectionRectangle.attachedImage.id, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            if DEBUG:
                self.canvasViewModel.canvas.moveto(self.selectionRectangle.attachedImage._debugBbox, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        self.__action = Action.NONE

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.canvasViewModel.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.selectionRectangle = SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y)
                self.selectionRectangle.canvasRectangle = self.canvasViewModel.canvas.create_rectangle(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y, outline="black", width=2, dash=(2, 2))
                self.selectionRectangle.attachedImage = image

                # Check the action to move since the cursor is inside the image
                self.__action = Action.MOVE
                self.canvasViewModel.canvas.config(cursor="fleur")
                return


