from math import sqrt

class Vector2:
    """
    A class to represent a 2D vector.

    Attributes
    -----------
    x : float
        The x-coordinate of the vector.
    y : float
        The y-coordinate of the vector.
    """
    #region Constructor
    
    def __init__(self, x=0, y=0) -> None:
        """
        Construct a Vector2 instance.

        Parameters
        -----------
        x : float
            The x-coordinate of the vector.
        y : float
            The y-coordinate of the vector.
        """
        self.x, self.y = x, y
    
    #endregion Constructor

    def __add__(self, other) -> 'Vector2':
        """
        Adds another vector or a tuple to this vector.

        Parameters
        -----------
        other : Vector2 or tuple
            The vector or tuple to add.

        Returns
        --------
        Vector2
            A new Vector2 instance representing the sum.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])
        elif isinstance(other, int):
            return Vector2(self.x + other, self.y + other)
        else:
            raise TypeError()

    def __sub__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Vector2(self.x - other[0], self.y - other[1])
        elif isinstance(other, int):
            return Vector2(self.x - other, self.y - other)
        else:
            raise TypeError()
        
    def __mul__(self, scalar) -> 'Vector2':
        """
        Multiplies the vector by a scalar.

        Parameters
        -----------
        scalar : float
            The scalar to multiply by.

        Returns
        --------
        Vector2
            A new Vector2 instance representing the scaled vector.

        Raises
        -------
        TypeError
            If the scalar is not a number.
        """
        if not isinstance(scalar, int) or not isinstance(scalar, float):
            raise TypeError()
        return Vector2(self.x * scalar, self.y * scalar)
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2):
            raise TypeError()    
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Vector2):
            return self.x < other.x and self.y < other.y
        else:
            raise TypeError()
        
    def __le__(self, other) -> bool:
        if isinstance(other, Vector2):
            return self.x <= other.x and self.y <= other.y
        else:
            raise TypeError()
        
    def __gt__(self, other) -> bool:
        if isinstance(other, Vector2):
            return self.x > other.x and self.y > other.y
        else:
            raise TypeError()
        
    def __ge__(self, other) -> bool:
        if isinstance(other, Vector2):
            return self.x >= other.x and self.y >= other.y
        else:
            raise TypeError()
        
    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)
    
    def __abs__(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)
    
    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'