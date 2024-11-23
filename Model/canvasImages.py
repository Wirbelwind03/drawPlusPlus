from DrawLibrary.Graphics.canvasImage import CanvasImage

class CanvasImages:
    def __init__(self) -> None:
        self.images: dict[int, CanvasImage] = {}

    def addImage(self, id: int, canvasImage: CanvasImage):
        self.images[id] = canvasImage

    def deleteImage(self, id):
        del self.images[id]