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
            raise ValueError("x-coordinate cannot be < 0")
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
            raise ValueError("y-coordinate cannot be < 0")
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
        return min(self.x, self.x + self.width)
    
    @left.setter
    def left(self, value: int) -> None:
        """
        Resize the left side of the rectangle
        When changed, it move the x-coordinate to the left,
        and resize the width of the rectangle

        Parameters
        -----------
        value : int
            The new x-coordinate to place the rectangle to
        """
        if value < 0:
            raise ValueError("left cannot be < 0.")
        self.width += self.x - value
        self.x = value
    
    @property
    def top(self) -> int:
        return min(self.y, self.y + self.height)
    
    @top.setter
    def top(self, value: int) -> None:
        """
        Resize the top side of the rectangle
        When changed, it move the y-coordinate to the top,
        and resize the width of the rectangle

        Parameters
        -----------
        value : int
            The new y-coordinate to place the rectangle to
        """
        if value < 0:
            raise ValueError("top cannot be < 0.")
        self.height += self.y - value
        self.y = value
    
    @property
    def right(self) -> int:
        return max(self.x, self.x + self.width)
    
    @right.setter
    def right(self, value: int) -> None:
        """
        Resize the right side of the rectangle

        Parameters
        -----------
        value : int
            The new width to set to the rectangle
        """
        if value < 0:
            raise ValueError("right cannot be < 0.")
        self.width = value - self.x
    
    @property
    def bottom(self) -> int:
        return max(self.y, self.y + self.height)
    
    @bottom.setter
    def bottom(self, value: int) -> None:
        """
        Resize the bottom side of the rectangle

        Parameters
        -----------
        value : int
            The new height to set to the rectangle
        """
        if value < 0:
            raise ValueError("bottom cannot be < 0.")
        self.height = value - self.y

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
