from Core.Math.vector2 import Vector2

class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
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
        return self._startCoordinates

    @startCoordinates.setter
    def startCoordinates(self, newCoordinates):
        self._startCoordinates = newCoordinates
    
    @property
    def endCoordinates(self):
        return self._endCoordinates
    
    @endCoordinates.setter
    def endCoordinates(self, newCoordinates):
        self._endCoordinates = newCoordinates

    @property
    def width(self):
        return self._width

    def getArea(self):
        return self.width * self.height
    
    def getPerimeter(self):
        return (self.width + self.height) * 2