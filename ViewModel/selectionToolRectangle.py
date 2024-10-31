from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from Model.canvasImage import CanvasImage

from config import DEBUG

class Action(Enum):
    CREATE = 0
    MOVE = 1
    RESIZE = 2
    ROTATE = 3

class SelectionToolRectangle:
    """
    A class for the selection tool used in the canvas.

    Attributes:
    -----------
    __canvas : tk.Canvas
        The canvas widget where the selection tool is used
    bbox : Rectangle
        A rectangle called Bounding Box that define the minimum and maximum coordinates
    _canvasSelectionRectangle : int
        The ID of the rectangle drawn on the Canvas
    _action : Action
        What the user want to do with the selection tool, like deleting, moving, etc.
    """

    def __init__(self, canvas):
        self.bbox: AABB = None

        self.__canvas = canvas
        
        self._canvasSelectionRectangle = -1
        self._debugBbox = -1
        self._action = Action.CREATE

        self._startGapOffset = 0
        self._endGapOffset = 0

        self._tempStartCoordinates = None
        
    def createDebugBbox(self):
        if self._debugBbox:
            self.__canvas.delete(self._debugBbox)

        self._debugBbox = self.__canvas.create_rectangle(self.bbox.min.x, self.bbox.min.y, self.bbox.max.x, self.bbox.max.y, outline="black", width=2)

    def on_mouse_over(self, event):
        """
        A event for when the mouse is hovering on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.bbox:
            # Check if the cursor is inside the selection rectangle
            if self.bbox.isInside(mouseCoords):
                # If it is, change that the action we want to do is moving the selection rectangle
                self._action = Action.MOVE
                self.__canvas.config(cursor="fleur")
            else:
                # If it's not, change that the action we want to do is creating a selection rectangle
                self._action = Action.CREATE
                self.__canvas.config(cursor="arrow")

    def on_button_press(self, event):
        """
        A event for when the user left click on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            # Calculate the offset between mouse click and rectangle's position
            self._startGapOffset = self.bbox.min - mouseCoords
            self._endGapOffset = self.bbox.max - mouseCoords
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self._canvasSelectionRectangle:
            self.__canvas.delete(self._canvasSelectionRectangle)

        # Save the starting point for the rectangle
        self._tempStartCoordinates = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self._canvasSelectionRectangle = self.__canvas.create_rectangle(self._tempStartCoordinates.x, self._tempStartCoordinates.y, self._tempStartCoordinates.x, self._tempStartCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        """
        A event for when the mouse is dragged over on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            # Update the coordinates and move the selection rectangle
            self.bbox.min = mouseCoords + self._startGapOffset
            self.bbox.max = mouseCoords + self._endGapOffset
            self.__canvas.moveto(self._canvasSelectionRectangle, self.bbox.min.x, self.bbox.min.y)
            return

        # Update the rectangle as the mouse is dragged
        self.__canvas.coords(self._canvasSelectionRectangle, self._tempStartCoordinates.x, self._tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Attributes:
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self._action == Action.MOVE:
            if DEBUG:
                self.createDebugBbox()
            return

        # On release, finalize the rectangle selection by setting its end coordinates
        self.bbox = AABB.fromCoordinates(self._tempStartCoordinates.x, self._tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

        if DEBUG:
            self.createDebugBbox()

    def on_delete(self, event):
        if self.bbox:
            selectionToolRectangleBbox = self.bbox
            for imageId, image in self.__canvas.canvasViewModel.images.items():
                # check overlap with image and selection tool
                if selectionToolRectangleBbox.isIntersecting(image.bbox):
                    x1 = max(selectionToolRectangleBbox.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(selectionToolRectangleBbox.topRight.y, image.bbox.topRight.y)
                    x2 = min(selectionToolRectangleBbox.topRight.x, image.bbox.topRight.x)
                    y2 = min(selectionToolRectangleBbox.bottomRight.y, image.bbox.bottomRight.y)
                    #intersectRectangle = selectionToolRectangleBbox.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    image.cut(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    
                    if DEBUG:
                        self.__canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
                        #self.__canvas.create_rectangle(intersectRectangle.topLeft.x, intersectRectangle.topLeft.y, intersectRectangle.bottomRight.x, intersectRectangle.bottomRight.y, outline="red", width=2)
                
            self.__canvas.canvasViewModel.update()
            self.__canvas.delete(self._debugBbox)

    def on_control_c(self, event):
        if self.bbox:
            blankCanvasImage = CanvasImage.createBlank(self.bbox.width, self.bbox.height)
            for imageId, image in self.__canvas.canvasViewModel.images.items():
                # check overlap with image and selection tool
                if self.bbox.isIntersecting(image.bbox):
                    x1 = max(self.bbox.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(self.bbox.topRight.y, image.bbox.topRight.y)
                    x2 = min(self.bbox.topRight.x, image.bbox.topRight.x)
                    y2 = min(self.bbox.bottomRight.y, image.bbox.bottomRight.y)
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    region = image.copy(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    # self.bbox.topLeft.x - x1
                    blankCanvasImage.paste(x1 - self.bbox.topLeft.x, y1 - self.bbox.topLeft.y, region)

                    if DEBUG:
                        self.__canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

            self.__canvas.canvasViewModel.drawImage(blankCanvasImage, 0, 256, 256, 256)