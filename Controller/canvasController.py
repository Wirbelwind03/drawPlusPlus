import tkinter as tk
from PIL import Image, ImageTk

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.canvasEntities import CanvasEntities

from config import DEBUG

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.canvasEntities import CanvasEntities
from Model.toolManager import ToolManager

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

    def __init__(self, canvas: tk.Canvas, toolManager: ToolManager):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters
        -----------
        canvas : tk.Canvas
            The canvas where the ViewModel is going to be tied to
        """
        self.view: tk.Canvas = canvas
        self.model: CanvasEntities = CanvasEntities()
        self.toolManager = toolManager

        # Bind mouse events to the canvas
        self.view.bind("<ButtonPress-1>", self.on_button_press)
        self.view.bind("<B1-Motion>", self.on_mouse_drag)
        self.view.bind("<ButtonRelease-1>", self.on_button_release)
        self.view.bind("<Motion>", self.on_mouse_over)
        
        # Bind key events to the canvas
        self.view.bind("<Delete>", self.on_delete)
        self.view.bind("<Control-Key-c>", self.on_control_c)
        self.view.bind("<Control-Key-v>", self.on_control_v)

    #region Public Methods

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
        self.model.addEntity(imageId, newCanvasImage)

        return newCanvasImage

    def rotateImage(self, canvasImage: CanvasImage, degrees: int):
        canvasImage.rotatePhotoImage(degrees)

        self.view.itemconfig(canvasImage.id, image=canvasImage.photoImage)

    def deleteImage(self, canvasImage: CanvasImage):
        if canvasImage == None:
            return
        self.view.delete(canvasImage.id)
        self.model.deleteEntity(canvasImage.id)

    def update(self):
        """
        Update every image that is present in the canvas
        """
        # Loop every image and its ID that is present in the dictionary
        for imageId, canvasImage in self.model.images.items():
            # Update the image
            self.view.itemconfig(imageId, image=canvasImage.photoImage)

    def deleteAll(self):
        # Remove every drawn entities on the canvas (aka both images and shapes)
        self.view.delete("all")
        self.model.deleteAll()

    #endregion Public Methods

    #region Private Methods

    def __invoke_active_tool_method(self, method_name, event):
        self.toolManager.invoke_tool_method(method_name, event)
        
    #endregion Private Methods

    #region Event

    def on_mouse_over(self, event):
        self.__invoke_active_tool_method("on_mouse_over", event)

    def on_button_press(self, event):
        self.view.focus_set()
        
        self.__invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event):
        self.__invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event):
        self.__invoke_active_tool_method("on_button_release", event)

    def on_delete(self, event):
        self.__invoke_active_tool_method("on_delete", event)
        self.update()

    def on_control_c(self, event):
        self.__invoke_active_tool_method("on_control_c", event)

    def on_control_v(self, event):
        self.__invoke_active_tool_method("on_control_v", event)

    #endregion Event