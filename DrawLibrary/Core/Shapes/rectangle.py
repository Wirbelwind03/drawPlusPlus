from DrawLibrary.Core.Math.vector2 import Vector2

class Rectangle:
    """
    A class to represent a rectangle in a 2D space.

    Attributes:
    -----------
    x : float
        The x coordinate of the top-left corner of the rectangle.
    y : float
        The y coordinate of the top-left corner of the rectangle.
    width : float
        The width of the rectangle.
    height : float
        The height of the rectangle.
    """

    def __init__(self, x=0, y=0, width=0, height=0):
        """
        Constructs a new rectangle instance with the specified position and dimensions.

        Parameters:
        -----------
        x : float
            The x coordinate of the top-left corner of the rectangle (default is 0).
        y : float
            The y coordinate of the top-left corner of the rectangle (default is 0).
        width : float
            The width of the rectangle (default is 0).
        height : float
            The height of the rectangle (default is 0).
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @classmethod
    def fromCoordinates(cls, x1, y1, x2, y2) -> 'Rectangle':
        width = x2 - x1
        height = y2 - y1
        return cls(x1, y1, width, height)

    @property
    def topLeft(self)  -> Vector2:
        return Vector2(self.x, self.y)
    
    @property
    def topRight(self)  -> Vector2:
        return Vector2(self.x + self.width, self.y)
    
    @property
    def bottomLeft(self)  -> Vector2:
        return Vector2(self.x, self.y + self.height)
    
    @property
    def bottomRight(self)  -> Vector2:
        return Vector2(self.x + self.width, self.y + self.height)

    def getArea(self):
        """
        Calculates the area of the rectangle.

        Returns:
        --------
        float
            The area of the rectangle.
        """
        return self.width * self.height
    
    def getPerimeter(self):
        """
        Calculates the perimeter of the rectangle.

        Returns:
        --------
        float
            The perimeter of the rectangle.
        """
        return (self.width + self.height) * 2