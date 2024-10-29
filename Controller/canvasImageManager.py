import tkinter as tk
from PIL import Image, ImageTk

from Model.canvasImage import CanvasImage

class CanvasImagesManager:
    """
    A class to manage the CanvasImage in a canvas.

    Attributes:
    -----------
    __canvas : tk.Canvas
        The canvas where the manager is tied to
    images : dict
        A dictonary to keep all the CanvasImage. The key are the Id of the canvas drawing, and the value is the CanvasImage itself.
    """

    def __init__(self, canvas: tk.Canvas):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters:
        -----------
        canvas : tk.Canvas
            The canvas where the manager is going to be tied to
        """
        self.__canvas = canvas
        self.images = {}

    def drawImage(self, canvasImage: CanvasImage):
        """
        Draw a image to the canvas

        Parameters:
        -----------
        canvasImage : CanvasImage
            The image we want to draw to the Canvas
        """
        # Draw the image to the canvas
        imageId = self.__canvas.create_image(canvasImage.coordinates.x, canvasImage.coordinates.y, anchor=tk.NW, image=canvasImage.photoImage) 
        canvasImage.id = imageId
        # Put the image to dictionary with the id as the key
        self.images[imageId] = canvasImage 

    def update(self):
        """
        Update every image that is present in the canvas
        """
        # Loop every image and its ID that is present in the dictionary
        for imageId, canvasImage in self.images.items():
            # Update the image
            self.__canvas.itemconfig(imageId, image=canvasImage.photoImage)