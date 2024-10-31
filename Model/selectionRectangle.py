from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Core.Math.vector2 import Vector2

from Model.canvasImage import CanvasImage

class SelectionRectangle(AABB):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.startGapOffset = 0
        self.endGapOffset = 0

        self.canvasRectangle = -1
        self.attachedImage: CanvasImage = None

    @classmethod
    def fromCoordinates(cls, x1, y1, x2, y2) -> 'SelectionRectangle':
        instance =  super().fromCoordinates(x1, y1, x2, y2)

        return instance

    def on_button_press(self, event):
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        self.startGapOffset = self.min - mouseCoords
        self.endGapOffset = self.max - mouseCoords

    def on_mouse_drag(self, event):
        mouseCoords = Vector2(event.x, event.y)

        self.min = mouseCoords + self.startGapOffset
        self.max = mouseCoords + self.endGapOffset
        if self.attachedImage:
            self.attachedImage.bbox.min = self.min
            self.attachedImage.bbox.max = self.max
    