from Core.Math.vector2 import Vector2

class Rectangle:
    """
    A class to represent a rectangle in a 2D space.

    Attributes:
    -----------
    startCoordinates : Vector2
        The top-left corner coordinates of the rectangle.
    endCoordinates : Vector2
        The bottom-right corner coordinates of the rectangle.
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
        self.startCoordinates = Vector2(x, y)
        self.endCoordinates = Vector2(x + width, y + height)
        self.width = width
        self.height = height

        self.topLeftCoords = self.startCoordinates
        self.topRightCoords = Vector2(self.startCoordinates.x + self.width, self.startCoordinates.y)
        self.bottomLeftCoords = Vector2(self.startCoordinates.x, self.startCoordinates.y + self.height)
        self.bottomRightCoords = self.endCoordinates

    @property
    def startCoordinates(self):
        """Returns the top-left coordinates of the rectangle."""
        return self._startCoordinates

    @startCoordinates.setter
    def startCoordinates(self, newCoordinates):
        """Sets the top-left coordinates of the rectangle."""
        self._startCoordinates = newCoordinates
    
    @property
    def endCoordinates(self):
        """Returns the bottom-right coordinates of the rectangle."""
        return self._endCoordinates
    
    @endCoordinates.setter
    def endCoordinates(self, newCoordinates):
        """Sets the bottom-right coordinates of the rectangle."""
        self._endCoordinates = newCoordinates

    @property
    def width(self):
        return self._width

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