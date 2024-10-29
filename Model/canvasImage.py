from PIL import Image, ImageTk
import os

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

class CanvasImage:
    def __init__(self, x=0, y=0) -> None:
        self.id = -1
        self.filePath = ""
        self.coordinates = Vector2(x, y)
        self.image = None
        self.photoImage = None
        self.bbox = None

    def load(self, filePath: str) -> None:
        try:
            # Check if the file exists
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"The file '{filePath}' does not exist.")

            self.image = Image.open(filePath)
            self.photoImage = ImageTk.PhotoImage(self.image)
            width, height = self.image.size
            self.bbox = AABB(self.coordinates.x, self.coordinates.y, width, height)
        except FileNotFoundError as e:
            print(e)

    def cut(self, x1, y1, width, height) -> None:
        new_img = self.image.convert("RGBA")
        mask = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        new_img.paste(mask, (x1, y1))

        self.image = new_img
        self.photoImage = ImageTk.PhotoImage(new_img)