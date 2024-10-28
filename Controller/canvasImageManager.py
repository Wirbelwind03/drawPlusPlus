import tkinter as tk
from PIL import Image, ImageTk

from Model.canvasImage import CanvasImage

class CanvasImagesManager:
    def __init__(self, canvas: tk.Canvas):
        self.__canvas = canvas
        self.images = {}

    def drawImage(self, canvasImage: CanvasImage):
        imageId = self.__canvas.create_image(canvasImage.coordinates.x, canvasImage.coordinates.y, anchor=tk.NW, image=canvasImage.photoImage)
        canvasImage.id = imageId
        self.images[imageId] = canvasImage

    def update(self):
        for imageId, canvasImage in self.images.items():
            self.__canvas.itemconfig(imageId, image=canvasImage.photoImage)