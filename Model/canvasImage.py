from PIL import Image, ImageTk

from Core.Math.vector2 import Vector2

class CanvasImage:
    def __init__(self, id, x, y):
        self.id = id
        self.coordinates = Vector2(x, y)
        self.width = 0
        self.height = 0
        self.image = None
        self.photoImage = None

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