import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum

from Model.canvasImage import CanvasImage
from Controller.canvasImageManager import CanvasImagesManager
from Controller.selectionTool import SelectionTool
from Controller.selectionToolRectangle import SelectionToolRectangle

class Tools(Enum):
    SELECTION_TOOL = 0
    SELECTION_TOOL_RECTANGLE = 1

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)
        self.canvasImagesManager = CanvasImagesManager(self)
        self.selectionTool = SelectionTool(self)
        self.selectionToolRectangle = SelectionToolRectangle(self)
        self.activeTool = Tools.SELECTION_TOOL_RECTANGLE
        
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Motion>", self.on_mouse_over)
        self.bind('<Control-Key-x>', self.on_control_x)

    def update(self):
        for imageId, image in self.canvasImagesManager.images.items():
            self.create_image(image.coordinates.x, image.coordinates.y, anchor=tk.NW, image=image.photoImage)

    def on_mouse_over(self, event):
        self._invoke_active_tool_method("on_mouse_over", event)

    def on_mouse_move(self, event):
        pass

    def on_button_press(self, event):
        self.focus_set()
        
        self._invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event):
        self._invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event):
        self._invoke_active_tool_method("on_button_release", event)

    def _invoke_active_tool_method(self, method_name, event):
        toolMap = {
            Tools.SELECTION_TOOL: self.selectionTool,
            Tools.SELECTION_TOOL_RECTANGLE: self.selectionToolRectangle,
        }

        tool = toolMap.get(self.activeTool)

        # If the tool exists and has the desired method, call it
        if tool and hasattr(tool, method_name):
            getattr(tool, method_name)(event)

    def on_control_x(self, event):
        if self.activeTool == Tools.SELECTION_TOOL_RECTANGLE:
            selectionToolRectangleBbox = self.selectionToolRectangle.bbox
            
            for imageId, image in self.canvasImagesManager.images.items():
                # check overlap with image and selection tool
                if selectionToolRectangleBbox.isIntersecting(image.bbox):
                    x1 = max(selectionToolRectangleBbox.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(selectionToolRectangleBbox.topRight.y, image.bbox.topRight.y)
                    x2 = min(selectionToolRectangleBbox.topRight.x, image.bbox.topRight.x)
                    y2 = min(selectionToolRectangleBbox.bottomRight.y, image.bbox.bottomRight.y)
                    #intersectRectangle = selectionToolBbox.getIntersectRectangle(canvasImage.bbox)
                    image.cutImage(x1, y1, x2 - x1, y2 - y1)
                    self.update()
                    #self.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
                    
            self.delete(self.selectionToolRectangle._debugBbox)