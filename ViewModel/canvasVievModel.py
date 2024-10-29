import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum

from Model.canvasImage import CanvasImage

from ViewModel.selectionTool import SelectionTool
from ViewModel.selectionToolRectangle import SelectionToolRectangle

class Tools(Enum):
    SELECTION_TOOL = 0
    SELECTION_TOOL_RECTANGLE = 1

class CanvasViewModel:
    """
    A class to manage the CanvasImage in a canvas.

    Attributes:
    -----------
    __canvas : tk.Canvas
        The canvas where the manager is tied to
    images : dict
        A dictonary to keep all the CanvasImage. The key are the Id of the canvas drawing, and the value is the CanvasImage itself.
    """

    def __init__(self, canvas):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters:
        -----------
        canvas : tk.Canvas
            The canvas where the manager is going to be tied to
        """
        self.__canvas = canvas
        self.images = {}

        self.selectionTool = SelectionTool(canvas)
        self.selectionToolRectangle = SelectionToolRectangle(canvas)
        self.activeTool = Tools.SELECTION_TOOL_RECTANGLE

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

    def getActiveTool(self):
        toolMap = {
            Tools.SELECTION_TOOL: self.selectionTool,
            Tools.SELECTION_TOOL_RECTANGLE: self.selectionToolRectangle,
        }

        tool = toolMap.get(self.activeTool)
        return tool