import tkinter as tk
from PIL import Image, ImageTk

from Model.canvasImage import CanvasImage
from Controller.selectionTool import SelectionTool

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)
        self.imgs = []
        self.currentImageId = 0
        self.selectionTool = SelectionTool(self)
        
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Motion>", self.on_mouse_over)
        self.bind('<Control-Key-x>', self.on_control_x)

    def update(self):
        for image in self.imgs:
            self.create_image(image.coordinates.x, image.coordinates.y, anchor=tk.NW, image=image.photoImage)

    def drawImage(self, filePath):
        #image = self.cropImage(image)
        canvasImage = CanvasImage(self.currentImageId, 0, 0)
        canvasImage.loadImage(filePath)
        self.imgs.append(canvasImage)
        
        self.create_image(canvasImage.coordinates.x, canvasImage.coordinates.y, anchor=tk.NW, image=canvasImage.photoImage)
        self.currentImageId += 1

    def on_mouse_over(self, event):
        self.selectionTool.on_mouse_over(event)

    def on_button_press(self, event):
        self.focus_set()

        self.selectionTool.on_button_press(event)
        
    def on_mouse_drag(self, event):
        self.selectionTool.on_mouse_drag(event)

    def on_button_release(self, event):
        self.selectionTool.on_button_release(event)

    def on_control_x(self, event):
        
        for img in self.imgs:
            # check overlap with image and selection tool
            
            pass

        self.update()