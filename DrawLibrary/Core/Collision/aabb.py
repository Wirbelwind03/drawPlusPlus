from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Shapes.rectangle import Rectangle

class AABB(Rectangle):
    """
    A class to represent a AABB (Axis Aligned Bounding Box).

    Attributes
    -----------
    _min : Vector2
        The minimum coordinates of the AABB (the top left corner).
        The min x-coordinate represent the left of the AABB.
        The min y-coordinate represent the top of the AABB.
    _max : Vector2
        The maximum coordinates of the AABB (the bottom right corner).
        The max x-coordinate represent the right of the AABB.
        The max y-coordinate represent the bottom of the AABB.
    """
    #region Constructor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = Vector2(self.left, self.top)
        self.max = Vector2(self.right, self.bottom)

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
    
    #endregion Constructor
    
    #region Property

    @property
    def min(self) -> Vector2:
        """
        Property for the minimum coordinates of the AABB instance

        Returns
        --------
        Vector2
            The minimum coordinates of the AABB instance
        """
        return self._min

    @min.setter
    def min(self, newValue: Vector2) -> None:
        """
        Set value for the minimum coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the minimum coordinates of the AABB instance 
        """
        self._min = newValue
        self.left = newValue.x
        self.top = newValue.y
    
    @property
    def max(self) -> Vector2:
        """
        Property for the maximum coordinates of the AABB instance

        Returns
        --------
        Vector2
            The maximum coordinates of the AABB instance
        """
        return self._max
    
    @max.setter
    def max(self, newValue: Vector2) -> None:
        """
        Set value for the maximum coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the maximum coordinates of the AABB instance 
        """
        self._max = newValue
        self.right = newValue.x
        self.bottom = newValue.y

    @property
    def topLeft(self) -> Vector2:
        """
        Property for the top left coordinates of the AABB instance

        Returns
        --------
        Vector2
            The top left coordinates of the AABB instance
        """
        return Vector2(self.min.x, self.min.y)
    
    @topLeft.setter
    def topLeft(self, newValue: Vector2) -> None:
        """
        Set value for the top left coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the top left coordinates of the AABB instance 
        """
        # The min represent the top left corner
        self.min = newValue
    
    @property
    def topRight(self) -> Vector2:
        """
        Property for the top right coordinates of the AABB instance

        Returns
        --------
        Vector2
            The top right coordinates of the AABB instance
        """
        return Vector2(self.max.x, self.min.y)
    
    @topRight.setter
    def topRight(self, newValue: Vector2) -> None:
        """
        Set value for the top right coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the top right coordinates of the AABB instance 
        """
        # The max x-coordinate represent the right
        self.max.x = newValue.x
        # The min y-coordinate represent the top
        self.min.y = newValue.y
        self.right = newValue.x
        self.top = newValue.y

    @property
    def bottomLeft(self) -> Vector2:
        """
        Property for the bottom left coordinates of the AABB instance

        Returns
        --------
        Vector2
            The bottom left coordinates of the AABB instance
        """
        return Vector2(self.min.x, self.max.y)
    
    @bottomLeft.setter
    def bottomLeft(self, newValue: Vector2) -> None:
        """
        Set value for the bottom left coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the bottom left coordinates of the AABB instance 
        """
        # The min x-coordinate represent the left
        self.min.x = newValue.x
        # The max y-coordinates represent the bottom
        self.max.y = newValue.y
        self.left = newValue.x
        self.bottom = newValue.y
    
    @property
    def bottomRight(self) -> Vector2:
        """
        Property for the bottom right coordinates of the AABB instance

        Returns
        --------
        Vector2
            The bottom right coordinates of the AABB instance
        """
        return Vector2(self.max.x, self.max.y)
    
    @bottomRight.setter
    def bottomRight(self, newValue: Vector2):
        """
        Set value for the bottom right coordinates of the AABB instance

        Parameters
        --------
        newValue : Vector2
            The new value for the bottom right coordinates of the AABB instance 
        """
        # The max represent the bottom right corner
        self.max = newValue
        
    #endregion Property

    def __repr__(self) -> str:
        return (
            f"AABB(\n"
            f"    x={self.x}, y={self.y}, width={self.width}, height={self.height},\n"
            f"    left={self.left}, right={self.right},\n"
            f"    top={self.top}, bottom={self.bottom},\n"
            f"    topLeft={self.topLeft}, topRight={self.topRight},\n"
            f"    bottomLeft={self.bottomLeft}, bottomRight={self.bottomRight}\n"
            f"    min={self.min}, max={self.max}\n"
            f")"
        )

    #region Public Methods

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
        
        else:
            raise TypeError()
    
    def getIntersectRectangle(self, other) -> 'AABB':
        if isinstance(other, Rectangle):
            # Top-left corner of the intersecting rectangle
            x1 = max(self.topLeft.x, other.topLeft.x)
            y1 = max(self.topRight.y, other.topRight.y)
            # Bottom-right cornoer of the intersecting rectangle
            x2 = min(self.topRight.x, other.topRight.x)
            y2 = min(self.bottomRight.y, other.bottomRight.y)
            return AABB(x1, y1, x2 - x1, y2 - y1)
        else:
            raise TypeError()
        
    #endregion Public Methods