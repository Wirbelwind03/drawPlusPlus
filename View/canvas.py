import tkinter as tk
from PIL import Image, ImageTk

from Controller.selectionTool import SelectionTool

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        tk.Canvas.__init__(self, *args, **kwargs)
        self.imgs = []
        self.selectionTool = SelectionTool(self)

    def loadImage(self, filePath):
        img = ImageTk.PhotoImage(Image.open(filePath))
        self.imgs.append(img)
        self.create_image(256, 256, anchor=tk.NW, image=img)
