from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from config import DEBUG

from ViewModel.canvasVievModel import CanvasViewModel

from Model.canvasImage import CanvasImage

class Action(Enum):
    NONE = 0
    MOVE = 1

class SelectionTool:
    def __init__(self, canvasViewModel):
        self.canvasViewModel: CanvasViewModel = canvasViewModel
        self.__action = Action.NONE

        self.__selectedImage: CanvasImage = None
        self.__canvasSelectedRectangle: int = -1

    def on_mouse_over(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.__selectedImage:
            if self.__selectedImage.bbox.isInside(mouseCoords):
                self.__action = Action.MOVE
                self.canvasViewModel.canvas.config(cursor="fleur")
            else:
                self.__action = Action.NONE
                self.canvasViewModel.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.__selectedImage:
            self.getClickedImage(mouseCoords)
        
        # If the cursor is outside the selected image, deselect it
        if self.__selectedImage and self.__selectedImage.bbox.isOutside(mouseCoords):
            self.canvasViewModel.canvas.delete(self.__canvasSelectedRectangle)
            self.__selectedImage = None
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)

        if self.__action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self._startGapOffset = self.__selectedImage.bbox.min - mouseCoords
            self._endGapOffset = self.__selectedImage.bbox.max - mouseCoords
            return

                
    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self.__action == Action.MOVE:
            self.__selectedImage.bbox.min = mouseCoords + self._startGapOffset
            self.__selectedImage.bbox.max = mouseCoords + self._endGapOffset
            self.canvasViewModel.canvas.moveto(self.__canvasSelectedRectangle, self.__selectedImage.bbox.min.x, self.__selectedImage.bbox.min.y)
            self.canvasViewModel.canvas.moveto(self.__selectedImage.id, self.__selectedImage.bbox.min.x, self.__selectedImage.bbox.min.y)
            if DEBUG:
                self.canvasViewModel.canvas.moveto(self.__selectedImage._debugBbox, self.__selectedImage.bbox.min.x, self.__selectedImage.bbox.min.y)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        self.__action = Action.NONE

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.canvasViewModel.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.__canvasSelectedRectangle = self.canvasViewModel.canvas.create_rectangle(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y, outline="black", width=2, dash=(2, 2))
                self.__selectedImage = image

                # Check the action to move since the cursor is inside the image
                self.__action = Action.MOVE
                self.canvasViewModel.canvas.config(cursor="fleur")
                return


