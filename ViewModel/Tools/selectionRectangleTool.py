from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from Model.canvasImage import CanvasImage
from Model.selectionRectangle import SelectionRectangle

from ViewModel.canvasVievModel import CanvasViewModel

from config import DEBUG

class Action(Enum):
    CREATE = 0
    MOVE = 1
    RESIZE = 2
    ROTATE = 3

class SelectionRectangleTool:
    """
    A class for the selection tool used in the canvas.

    Attributes:
    -----------
    _canvas : tk.Canvas
        The canvas widget where the selection tool is used
    bbox : Rectangle
        A rectangle called Bounding Box that define the minimum and maximum coordinates
    _canvasSelectionRectangle : int
        The ID of the rectangle drawn on the Canvas
    _action : Action
        What the user want to do with the selection tool, like deleting, moving, etc.
    """

    def __init__(self, canvasViewModel):
        self.canvasViewModel: CanvasViewModel = canvasViewModel
        
        self.__debugBbox = -1
        self.__action = Action.CREATE

        self.selectionRectangle: SelectionRectangle = None

        self.__tempStartCoordinates = None
        self.__tempCanvasSelectionRectangle = -1
        self.__copiedImage : CanvasImage = None
        
    def createDebugBbox(self):
        if self.__debugBbox:
            self.canvasViewModel.canvas.delete(self.__debugBbox)

        self.__debugBbox = self.canvasViewModel.canvas.create_rectangle(self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.max.x, self.selectionRectangle.max.y, outline="black", width=2)

    def on_mouse_over(self, event):
        """
        A event for when the mouse is hovering on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.selectionRectangle:
            # Check if the cursor is inside the selection rectangle
            if self.selectionRectangle.isInside(mouseCoords):
                # If it is, change that the action we want to do is moving the selection rectangle
                self.__action = Action.MOVE
                self.canvasViewModel.canvas.config(cursor="fleur")
            else:
                # If it's not, change that the action we want to do is creating a selection rectangle
                self.__action = Action.CREATE
                self.canvasViewModel.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        """
        A event for when the user left click on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.__action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self.selectionRectangle.on_button_press(event)
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.__tempCanvasSelectionRectangle:
            self.canvasViewModel.canvas.delete(self.__tempCanvasSelectionRectangle)

        # Save the starting point for the rectangle
        self.__tempStartCoordinates = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self.__tempCanvasSelectionRectangle = self.canvasViewModel.canvas.create_rectangle(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        """
        A event for when the mouse is dragged over on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.__action == Action.MOVE:
            # Update the coordinates and move the selection rectangle
            self.selectionRectangle.on_mouse_drag(event)
            self.canvasViewModel.canvas.moveto(self.__tempCanvasSelectionRectangle, self.selectionRectangle.min.x, self.selectionRectangle.min.y)
            return

        # Update the rectangle as the mouse is dragged
        self.canvasViewModel.canvas.coords(self.__tempCanvasSelectionRectangle, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.__action == Action.MOVE:
            if DEBUG:
                self.createDebugBbox()
            return

        # On release, finalize the rectangle selection by setting its end coordinates
        self.selectionRectangle = SelectionRectangle.fromCoordinates(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

        if DEBUG:
            self.createDebugBbox()

    def on_delete(self, event):
        if self.selectionRectangle:
            for imageId, image in self.canvasViewModel.images.items():
                # check overlap with image and selection tool
                if self.selectionRectangle.isIntersecting(image.bbox):
                    x1 = max(self.selectionRectangle.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(self.selectionRectangle.topRight.y, image.bbox.topRight.y)
                    x2 = min(self.selectionRectangle.topRight.x, image.bbox.topRight.x)
                    y2 = min(self.selectionRectangle.bottomRight.y, image.bbox.bottomRight.y)
                    #intersectRectangle = selectionToolRectangleBbox.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    image.cut(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    
                    if DEBUG:
                        self.canvasViewModel.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
                        #self._canvas.create_rectangle(intersectRectangle.topLeft.x, intersectRectangle.topLeft.y, intersectRectangle.bottomRight.x, intersectRectangle.bottomRight.y, outline="red", width=2)
                
            self.canvasViewModel.update()
            self.canvasViewModel.canvas.delete(self.__debugBbox)

    def on_control_c(self, event):
        if self.selectionRectangle:
            blankCanvasImage = CanvasImage.createBlank(self.selectionRectangle.width, self.selectionRectangle.height)
            isBlank = True
            for imageId, image in self.canvasViewModel.images.items():
                # check overlap with image and selection tool
                if self.selectionRectangle.isIntersecting(image.bbox):
                    x1 = max(self.selectionRectangle.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(self.selectionRectangle.topRight.y, image.bbox.topRight.y)
                    x2 = min(self.selectionRectangle.topRight.x, image.bbox.topRight.x)
                    y2 = min(self.selectionRectangle.bottomRight.y, image.bbox.bottomRight.y)
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    region = image.copy(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    blankCanvasImage.paste(x1 - self.selectionRectangle.topLeft.x, y1 - self.selectionRectangle.topLeft.y, region)
                    isBlank = False

                    if DEBUG:
                        self.canvasViewModel.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

            if not isBlank:
                self.__copiedImage = blankCanvasImage

    def on_control_v(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        if self.__copiedImage:
            self.canvasViewModel.drawImage(self.__copiedImage, 0, 0)