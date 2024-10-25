from math import sqrt

class Vector2:
    """
    A class to represent a 2D vector.

    Attributes:
    -----------
    x : float
        The x-coordinate of the vector.
    y : float
        The y-coordinate of the vector.
    """

    def __init__(self, x, y) -> None:
        """
        Construct a Vector2 instance.

        Parameters:
        -----------
        x : float
            The x-coordinate of the vector.
        y : float
            The y-coordinate of the vector.
        """
        self.x, self.y = x, y

    def __add__(self, other):
        """
        Adds another vector or a tuple to this vector.

        Parameters:
        -----------
        other : Vector2 or tuple
            The vector or tuple to add.

        Returns:
        --------
        Vector2
            A new Vector2 instance representing the sum.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Vector2(self.x - other[0], self.y - other[1])
        
    def __mul__(self, scalar):
        """
        Multiplies the vector by a scalar.

        Parameters:
        -----------
        scalar : float
            The scalar to multiply by.

        Returns:
        --------
        Vector2
            A new Vector2 instance representing the scaled vector.

        Raises:
        -------
        TypeError
            If the scalar is not a number.
        """
        if not isinstance(scalar, int) or not isinstance(scalar, float):
            raise TypeError()
        return Vector2(self.x * scalar, self.y * scalar)
        
    def __eq__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError()    
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        if isinstance(other, Vector2):
            return self.x < other.x and self.y < other.y
        else:
            raise TypeError()
        
    def __le__(self, other):
        if isinstance(other, Vector2):
            return self.x <= other.x and self.y <= other.y
        else:
            raise TypeError()
        
    def __gt__(self, other):
        if isinstance(other, Vector2):
            return self.x > other.x and self.y > other.y
        else:
            raise TypeError()
        
    def __ge__(self, other):
        if isinstance(other, Vector2):
            return self.x >= other.x and self.y >= other.y
        else:
            raise TypeError()
        

    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __abs__(self):
        return sqrt(self.x * self.x + self.y * self.y)