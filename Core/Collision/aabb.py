from Core.Math.vector2 import Vector2
from Core.Shapes.rectangle import Rectangle

class AABB(Rectangle):
    def __init__(self, *args, **kwargs):
        Rectangle.__init__(self, *args, **kwargs)

    @classmethod
    def fromCoordinates(cls, x1, y1, x2, y2):
        # Top left coordinates
        xMin = min(x1, x2)
        yMin = min(y1, y2)
        # Bottom right coordinates
        xMax = max(x1, x2)
        yMax = max(y1, y2)
        return Rectangle.fromCoordinates(cls, xMin, yMin, xMax, yMax)

    def isInside(self, other):
        if isinstance(other, Vector2):
            return (other.x > self.startCoordinates.x and other.x < self.endCoordinates.x and 
                    other.y > self.startCoordinates.y and other.y < self.endCoordinates.y)
        
        return False
    
    def isOutside(self, other):
        if isinstance(other, Vector2):
            return (other.x < self.startCoordinates.x and other.x > self.endCoordinates.x and
                    other.y < self.startCoordinates.y and other.y > self.endCoordinates.y)
        
        return False

    def isIntersecting(self, other):
        if isinstance(other, Rectangle):
            if self.topRight.x < other.topLeft.x or other.topRight.x < self.topLeft.x:
                return False
            
            if self.bottomRight.y < other.topRight.y or other.bottomRight.y < self.topRight.y:
                return False
            
            return True

        return False
    
    def getIntersectRectangle(self, other):
        if isinstance(other, Rectangle):
            x1 = max(self.topLeft.x, other.topLeft.x)
            y1 = max(self.topRight.y, other.topRight.y)
            x2 = min(self.topRight.x, other.topRight.x)
            y2 = min(self.bottomRight.y, other.bottomRight.y)
            return AABB.fromCoordinates(x1, y1, x2, y2)

        return None