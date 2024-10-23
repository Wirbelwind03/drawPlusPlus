import tkinter as tk
from PIL import Image, ImageTk

from Model.canvasImage import CanvasImage
from Controller.selectionTool import SelectionTool

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)
        self.imgs = []
        self.currentImageId = 0
        self.selectionTool = SelectionTool(self)

    def drawImage(self, filePath):
        #image = self.cropImage(image)
        canvasImage = CanvasImage(self.currentImageId, 0, 0)
        canvasImage.loadImage(filePath)
        self.imgs.append(canvasImage)
        
        self.create_image(canvasImage.coordinates.x, canvasImage.coordinates.y, anchor=tk.NW, image=canvasImage.photoImage)
        self.currentImageId += 1

        canvasImage.cropImage()
        self.create_image(canvasImage.coordinates.x, canvasImage.coordinates.y, anchor=tk.NW, image=canvasImage.photoImage)

    def cropImage(self, img):
        width, height = img.size

        # Define the crop rectangle to keep top left, top right, and bottom left
        crop_rectangle = (0, 0, width, height)  # Keep the entire image

        # Create a new blank image with transparency
        new_img = Image.new("RGBA", img.size)

        # Paste the original image onto the new image
        new_img.paste(img)

        # Create a mask to remove the bottom right corner
        mask = Image.new("L", img.size, 255)  # White mask (opaque)
        mask.paste(0, (width // 2, height // 2, width, height))  # Black (transparent) area

        # Apply the mask to create the final image
        new_img.putalpha(mask)

        return new_img
