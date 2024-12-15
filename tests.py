from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Shapes.rectangle import Rectangle
from DrawLibrary.Core.Collision.aabb import AABB
from Model.selectionRectangle import SelectionRectangle

rectangle = Rectangle.fromCoordinates(1, 1, 5, 5)
print(rectangle)
aabb = AABB.fromCoordinates(1,1,5,5)
aabb.top = 2
print(aabb)
sr = SelectionRectangle.fromCoordinates(1, 1, 5, 5)
sr.top = 2
print(sr)