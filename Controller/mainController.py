import tkinter as tk

from tkinter import filedialog

from DrawScript.Core.drawScriptParser import DrawScriptParser

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool
from Controller.canvasController import CanvasController
from Controller.scriptEditorController import ScriptEditorController
from Controller.menuBarController import MenuBarController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.toolManager import ToolManager

from View.mainFrame import MainFrame

class MainController:
    def __init__(self, view: MainFrame) -> None:
        self.view = view

        # Create a tool manager for the canvas controller
        self.canvasToolManager = ToolManager()
        # Attach the canvas controller to the main controller
        self.CC = CanvasController(self.view.canvas, self.canvasToolManager)
        # Attach the selection rectangle canvas controller to the canvas
        # It's used to control the selection rectangle when it's on the canvas
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.CC)
        # Attach the tools to the canvas and the selection rectangle controller
        # Since each of them has a selection rectangle, it's attached to the selection rectangle controller
        self.canvasToolManager.addTool("SELECTION_TOOL", SelectionTool(self.CC, self.SRCC))
        self.canvasToolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.CC, self.SRCC))
        self.canvasToolManager.setActiveTool("SELECTION_TOOL_RECTANGLE")

        self.SEC = ScriptEditorController(self.view.textEditor, self.view.terminal, self.CC)

        self.MBC = MenuBarController(self.view.menuBar, self.SEC)

        self.compiler = DrawScriptParser()

        circleImage = CanvasImage()
        circleImage.load("Data/Assets/circle.jpg")

        self.CC.drawImage(circleImage, 0, 0, 256, 256)
        self.CC.drawImage(circleImage, 256, 0, 256, 256)