from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Shapes.rectangle import Rectangle

class AABB(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = Vector2(min(self.x, self.x + self.width), min(self.y, self.y + self.height))
        self.max = Vector2(max(self.x, self.x + self.width), max(self.y, self.y + self.height))

    @classmethod
    def fromCoordinates(cls, x1, y1, x2, y2) -> 'AABB':
        """
        Create a AABB from start and end coordinates

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
        AABB
            The new AABB created from the arguments
        """
        # Top left coordinates
        xMin = min(x1, x2)
        yMin = min(y1, y2)
        # Bottom right coordinates
        xMax = max(x1, x2)
        yMax = max(y1, y2)
        return super().fromCoordinates(xMin, yMin, xMax, yMax)
    
    @property
    def topLeft(self) -> Vector2:
        return Vector2(self.min.x, self.min.y)
    
    @property
    def topRight(self) -> Vector2:
        return Vector2(self.max.x, self.min.y)
    
    @property
    def bottomLeft(self) -> Vector2:
        return Vector2(self.min.x, self.max.y)
    
    @property
    def bottomRight(self) -> Vector2:
        return Vector2(self.max.x, self.max.y)
    
    @property
    def corners(self) -> list:
        return [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]

    def isInside(self, other) -> bool:
        """
        Check if the object entered as argument is inside the AABB

        Parameters
        -----------
        other: Vector2
            The object checked with the AABB

        Returns
        -----------
        bool
            Boolean if the objest as argument is inside or not the ABB
        """
        if isinstance(other, Vector2):
            return (other.x > self.min.x and other.x < self.max.x and 
                    other.y > self.min.y and other.y < self.max.y)
        
        return False
    
    def isOutside(self, other) -> bool:
        """
        Check if the object entered as argument is outside the AABB

        Parameters
        -----------
        other: Vector2
            The object checked with the AABB

        Returns
        -----------
        bool
            Boolean if the objest as argument is outside or not the ABB
        """
        if isinstance(other, Vector2):
            return (other.x < self.min.x or other.x > self.max.x or
                    other.y < self.min.y or other.y > self.max.y)
        
        return False

    def isIntersecting(self, other) -> bool:
        """
        Check if the object entered as argument is intersecting with the AABB

        Parameters
        -----------
        other: Rectangle
            The object checked with the AABB

        Returns
        -----------
        bool
            Boolean if the objest as argument is intersecting or not with the ABB
        """
        if isinstance(other, Rectangle):
            if self.topRight.x < other.topLeft.x or other.topRight.x < self.topLeft.x:
                return False
            
            if self.bottomRight.y < other.topRight.y or other.bottomRight.y < self.topRight.y:
                return False
            
            return True

        return False
    
    def getIntersectRectangle(self, other) -> 'AABB':
        if isinstance(other, Rectangle):
            # Top-left corner of the intersecting rectangle
            x1 = max(self.topLeft.x, other.topLeft.x)
            y1 = max(self.topRight.y, other.topRight.y)
            # Bottom-right cornoer of the intersecting rectangle
            x2 = min(self.topRight.x, other.topRight.x)
            y2 = min(self.bottomRight.y, other.bottomRight.y)
            return AABB(x1 - other.topLeft.x, y1 - other.topLeft.y, x2 - x1, y2 - y1)

        return None