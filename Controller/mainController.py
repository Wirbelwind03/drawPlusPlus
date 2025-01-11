import tkinter as tk

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool
from Controller.canvasController import CanvasController
from Controller.debugCanvasController import DebugCanvasController
from Controller.scriptEditorController import ScriptEditorController
from Controller.menuBarController import MenuBarController
from Controller.mainBarController import MainBarController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController
from Controller.settingsWindowController import SettingsWindowController
from Controller.toolBarController import ToolBarController

from DrawLibrary.Graphics.canvasImage import CanvasImage

from Model.toolManager import ToolManager

from View.mainFrame import MainFrame

class MainController:
    """
    The main controller act the as the central exchanger of all informations that is communicated in the application.
    It's used to ensure smooth communications between the different components (views and models).
    Each controller is used to handle a specific part of the application, like the canvas, the text editor, the terminal, etc.
    The main controller regroup every of those controller, to allow them to work together

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
        self.toolBarController = ToolBarController(self.view.toolBar, canvasToolManager)
        #
        self.DCC = DebugCanvasController(self.view.canvas)
        
        # Attach the canvas controller to the main controller
        self.CC = CanvasController(self.view.canvas, canvasToolManager, self.DCC)
        
        # Attach the selection rectangle canvas controller to the canvas
        # It's used to control the selection rectangle when it's on the canvas
        self.SRCC: SelectionRectangleCanvasController = SelectionRectangleCanvasController(self.CC, self.toolBarController)
        
        # Attach the tools to the canvas controller and the selection rectangle controller
        # Since each of them has a selection rectangle, it's attached to the selection rectangle controller
        canvasToolManager.addTool("SELECTION_TOOL", SelectionTool(self.SRCC))
        canvasToolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.SRCC, self.toolBarController))
        # Attach the script editor controller to the main controller
        self.SEC = ScriptEditorController(self.view.textEditor, self.view.terminal, self.CC)
        self.SEC.set_event_refresh_widgets(self.refresh_widgets)
        # Attach the menu bar controller to the main controller
        self.MBC = MenuBarController(self.view.menuBar, self.SEC)
        self.MainBarController = MainBarController(self.view.mainBar, self.SC)
        self.MainBarController.set_event_setting_window_close(self.refresh_widgets)

        # Refresh the widget to apply the settings
        self.refresh_widgets()

    def start(self) -> None:
        test = CanvasImage.fromPath("Data/Assets/trash.png")
        self.CC.drawImage(test, 698//2, 408//2, 128, 64)

    def refresh_widgets(self) -> None:
        """
        Refresh all the widget inside the mainController
        Used to change the color, font, etc.
        """
        # If there isn't any settings, stop this function since it's needed
        if self.SC.settings == None: return

        # Apply the settings to the widgets
        self.view.refresh_widgets(self.SC.settings)
        self.view.textEditor.refresh(self.SC.settings)
        self.view.terminal.refresh(self.SC.settings)
