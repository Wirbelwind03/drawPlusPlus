from math import sqrt

class Vector2:

    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def __add__(self, other):
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
        if not isinstance(scalar, int) or not isinstance(scalar, float):
            raise TypeError()
        return Vector2(self.x * scalar, self.y * scalar)
        
    def __eq__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError()    
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __abs__(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def squareMagnitude(self):
        return self.x * self.x + self.y * self.y