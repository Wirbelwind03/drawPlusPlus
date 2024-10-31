from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from config import DEBUG

from Model.canvasImage import CanvasImage

class Action(Enum):
    NONE = 0
    MOVE = 1

class SelectionTool:
    def __init__(self, canvas):
        self.__canvas = canvas
        self._action = Action.NONE

        self.selectedImage: CanvasImage = None
        self._canvasSelectedRectangle = -1

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.selectedImage:
            if self.selectedImage.bbox.isInside(mouseCoords):
                self._action = Action.MOVE
                self.__canvas.config(cursor="fleur")
            else:
                self._action = Action.NONE
                self.__canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.selectedImage:
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.selectedImage and self.selectedImage.bbox.isOutside(mouseCoords):
            self.__canvas.delete(self._canvasSelectedRectangle)
            self.selectedImage = None
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self._action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self._startGapOffset = self.selectedImage.bbox.min - mouseCoords
            self._endGapOffset = self.selectedImage.bbox.max - mouseCoords
            return

                
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            self.selectedImage.bbox.min = mouseCoords + self._startGapOffset
            self.selectedImage.bbox.max = mouseCoords + self._endGapOffset
            self.__canvas.moveto(self._canvasSelectedRectangle, self.selectedImage.bbox.min.x, self.selectedImage.bbox.min.y)
            self.__canvas.moveto(self.selectedImage.id, self.selectedImage.bbox.min.x, self.selectedImage.bbox.min.y)
            if DEBUG:
                self.__canvas.moveto(self.selectedImage._debugBbox, self.selectedImage.bbox.min.x, self.selectedImage.bbox.min.y)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        self._action = Action.NONE

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.__canvas.canvasViewModel.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self._canvasSelectedRectangle = self.__canvas.create_rectangle(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y, outline="black", width=2, dash=(2, 2))
                self.selectedImage = image

                # Check the action to move since the cursor is inside the image
                self._action = Action.MOVE
                self.__canvas.config(cursor="fleur")
                return


