import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum

from Model.canvasImage import CanvasImage

from DrawLibrary.Core.Collision.aabb import AABB

from Model.toolManager import ToolManager

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool

from config import DEBUG

class CanvasController:
    """
    A class to manage the CanvasImage in a canvas.

    Attributes
    -----------
    canvas : tk.Canvas
        The canvas where the ViewModel is tied to
    images : dict[int, CanvasImage]
        A dictonary to keep all the CanvasImage. 
        The key are the ID given through the draw functions of tk.Canvas, and the value is the CanvasImage itself.
    """

    def __init__(self, canvas: tk.Canvas):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the ViewModel is going to be tied to
        """
        self.canvas: tk.Canvas = canvas
        self.images: dict[int, CanvasImage] = {}

        self.toolManager = ToolManager()
        self.toolManager.addTool("SELECTION_TOOL", SelectionTool(self.CC))
        self.toolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.CC))
        self.toolManager.setActiveTool("SELECTION_TOOL")

        # Mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_mouse_over)
        
        # Key events
        self.canvas.bind("<Delete>", self.on_delete)
        self.canvas.bind("<Control-Key-c>", self.on_control_c)
        self.canvas.bind("<Control-Key-v>", self.on_control_v)

    def drawImage(self, canvasImage: CanvasImage, x, y, width=None, height=None):
        """
        Draw a image to the canvas

        Parameters
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

    def deleteImage(self, canvasImage: CanvasImage):
        self.canvas.delete(canvasImage.id)
        del self.images[canvasImage.id]

    def update(self):
        """
        Update every image that is present in the canvas
        """
        # Loop every image and its ID that is present in the dictionary
        for imageId, canvasImage in self.images.items():
            # Update the image
            self.canvas.itemconfig(imageId, image=canvasImage.photoImage)

    def _invoke_active_tool_method(self, method_name, event):
        self.toolManager.invoke_tool_method(method_name, event)

    def on_mouse_over(self, event):
        self._invoke_active_tool_method("on_mouse_over", event)

    def on_button_press(self, event):
        self.canvas.focus_set()
        
        self._invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event):
        self._invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event):
        self._invoke_active_tool_method("on_button_release", event)

    def on_delete(self, event):
        self._invoke_active_tool_method("on_delete", event)

    def on_control_c(self, event):
        self._invoke_active_tool_method("on_control_c", event)

    def on_control_v(self, event):
        self._invoke_active_tool_method("on_control_v", event)