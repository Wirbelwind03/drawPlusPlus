import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum

from DrawLibrary.Graphics.canvasImage import CanvasImage

from DrawLibrary.Core.Collision.aabb import AABB

from Model.toolManager import ToolManager
from Model.canvasImages import CanvasImages

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

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
        self.view: tk.Canvas = canvas
        self.model: CanvasImages = CanvasImages()
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.view, self.model)

        self.toolManager = ToolManager()
        self.toolManager.addTool("SELECTION_TOOL", SelectionTool(self.view, self.model, self.SRCC))
        self.toolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.view, self.model, self.SRCC))
        self.toolManager.setActiveTool("SELECTION_TOOL")

        # Mouse events
        self.view.bind("<ButtonPress-1>", self.on_button_press)
        self.view.bind("<B1-Motion>", self.on_mouse_drag)
        self.view.bind("<ButtonRelease-1>", self.on_button_release)
        self.view.bind("<Motion>", self.on_mouse_over)
        
        # Key events
        self.view.bind("<Delete>", self.on_delete)
        self.view.bind("<Control-Key-c>", self.on_control_c)
        self.view.bind("<Control-Key-v>", self.on_control_v)

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
        newCanvasImage.createAABB(x, y, width, height)

        imageId = self.view.create_image(x, y, anchor=tk.NW, image=newCanvasImage.photoImage) 
        newCanvasImage.id = imageId

        if DEBUG:
            newCanvasImage.debugBbox = self.view.create_rectangle(newCanvasImage.bbox.min.x, newCanvasImage.bbox.min.y, newCanvasImage.bbox.max.x, newCanvasImage.bbox.max.y, outline="black", width=2)

        # Put the image to dictionary with the id as the key
        self.model.addImage(imageId, newCanvasImage)

    def deleteImage(self, canvasImage: CanvasImage):
        self.view.delete(canvasImage.id)
        self.model.deleteImage(canvasImage.id)

    def update(self):
        """
        Update every image that is present in the canvas
        """
        # Loop every image and its ID that is present in the dictionary
        for imageId, canvasImage in self.model.images.items():
            # Update the image
            self.view.itemconfig(imageId, image=canvasImage.photoImage)

    def _invoke_active_tool_method(self, method_name, event):
        self.toolManager.invoke_tool_method(method_name, event)
        self.update()

    ## Events ##

    def on_mouse_over(self, event):
        self._invoke_active_tool_method("on_mouse_over", event)

    def on_button_press(self, event):
        self.view.focus_set()
        
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