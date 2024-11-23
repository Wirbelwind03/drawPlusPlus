import tkinter as tk

from tkinter import filedialog

from DrawScript.Core.drawScriptParser import DrawScriptParser

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool
from Controller.canvasController import CanvasController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.toolManager import ToolManager

from View.mainFrame import MainFrame

class MainController:
    def __init__(self, view: MainFrame):
        self.view = view

        # Create a tool manager for the canvas controller
        self.canvasToolManager = ToolManager()
        # Attach the canvas controller to the main controller
        self.CC = CanvasController(self.view.canvas, self.canvasToolManager)
        # Attach the selection rectangle canvas controller to the canvas
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.CC.view, self.CC.model)
        # Attach the tools of the canvas to it and the selection rectangle
        self.canvasToolManager.addTool("SELECTION_TOOL", SelectionTool(self.CC.view, self.CC.model, self.CC, self.SRCC))
        self.canvasToolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.CC.view, self.CC.model, self.CC, self.SRCC))
        self.canvasToolManager.setActiveTool("SELECTION_TOOL")

        self.compiler = DrawScriptParser()

        circleImage = CanvasImage()
        circleImage.load("Data/Assets/circle.jpg")

        self.CC.drawImage(circleImage, 0, 0, 256, 256)
        self.CC.drawImage(circleImage, 256, 0, 256, 256)