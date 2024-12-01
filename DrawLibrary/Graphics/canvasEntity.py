
from DrawLibrary.Core.Collision.aabb import AABB

class CanvasEntity:
    """
    A class representing a entity on a tk.Canvas

    Attributes
    -----------
    id : int
        The id of the CanvasEntity drawn on a tk.Canvas
    bbox : AABB
        The bounding box tied to the CanvasEntity
    debugBbox : int
        The ID of the debug rectangle rendered on a tk.Canvas
    """
    def __init__(self) -> None:
        self.id: int = -1
        self.bbox: AABB = None

        self.debugBbox: int = -1

    def createAABB(self, x, y, width=0, height=0):
        self.bbox = AABB(x, y, width, height)