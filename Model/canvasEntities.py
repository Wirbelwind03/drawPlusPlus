from DrawLibrary.Graphics.canvasImage import CanvasImage

class CanvasEntities:
    def __init__(self) -> None:
        self.images: dict[int, CanvasImage] = {}

    def addEntity(self, id: int, canvasImage: CanvasImage):
        self.images[id] = canvasImage

    def deleteEntity(self, id: int):
        del self.images[id]

    def deleteAll(self):
        self.images.clear()