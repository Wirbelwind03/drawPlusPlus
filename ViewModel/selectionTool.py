from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

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
                self.__canvas.config(cursor="arrow")

    def on_button_press(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if not self.selectedImage:
            for imageId, image in self.__canvas.canvasViewModel.images.items():
                if image.bbox.isInside(mouseCoords):
                    self._canvasSelectedRectangle = self.__canvas.create_rectangle(image.bbox.startCoordinates.x, image.bbox.startCoordinates.y, image.bbox.endCoordinates.x, image.bbox.endCoordinates.y, outline="black", width=2, dash=(2, 2))
                    self.selectedImage = image
                    self._action = Action.MOVE
                    self.__canvas.config(cursor="fleur")
                    self._startGapOffset = image.bbox.startCoordinates - mouseCoords
                    self._endGapOffset = image.bbox.endCoordinates - mouseCoords
                    return
        else:
            pass

    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            self.selectedImage.bbox.startCoordinates = mouseCoords + self._startGapOffset
            self.selectedImage.bbox.endCoordinates = mouseCoords + self._endGapOffset
            self.__canvas.moveto(self._canvasSelectedRectangle, self.selectedImage.bbox.startCoordinates.x, self.selectedImage.bbox.startCoordinates.y)
            self.__canvas.moveto(self.selectedImage.id, self.selectedImage.bbox.startCoordinates.x, self.selectedImage.bbox.startCoordinates.y)
            return
        
    def on_button_release(self, event):
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            self.__canvas.delete(self._canvasSelectedRectangle)
            self.selectedImage = None
        
        self._action = Action.NONE

