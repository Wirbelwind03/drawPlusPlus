import tkinter as tk

from tkinter import filedialog

from DrawScript.Core.drawScriptParser import DrawScriptParser

from Controller.canvasController import CanvasController

from DrawLibrary.Graphics.canvasImage import CanvasImage

class MainController:
    def __init__(self, view):
        self.view = view
        self.CC = CanvasController(self.view.canvas)

        circleImage = CanvasImage()
        circleImage.load("Data/Assets/circle.jpg")

        self.CC.drawImage(circleImage, 0, 0, 256, 256)
        self.CC.drawImage(circleImage, 256, 0, 256, 256)