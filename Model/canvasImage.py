from PIL import Image, ImageTk
import os

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

class CanvasImage:
    def __init__(self) -> None:
        self.id = -1
        self.filePath = ""
        self._width = 0
        self._height = 0
        self.image: Image = None
        self.photoImage: ImageTk.PhotoImage = None
        self.bbox = None

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = width
        if self.bbox:
            self.bbox.width = self.width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height
        if self.bbox:
            self.bbox.height = self.height

    def clone(self) -> 'CanvasImage':
        canvasImage = CanvasImage()
        canvasImage.id = -1
        canvasImage.image = self.image.copy()
        canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
        canvasImage.width = self.width
        canvasImage.height = self.height
        canvasImage.filePath = self.filePath
        canvasImage.bbox = self.bbox

        return canvasImage

    def load(self, filePath: str) -> None:
        try:
            # Check if the file exists
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"The file '{filePath}' does not exist.")

            self.image = Image.open(filePath)
            self.photoImage = ImageTk.PhotoImage(self.image)
            self.width, self.height = self.image.size
        except FileNotFoundError as e:
            print(e)

    def cut(self, x, y, width, height) -> None:
        new_img = self.image.convert("RGBA")
        mask = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        new_img.paste(mask, (x, y))

        # Update the image
        self.image = new_img
        self.photoImage = ImageTk.PhotoImage(new_img)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        resizedImage = self.image.resize((self.width, self.height))
        
        # Update the image
        self.image = resizedImage
        self.photoImage = ImageTk.PhotoImage(resizedImage)

