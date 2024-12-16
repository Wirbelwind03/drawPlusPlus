from enum import Enum

from DrawLibrary.Core.Math.vector2 import Vector2

class RectangleCorners(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class Rectangle:
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
    #region Constructor

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
        self.width: int = width
        self.height: int = height

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
    def x(self) -> int:
        """
        The x-coordinate of the rectangle
        """
        return self._x
    
    @x.setter
    def x(self, newValue: int):
        """
        Set the value for the x-coordinate of the rectangle
        When changed, it move the whole rectangle in x-coordinate
        It's cannot be < 0 since the library is for a tkinter canvas (where negative coordanites doesn't exist)

        Parameters
        -----------
        newValue : int
            The new x-coordinate to place the rectangle to
        """
        if newValue < 0:
            newValue = 0
        self._x = newValue

    @property
    def y(self) -> int:
        """
        The y-coordinate of the rectangle
        """
        return self._y
    
    @y.setter
    def y(self, newValue: int):
        """
        Set the value for the y-coordinate of the rectangle
        When changed, it move the whole rectangle in the y-coordinate
        It's cannot be < 0 since the library is for a tkinter canvas (where negative coordanites doesn't exist)

        Parameters
        -----------
        newValue : int
            The new y-coordinate to place the rectangle to
        """
        if newValue < 0:
            newValue = 0
        self._y = newValue

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, newValue: int):
        if newValue < 0:
            raise ValueError("Width cannot be < 0")
        self._width = newValue

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, newValue: int):
        if newValue < 0:
            raise ValueError("Width cannot be < 0")
        self._height = newValue

    @property
    def left(self) -> int:
        """
        Get the left boundary of the rectangle.

        Returns
        -------
        int
            The left boundary of the rectangle.
        """
        return min(self.x, self.x + self.width)
    
    @left.setter
    def left(self, value: int) -> None:
        """
        Set the left boundary of the rectangle. If the value exceeds the right boundary, 
        it will be clamped to the right boundary.

        Parameters
        ----------
        value : int
            The new left boundary value.
        """
        if value > self.right:
            value = self.right  # Clamp the left to be no greater than right
        self.width += self.x - value
        self.x = value
    
    @property
    def top(self) -> int:
        """
        Get the top boundary of the rectangle.

        Returns
        -------
        int
            The top boundary of the rectangle.
        """
        return min(self.y, self.y + self.height)
    
    @top.setter
    def top(self, value: int) -> None:
        """
        Set the top boundary of the rectangle. If the value exceeds the bottom boundary, 
        it will be clamped to the bottom boundary.

        Parameters
        ----------
        value : int
            The new top boundary value.
        """
        if value > self.bottom:
            value = self.bottom  # Clamp the top to be no greater than bottom
        self.height += self.y - value
        self.y = value
    
    @property
    def right(self) -> int:
        """
        Get the right boundary of the rectangle.

        Returns
        -------
        int
            The right boundary of the rectangle.
        """
        return max(self.x, self.x + self.width)
    
    @right.setter
    def right(self, value: int) -> None:
        """
        Set the right boundary of the rectangle. If the value is less than the left boundary,
        it will be clamped to the left boundary.

        Parameters
        ----------
        value : int
            The new right boundary value.
        """
        if value < self.left:
            value = self.left  # Clamp the right to be no less than left
        self.width = value - self.x
    
    @property
    def bottom(self) -> int:
        """
        Get the bottom boundary of the rectangle.

        Returns
        -------
        int
            The bottom boundary of the rectangle.
        """
        return max(self.y, self.y + self.height)
    
    @bottom.setter
    def bottom(self, value: int) -> None:
        """
        Set the bottom boundary of the rectangle. If the value is less than the top boundary, 
        it will be clamped to the top boundary.

        Parameters
        ----------
        value : int
            The new bottom boundary value.
        """
        if value < self.top:
            value = self.top  # Clamp the bottom to be no less than top
        self.height = value - self.y

    @property
    def center(self) -> Vector2:
        return Vector2(self.topLeft.x // 2, self.topLeft.y // 2)

    @property
    def topLeft(self) -> Vector2:
        return Vector2(self.left, self.top)
    
    @topLeft.setter
    def topLeft(self, value: Vector2) -> None:
        self.left = value.x
        self.top = value.y
        
    @property
    def topRight(self) -> Vector2:
        return Vector2(self.right, self.top)
    
    @topRight.setter
    def topRight(self, value: Vector2) -> None:
        self.right = value.x
        self.top = value.y
    
    @property
    def bottomLeft(self) -> Vector2:
        return Vector2(self.left, self.bottom)
    
    @bottomLeft.setter
    def bottomLeft(self, value: Vector2) -> None:
        self.left = value.x
        self.bottom = value.y
    
    @property
    def bottomRight(self) -> Vector2:
        return Vector2(self.right, self.bottom)
    
    @bottomRight.setter
    def bottomRight(self, value: Vector2) -> None:
        self.right = value.x
        self.bottom = value.y
    
    @property
    def corners(self) -> list:
        return [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
    
    #endregion Property

    def __repr__(self) -> str:
        return (
            f"Rectangle(\n"
            f"    x={self.x}, y={self.y}, width={self.width}, height={self.height},\n"
            f"    left={self.left}, right={self.right},\n"
            f"    top={self.top}, bottom={self.bottom},\n"
            f"    topLeft={self.topLeft}, topRight={self.topRight},\n"
            f"    bottomLeft={self.bottomLeft}, bottomRight={self.bottomRight}\n"
            f")"
        )
