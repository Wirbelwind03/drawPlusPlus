from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2

class RectangleCorners(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class Rectangle:
    #region Constructor

    """
    A class to represent a rectangle in a 2D space.

    Attributes
    -----------
    x : int
        The x coordinate of the top-left corner of the rectangle.
    y : int
        The y coordinate of the top-left corner of the rectangle.
    width : int
        The width of the rectangle.
    height : int
        The height of the rectangle.
    """

    def __init__(self, x:int = 0, y:int = 0, width:int = 0, height:int = 0):
        """
        Constructs a new rectangle instance with the specified position and dimensions.

        Parameters
        -----------
        x : int
            The x coordinate of the top-left corner of the rectangle (default is 0).
        y : int
            The y coordinate of the top-left corner of the rectangle (default is 0).
        width : int
            The width of the rectangle (default is 0).
        height : int
            The height of the rectangle (default is 0).
        """
        self.x: int = x
        self.y: int = y
        self._width: int = width
        self._height: int = height

    @classmethod
    def fromCoordinates(cls, x1: int, y1: int, x2: int, y2: int) -> 'Rectangle':
        """
        Create a Rectagle from start and end coordinates

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

        Returns
        --------
        Rectangle
            The new Rectangle created from the arguments coordinates
        """
        width = x2 - x1
        height = y2 - y1
        return cls(x1, y1, width, height)
    
    #endregion Constructor

    #region Property

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
    
    @property
    def center(self) -> Vector2:
        return Vector2(self.topLeft.x // 2, self.topLeft.y // 2)

    @property
    def topLeft(self) -> Vector2:
        return Vector2(min(self.x, self.x + self.width), min(self.y, self.y + self.height))
        
    @property
    def topRight(self) -> Vector2:
        return Vector2(max(self.x, self.x + self.width), min(self.y, self.y + self.height))
    
    @property
    def bottomLeft(self) -> Vector2:
        return Vector2(min(self.x, self.x + self.width), max(self.y, self.y + self.height))
    
    @property
    def bottomRight(self) -> Vector2:
        return Vector2(max(self.x, self.x + self.width), max(self.y, self.y + self.height))
    
    @property
    def corners(self) -> list:
        return [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
    
    #endregion Property

    #region Public Methods

    def getArea(self):
        """
        Calculates the area of the rectangle.

        Returns
        --------
        float
            The area of the rectangle.
        """
        return self.width * self.height
    
    def getPerimeter(self):
        """
        Calculates the perimeter of the rectangle.

        Returns
        --------
        float
            The perimeter of the rectangle.
        """
        return (self.width + self.height) * 2
    
    #endregion Public Methods