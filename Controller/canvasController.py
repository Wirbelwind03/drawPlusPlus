import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from Controller.debugCanvasController import DebugCanvasController

from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.Core.Math.vector2 import Vector2

from Model.canvasEntities import CanvasEntities
from Model.toolManager import ToolManager

class CanvasController:
    """
    The canvas controller is used to communication infos given to the canvas, and opposite.


    Attributes
    -----------
    canvas : tk.Canvas
        The canvas where the ViewModel is tied to
    images : dict[int, CanvasImage]
        A dictonary to keep all the CanvasImage. 
        The key are the ID given through the draw functions of tk.Canvas, and the value is the CanvasImage itself.
    """

    def __init__(self, canvas: tk.Canvas, toolManager: ToolManager, DCC: DebugCanvasController = None):
        """
        Constructs a new CanvasImagesManager to the canvas.

        Parameters
        -----------
        view : tk.Canvas
            The canvas where the ViewModel is going to be tied to
        toolManager : ToolManager
            The tools tied to this controller, for example, the selection tool, the selection rectangle creation tool, etc.
        DCC : DebugCanvasController
            A controller used to communicate with the debug informations
        """
        self.view: tk.Canvas = canvas
        self.model: CanvasEntities = CanvasEntities()
        self.toolManager = toolManager
        self.DCC = DCC

        # Bind mouse events to the canvas
        self.view.bind("<ButtonPress-1>", self.on_button_press)
        self.view.bind("<B1-Motion>", self.on_mouse_drag)
        self.view.bind("<ButtonRelease-1>", self.on_button_release)
        self.view.bind("<Motion>", self.on_mouse_over)
        
        # Bind key events to the canvas
        self.view.bind("<Delete>", self.on_delete)
        self.view.bind("<Control-Key-c>", self.on_control_c)
        self.view.bind("<Control-Key-v>", self.on_control_v)
        self.view.bind("<Left>", self.on_left)
        self.view.bind("<Left>", self.on_left)

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
        # If the width and height arguments hasn't been put
        # Put the width and height of the canvas image loaded
        width = width or canvasImage.width
        height = height or canvasImage.height

        # Clone the canvas image, so a new reference can be create
        newCanvasImage = canvasImage.clone()

        # Resize the image
        resizedImage = newCanvasImage.image.resize((width, height))
        # Attach the new resized image to the attribute
        newCanvasImage.image = resizedImage
        newCanvasImage.photoImage = ImageTk.PhotoImage(resizedImage)

        newCanvasImage.width = width
        newCanvasImage.height = height
        
        # Create the abb of the image
        newCanvasImage.createAABB(x, y, width, height)

        # Set the CanvasImage position in the center
        newCanvasImageCenter = Vector2(x + width // 2, y + height // 2)
        # Draw the image on the tkinter canvas
        imageId = self.view.create_image(newCanvasImageCenter.x, newCanvasImageCenter.y, image=newCanvasImage.photoImage) 
        # Assign the id to the CanvasImage
        newCanvasImage.id = imageId

        # Draw debug informations of the canvas Image
        if DEBUG and self.DCC != None:
            self.DCC.addCanvasID(newCanvasImage)
            self.DCC.drawCanvasImageDebugInfos(newCanvasImage)

        # Put the image to dictionary with the id as the key
        self.model.addEntity(imageId, newCanvasImage)

        return newCanvasImage
    
    def rotateImage(self, canvasImage: CanvasImage, degrees: int = 0):
        canvasImage.rotatePhotoImage(degrees)

        # Update the photoImage on the tkinter Canvas
        self.view.itemconfig(canvasImage.id, image=canvasImage.photoImage)

    def resizeImage(self, canvasImage: CanvasImage, width: int, height: int):
        canvasImage.resizePhotoImage(width, height)

        # Update the photoImage on the tkinter Canvas
        self.view.itemconfig(canvasImage.id, image=canvasImage.photoImage)
    
    def deleteImage(self, canvasImage: CanvasImage) -> None:
        if canvasImage == None:
            return
        self.view.delete(canvasImage.id)
        self.model.deleteEntity(canvasImage.id)

    def update(self) -> None:
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

    def __invoke_active_tool_method(self, method_name: str, event) -> None:
        """
        Call the function from the tool

        Parameters
        -----------
        method_name : str
            The function name to be called in the tool
        event :
        """
        self.toolManager.invoke_tool_method(method_name, event)
        
    #endregion Private Methods

    #region Event

    def on_mouse_over(self, event) -> None:
        """
        Event when the mouse is over the canvas

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_mouse_over", event)

    def on_button_press(self, event) -> None:
        """
        Event when the left click of the mouse is pressed

        Parameters
        -----------
        event :
        """
        self.view.focus_set()
        
        self.__invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event) -> None:
        """
        Event when the mouse is dragged over the canvas

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event) -> None:
        """
        Event when the left click of the mouse is released

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_button_release", event)

    def on_delete(self, event) -> None:
        """
        Event when the "Del" button on the keyboard is pressed

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_delete", event)
        self.update()

    def on_control_c(self, event) -> None:
        """
        Event when the "Ctrl+C" short cut on the keyboard is pressed

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_control_c", event)

    def on_control_v(self, event) -> None:
        """
        Event when the "Ctrl+V" short cut on the keyboard is pressed

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_control_v", event)

    def on_left(self, event) -> None:
        """
        Event when the left arrow button on the keyboard is pressed

        Parameters
        -----------
        event :
        """
        self.__invoke_active_tool_method("on_left", event)

    #endregion Event