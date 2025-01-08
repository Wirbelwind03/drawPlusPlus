from Model.toolManager import ToolManager

from View.Resources.Widgets.toolBar import ToolBar

class ToolBarController:
    def __init__(self, toolBar: ToolBar, toolManager : ToolManager):
        self.view = toolBar
        self.toolManager = toolManager

        self.view.mouseButton.configure(command=self.on_mouse_button_click)
        self.view.rectangleButton.configure(command=self.on_rectangle_button_click)
        
    def on_mouse_button_click(self):
        self.toolManager.setActiveTool("SELECTION_TOOL")

    def on_rectangle_button_click(self):
        self.toolManager.setActiveTool("SELECTION_TOOL_RECTANGLE")





