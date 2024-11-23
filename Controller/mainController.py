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
    """
    The controller where everything is handled, hence why the name "mainController"

    Attributes
    -----------
    view : MainFrame
        The view where the controller is going to be attached to
    CC : CanvasController
        A Controller used to communicate with the Canvas
    SRCC : SelectionRectangleCanvasController
        A Controller used to communicate with the Selection Rectangle that is on the Canvas
    SEC : ScriptEditorController
        A Controller used to communicate with the text editor and the terminal used for the drawScript
    MBC : MenuBarController
        A Controller used to communicate with the menu bar
    """

    def __init__(self, view: MainFrame) -> None:
        """
        The constructor for the MainController

        Parameters
        -----------
        view : MainFrame
            The view where the controller is going to be attached to
        """
        self.view = view

        # Create a tool manager for the canvas controller
        canvasToolManager = ToolManager()
        # Attach the canvas controller to the main controller
        self.CC = CanvasController(self.view.canvas, canvasToolManager)
        # Attach the selection rectangle canvas controller to the canvas
        # It's used to control the selection rectangle when it's on the canvas
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.CC)
        # Attach the tools to the canvas controller and the selection rectangle controller
        # Since each of them has a selection rectangle, it's attached to the selection rectangle controller
        canvasToolManager.addTool("SELECTION_TOOL", SelectionTool(self.CC, self.SRCC))
        canvasToolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.CC, self.SRCC))
        canvasToolManager.setActiveTool("SELECTION_TOOL")
        # Attach the script editor controller to the main controller
        self.SEC = ScriptEditorController(self.view.textEditor, self.view.terminal, self.CC)
        # Attach the menu bar controller to the main controller
        self.MBC = MenuBarController(self.view.menuBar, self.SEC)
    
    def start(self):
        circleImage = CanvasImage()
        circleImage.load("Data/Assets/circle.jpg")

        self.CC.drawImage(circleImage, 0, 0, 256, 256)
        self.CC.drawImage(circleImage, 256, 0, 256, 256)