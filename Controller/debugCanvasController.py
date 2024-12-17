import tkinter as tk

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.debugCanvasEntity import DebugCanvasEntity

class DebugCanvasController:
    def __init__(self, view: tk.Canvas):
        self.view = view
        self.debugCanvas = {}

    def addCanvasID(self, canvasImage: CanvasImage):
        self.debugCanvas[canvasImage.id] = DebugCanvasEntity()

    def drawCanvasImageDebugInfos(self, canvasImage: CanvasImage):
        debugCanvasEntity: DebugCanvasEntity = self.debugCanvas[canvasImage.id]

        self.erase(canvasImage)

        bbox = canvasImage.bbox
        debugCanvasEntity.canvasID.append(self.view.create_rectangle(bbox.min.x, bbox.min.y, bbox.max.x, bbox.max.y, outline="red", width=2))
        
        debugCanvasEntity.canvasID.append(self.view.create_text(bbox.topLeft.x, bbox.topLeft.y - 10, text=f"({bbox.topLeft.x}, {bbox.topLeft.y})", fill="red"))
        debugCanvasEntity.canvasID.append(self.view.create_text(bbox.topRight.x, bbox.topRight.y - 10, text=f"({bbox.topRight.x}, {bbox.topRight.y})", fill="red"))
        debugCanvasEntity.canvasID.append(self.view.create_text(bbox.bottomLeft.x, bbox.bottomLeft.y + 10, text=f"({bbox.bottomLeft.x}, {bbox.bottomLeft.y})", fill="red"))
        debugCanvasEntity.canvasID.append(self.view.create_text(bbox.bottomRight.x, bbox.bottomRight.y + 10, text=f"({bbox.bottomRight.x}, {bbox.bottomRight.y})", fill="red"))

        debugCanvasEntity.canvasID.append(self.view.create_text((bbox.min.x + bbox.max.x) / 2, bbox.min.y - 10, text=f"{bbox.width}", fill="green"))
        debugCanvasEntity.canvasID.append(self.view.create_text(bbox.max.x + 15, (bbox.min.y + bbox.max.y) / 2, text=f"{bbox.height}", fill="green"))

        self.drawCanvasImageCenter(canvasImage)

    def drawCanvasImageCenter(self, canvasImage: CanvasImage):
        debugCanvasEntity: DebugCanvasEntity = self.debugCanvas[canvasImage.id]

        bbox = canvasImage.bbox
        debugCanvasEntity.canvasID.append(self.view.create_line(bbox.topLeft.x, bbox.topLeft.y, bbox.center.x, bbox.center.y, fill="green"))
        debugCanvasEntity.canvasID.append(self.view.create_line(bbox.topRight.x, bbox.topRight.y, bbox.center.x, bbox.center.y, fill="green"))
        debugCanvasEntity.canvasID.append(self.view.create_line(bbox.bottomLeft.x, bbox.bottomLeft.y, bbox.center.x, bbox.center.y, fill="green"))
        debugCanvasEntity.canvasID.append(self.view.create_line(bbox.bottomRight.x, bbox.bottomRight.y, bbox.center.x, bbox.center.y, fill="green"))

    def erase(self, canvasImage: CanvasImage):
        debugCanvasEntity: DebugCanvasEntity = self.debugCanvas[canvasImage.id]

        for canvasID in debugCanvasEntity.canvasID:
            self.view.delete(canvasID)
        debugCanvasEntity.canvasID.clear()