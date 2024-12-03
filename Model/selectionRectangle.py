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

        self.cornersBbox: list[AABB]  = []
        self.selectedCornerIndex: int = None
        
        self.canvasIdRectangle: int = -1
        self.canvasIdCorners: list[int] = []
        self.attachedImage: CanvasImage = None

        self.action: SelectionRectangleAction = SelectionRectangleAction.NONE

        for i in range(len(self.corners)):
            self.cornersBbox.append(AABB.fromCoordinates(self.corners[i].x - self.cornerSize, self.corners[i].y - self.cornerSize, self.corners[i].x + self.cornerSize, self.corners[i].y + self.cornerSize))

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
        super(SelectionRectangle, type(self)).topLeft.fset(self, newValue)
        self.__updateCornersBbox(3)

    @property
    def topRight(self) -> Vector2:
        return super().topRight
    
    @topRight.setter
    def topRight(self, newValue):
        super(SelectionRectangle, type(self)).topRight.fset(self, newValue)
        self.__updateCornersBbox(2)

    @property
    def bottomLeft(self) -> Vector2:
        return super().bottomLeft
    
    @bottomLeft.setter
    def bottomLeft(self, newValue):
        super(SelectionRectangle, type(self)).bottomLeft.fset(self, newValue)
        self.__updateCornersBbox(1)

    @property
    def bottomRight(self) -> Vector2:
        return super().bottomRight
    
    @bottomRight.setter
    def bottomRight(self, newValue):
        super(SelectionRectangle, type(self)).bottomRight.fset(self, newValue)
        self.__updateCornersBbox(0)

    #endregion

    #region Private Methods

    def __updateCornersBbox(self, cornerIndexToSkip):
        """
        Update the position of the corner BBOX

        Parameters
        -----------
        cornerIndexToSkip : int
            The index of the corner to skip
        """
        for i in range(len(self.cornersBbox)):
            if i != cornerIndexToSkip:
                bbox: AABB = self.cornersBbox[i]
                # Update the corner bbox
                bbox.min = self.corners[i] - self.cornerSize
                bbox.max = self.corners[i] + self.cornerSize
        
    #endregion Private Methods

    #region Public Methods

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

    #endregion Public Methods