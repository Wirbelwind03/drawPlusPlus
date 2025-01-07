import tkinter as tk

from tkinter import filedialog
from tkinter import font

from DrawScript.Core.drawScriptParser import DrawScriptParser

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool
from Controller.canvasController import CanvasController
from Controller.debugCanvasController import DebugCanvasController
from Controller.scriptEditorController import ScriptEditorController
from Controller.menuBarController import MenuBarController
from Controller.mainBarController import MainBarController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController
from Controller.settingsWindowController import SettingsWindowController

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.toolManager import ToolManager

from View.mainFrame import MainFrame
from View.Resources.Widgets.gear import GearWindow

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

        self.SC = SettingsWindowController("appSettings.json")

        # Create a tool manager for the canvas controller
        canvasToolManager = ToolManager()
        #
        self.DCC = DebugCanvasController(self.view.canvas)
        # Attach the canvas controller to the main controller
        self.CC = CanvasController(self.view.canvas, canvasToolManager)
        # Attach the selection rectangle canvas controller to the canvas
        # It's used to control the selection rectangle when it's on the canvas
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.CC)
        # Attach the tools to the canvas controller and the selection rectangle controller
        # Since each of them has a selection rectangle, it's attached to the selection rectangle controller
        canvasToolManager.addTool("SELECTION_TOOL", SelectionTool(self.SRCC))
        canvasToolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.SRCC))
        canvasToolManager.setActiveTool("SELECTION_TOOL")
        # Attach the script editor controller to the main controller
        self.SEC = ScriptEditorController(self.view.textEditor, self.view.terminal, self.CC)
        # Attach the menu bar controller to the main controller
        self.MBC = MenuBarController(self.view.menuBar, self.SEC)
        self.MainBarController = MainBarController(self.view.mainBar, self.SC)
        self.MainBarController.set_event_setting_window_close(self.refresh_widgets)

        # Refresh the widget to apply the settings
        self.refresh_widgets()

    def start(self):
        pass

    def refresh_widgets(self):
        if self.SC.settings == None: return

        # Apply the settings to the widgets
        self.view.textEditor.refresh(self.SC.settings)
