from PIL import Image, ImageTk

from Core.Math.vector2 import Vector2
from Core.Collision.aabb import AABB

class CanvasImage:
    def __init__(self, x=0, y=0):
        self.id = -1
        self.filePath = ""
        self.coordinates = Vector2(x, y)
        self._width = 0
        self._height = 0
        self.image = None
        self.photoImage = None
        self.bbox = AABB(x, y)

    def loadImage(self, filePath):
        self.image = Image.open(filePath)
        self.width, self.height = self.image.size
        self.photoImage = ImageTk.PhotoImage(self.image)

    def cutImage(self, x1, y1, width, height):
        new_img = self.image.convert("RGBA")
        mask = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        new_img.paste(mask, (x1, y1))

        self.image = new_img
        self.photoImage = ImageTk.PhotoImage(new_img)

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = width
        self.bbox.width = self.width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height
        self.bbox.height = self.height
