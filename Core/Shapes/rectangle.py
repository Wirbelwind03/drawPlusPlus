from Core.Math.vector2 import Vector2

class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.coordinates = Vector2(x, y)
        self.width = width
        self.height = height

        self.topLeftCoords = self.coordinates
        self.topRightCoords = Vector2(self.coordinates.x + self.width, self.coordinates.y)
        self.bottomLeftCoords = Vector2(self.coordinates.x, self.coordinates.y + self.height)
        self.bottomRightCoords = Vector2(self.coordinates.x + self.width, self.coordinates.y + self.height)

    def getArea(self):
        return self.width * self.height
    
    def getPerimeter(self):
        return (self.width + self.height) * 2