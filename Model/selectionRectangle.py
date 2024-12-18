import tkinter as tk

from enum import Enum

from DrawLibrary.Core.Shapes.rectangle import RectangleCorners
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Core.Math.vector2 import Vector2

from DrawLibrary.Graphics.canvasImage import CanvasImage

class SelectionRectangleAction(Enum):
    NONE = 0
    MOVE = 1
    RESIZE = 2

class SelectionRectangle(AABB):

    #region Constructor

    """
    A class representing a selection rectangle (like the tool used in Paint)

    Attributes
    -----------
    canvasIdRectangle : int
        The ID of the rectangle rendered on a tk.Canvas, and is used to render the selection rectangle
    canvasIdCorners : list
        The IDs of the rectangles rendered on a tk.Canvas, and is used to render the corners of the selection rectangle
    attachedImage : CanvasImage
        The image attached to the selection rectangle
    action : SelectionRectangleAction
        The action the user is going to do with the selection rectangle
    """

    def __init__(self, *args, cornerSize: int=10, cornerCanvasSize: int=5, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.cornerSize: int = cornerSize
        self.cornerCanvasSize: int = cornerCanvasSize

        self.selectedCornerIndex: int = None
        
        self.canvasIdRectangle: int = -1
        self.canvasIdCorners: list[int] = []
        self.attachedImage: CanvasImage = None

        self.action: SelectionRectangleAction = SelectionRectangleAction.NONE

    @classmethod
    def fromCoordinates(cls, x1: int, y1: int, x2: int, y2: int, cornerSize: int=10, cornerCanvasSize: int=5) -> 'SelectionRectangle':
        """
        Create a SelectionRectangle from start and end coordinates
        The function also take the corner size as argument

        Parameters
        --------
        x1 : int
            The x start coordinate of the rectangle
        y1 : int
            The y start coordinate of the rectangle
        x2 : int
            The x end coordinate of the rectangle
        y2 : int
            The y end coordinate of the rectangle
        cornerSize : int
            The size of the corner, where the program is going to detect collision
        cornerCanvasSize : int
            The size of the corner rendered on the canvas

        Returns
        --------
        SelectionRectangle
            The new SelectionRectangle created from the arguments
        """
        instance: 'SelectionRectangle' =  super().fromCoordinates(x1, y1, x2, y2)
        instance.cornerSize = cornerSize
        instance.cornerCanvasSize = cornerCanvasSize
        return instance
    
    #endregion Constructor

    #region Property

    @property
    def min(self) -> Vector2:
        return super().min

    @min.setter
    def min(self, newValue: Vector2):
        super(SelectionRectangle, type(self)).min.fset(self, newValue)
        # Update the image coordinates
        if self.attachedImage:
            self.attachedImage.bbox.min = self.min

    @property
    def max(self) -> Vector2:
        return super().max

    @max.setter
    def max(self, newValue: Vector2):
        super(SelectionRectangle, type(self)).max.fset(self, newValue)
        # Update the image coordinates
        if self.attachedImage:
            self.attachedImage.bbox.max = self.max

    @property
    def topLeft(self) -> Vector2:
        return super().topLeft
    
    @topLeft.setter
    def topLeft(self, newValue):
        # The top left has lower x-coordinate than the top right
        # If the top left is more or equal than the x-coordinate of the top right
        # Then take the top right x-coordinate and subtract 1 so the top left stay lower
        # (left of the canvas = lower x-coordinate)
        if self.topLeft.x >= self.topRight.x:
            newValue = Vector2(self.topRight.x - 1, self.topRight.y)
        # The top left has lower y-coordinate than the bottom left
        # If the top left is more or equal than the y-coordinate of the bottom left
        # Then take the bottom left y-coordinate and subtract 1 so the top left stay lower
        # (top of the canvas = lower y-coordinate)
        elif self.topLeft.y >= self.bottomLeft.y:
            newValue = Vector2(self.bottomLeft.x, self.bottomLeft.y - 1)
        super(SelectionRectangle, type(self)).topLeft.fset(self, newValue)
        # Update the image coordinates
        if self.attachedImage:
            self.attachedImage.bbox.topLeft = newValue

    @property
    def topRight(self) -> Vector2:
        return super().topRight
    
    @topRight.setter
    def topRight(self, newValue):
        # The top right has higher x-coordinate than the top left
        # If the top right is less or equal than the x-coordinate of the top left
        # Then take the top left x-coordinate and add 1 so the top right stay higher
        # (right of the canvas = higher x-coordinate)
        if self.topRight.x <= self.topLeft.x:
            newValue = Vector2(self.topLeft.x + 1, self.topLeft.y)
        # The top right has lower y-coordinate than the bottom right
        # If the top right is more or equal than the y-coordinate of the bottom right
        # Then take the bottom right y-coordinate and subtract 1 so the top right stay lower
        # (top of the canvas = lower y-coordinate)
        elif self.topRight.y >= self.bottomRight.y:
            newValue = Vector2(self.bottomRight.x, self.bottomRight.y - 1)
        super(SelectionRectangle, type(self)).topRight.fset(self, newValue)
        # Update the image coordinates
        if self.attachedImage:
            self.attachedImage.bbox.topRight = newValue

    @property
    def bottomLeft(self) -> Vector2:
        return super().bottomLeft
    
    @bottomLeft.setter
    def bottomLeft(self, newValue):
        # The bottom left has lower x-coordinate than the bottom right
        # If the bottom left is more or equal than the x-coordinate of the bottom right
        # Then take the bottom right x-coordinate and subtract 1 so the bottom left stay lower
        # (left of the canvas = lower x-coordinate)
        if self.bottomLeft.x >= self.bottomRight.x:
            newValue = Vector2(self.bottomRight.x - 1, self.bottomRight.y)
        # The bottom left has higher y-coordinate than the top left
        # If the bottom left is less or equal than the y-coordinate of the top left
        # Then take the top left y-coordinate and add 1 so the bottom left stay higher
        # (bottom of the canvas = higher y-coordinate)
        elif self.bottomLeft.y <= self.topLeft.y:
            newValue = Vector2(self.topLeft.x, self.topLeft.y  + 1)
        super(SelectionRectangle, type(self)).bottomLeft.fset(self, newValue)
        # Update the image coordinates
        if self.attachedImage:
            self.attachedImage.bbox.bottomLeft = newValue

    @property
    def bottomRight(self) -> Vector2:
        return super().bottomRight
    
    @bottomRight.setter
    def bottomRight(self, newValue):
        # The bottom right has higher x-coordinate than the bottom left
        # If the bottom right is less or equal than the x-coordinate of the bottom left
        # Then take the bottom left x-coordinate and add 1 so the bottom right stay higher
        # (right of the canvas = higher x-coordinate)
        if self.bottomRight.x <= self.bottomLeft.x:
            newValue = Vector2(self.bottomLeft.x + 1, self.bottomLeft.y)
        # The bottom right has higher y-coordinate than the top right
        # If the bottom right is less or equal than the y-coordinate of the top right
        # Then take the top right y-coordinate and add 1 so the bottom right stay higher
        # (bottom of the canvas = higher y-coordinate)
        elif self.bottomRight.y <= self.topRight.y:
            newValue = Vector2(self.topRight.x, self.topRight.y + 1)
        super(SelectionRectangle, type(self)).bottomRight.fset(self, newValue)
        if self.attachedImage:
            self.attachedImage.bbox.bottomRight = newValue

    @property
    def cornersBbox(self):
        self._cornersBbox = []
        for i in range(len(self.corners)):
            self._cornersBbox.append(AABB.fromCoordinates(self.corners[i].x - 5, self.corners[i].y - 5, self.corners[i].x + 5, self.corners[i].y + 5))
        return self._cornersBbox

    #endregion

    def __repr__(self) -> str:
        return (
            f"SelectionRectangle(\n"
            f"    x={self.x}, y={self.y}, width={self.width}, height={self.height},\n"
            f"    left={self.left}, right={self.right},\n"
            f"    top={self.top}, bottom={self.bottom},\n"
            f"    topLeft={self.topLeft}, topRight={self.topRight},\n"
            f"    bottomLeft={self.bottomLeft}, bottomRight={self.bottomRight}\n"
            f"    min={self.min}, max={self.max}\n"
            f")"
        )


    #region Public Methods

    def setCoords(self, newMin: Vector2, newMax: Vector2) -> None:
        # Update the selection rectangle coordinates
        if newMin.x < 0:
            newMin.x = 0
        if newMin.y < 0:
            newMin.y = 0
        self.min = newMin
        self.max = newMax

    def isInsideCorners(self, coords: Vector2) -> bool:
        """
        Check if a coordinates is inside the corners BBOX of the selection rectangle

        Parameters
        -----------
        coords : Vector2
            The coords that is going to be checked for every corner

        Return
        -----------
        bool
            Boolean if the coords are inside the corners BBOX
        """
        for i in range(len(self.cornersBbox)):
            corner = self.cornersBbox[i]
            if corner.isInside(coords):
                self.selectedCornerIndex = i
                return True
        self.selectedCornerIndex = -1
        return False
    
    def isOutsideCorners(self, coords: Vector2) -> bool:
        """
        Check if a coordinates is outside the corners BBOX of the selection rectangle

        Parameters
        -----------
        coords : Vector2
            The coords that is going to be checked for every corner

        Return
        -----------
        bool
            Boolean if the coords are outside the corners BBOX
        """
        for i in range(len(self.cornersBbox)):
            corner = self.cornersBbox[i]
            if corner.isInside(coords):
                self.selectedCornerIndex = i
                return False
        self.selectedCornerIndex = -1
        return True

    def getSelectedCorner(self, coords: Vector2) -> int:
        for i in range(len(self.cornersBbox)):
            corner = self.cornersBbox[i]
            if corner.isInside(coords):
                return i
        return -1

    def isOutside(self, other) -> bool:
        """
        Check if a coordinates is outside the corners BBOX and the selection rectangle

        Parameters
        -----------
        coords : Vector2
            The coords that is going to be checked

        Return
        -----------
        bool
            Boolean if the coords are outside the corners BBOX and the selection rectangle
        """
        if super().isOutside(other) and self.isOutsideCorners(other):
            return True
        return False

    def checkBounds(self) -> bool:
        if (self.topLeft.x >= self.topRight.x
            or self.topLeft.y >= self.bottomLeft.y
            or self.topRight.x <= self.topLeft.x
            or self.topRight.y >= self.bottomRight.y
            or self.bottomLeft.x >= self.bottomRight.x
            or self.bottomLeft.y <= self.topLeft.y
            or self.bottomRight.x <= self.bottomLeft.x
            or self.bottomRight.y <= self.topRight.y):
            return True
        return False

    #endregion Public Methods