from PIL import Image, ImageTk

from Core.Math.vector2 import Vector2
from Core.Shapes.rectangle import Rectangle

class CanvasImage:
    def __init__(self, id, x, y):
        self.id = id
        self.coordinates = Vector2(x, y)
        self._width = 0
        self._height = 0
        self.image = None
        self.photoImage = None
        self.bbox = Rectangle(x, y)

    def loadImage(self, filePath):
        self.image = Image.open(filePath)
        self.width, self.height = self.image.size
        self.photoImage = ImageTk.PhotoImage(self.image)

    def cropImage(self):
        # Create a new blank image with transparency
        new_img = Image.new("RGBA", self.image.size)

        # Paste the original image onto the new image
        new_img.paste(self.image)

        # Create a mask to remove the bottom right corner
        mask = Image.new("L", self.image.size, 255)  # White mask (opaque)
        mask.paste(0, (self.width // 2, self.height // 2, self.width, self.height))  # Black (transparent) area

        # Apply the mask to create the final image
        new_img.putalpha(mask)

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
