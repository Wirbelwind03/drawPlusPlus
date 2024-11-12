import tkinter as tk
import copy
from PIL import Image, ImageTk
from enum import Enum

from Model.canvasImage import CanvasImage

from DrawLibrary.Core.Collision.aabb import AABB

from config import DEBUG

class CanvasViewModel:
    """
    A class to manage the CanvasImage in a canvas.

    Attributes:
    -----------
    canvas : tk.Canvas
        The canvas where the ViewModel is tied to
    images : dict
        A dictonary to keep all the CanvasImage. The key are the Id of the canvas drawing, and the value is the CanvasImage itself.
    """

    def __init__(self, canvas: tk.Canvas):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters:
        -----------
        canvas : tk.Canvas
            The canvas where the ViewModel is going to be tied to
        """
        self.canvas: tk.Canvas = canvas
        self.images = {}

    def drawImage(self, canvasImage: CanvasImage, x, y, width=None, height=None):
        """
        Draw a image to the canvas

        Parameters:
        -----------
        canvasImage : CanvasImage
            The image we want to draw to the Canvas
        x : int
            The x position where the image is going to be draw
        y : int
            The y position where the image is giong to be draw
        width : int
            The width the image is going to be resized to
        height : int
            The height the image is going to be resized to
        """
        width = width or canvasImage.width
        height = height or canvasImage.height

        # Draw the image to the canvas
        newCanvasImage = canvasImage.clone()
        newCanvasImage.resize(width, height)
        imageId = self.canvas.create_image(x, y, anchor=tk.NW, image=newCanvasImage.photoImage) 
        newCanvasImage.id = imageId
        newCanvasImage.bbox = AABB(x, y, width, height)

        if DEBUG:
            newCanvasImage.debugBbox = self.canvas.create_rectangle(newCanvasImage.bbox.min.x, newCanvasImage.bbox.min.y, newCanvasImage.bbox.max.x, newCanvasImage.bbox.max.y, outline="black", width=2)

        # Put the image to dictionary with the id as the key
        self.images[imageId] = newCanvasImage

        return newCanvasImage 

    def update(self):
        """
        Update every image that is present in the canvas
        """
        # Loop every image and its ID that is present in the dictionary
        for imageId, canvasImage in self.images.items():
            # Update the image
            self.canvas.itemconfig(imageId, image=canvasImage.photoImage)