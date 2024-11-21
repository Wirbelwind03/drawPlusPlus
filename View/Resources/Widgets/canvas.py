import tkinter as tk
from enum import Enum

from Controller.canvasController import CanvasController
from Model.toolManager import ToolManager

from Controller.Tools.selectionTool import SelectionTool
from Controller.Tools.selectionRectangleTool import SelectionRectangleTool

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.CC = CanvasController(self)
        
        self.toolManager = ToolManager()
        self.toolManager.addTool("SELECTION_TOOL", SelectionTool(self.CC))
        self.toolManager.addTool("SELECTION_TOOL_RECTANGLE", SelectionRectangleTool(self.CC))
        self.toolManager.setActiveTool("SELECTION_TOOL")
        
        # Mouse events
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Motion>", self.on_mouse_over)
        
        # Key events
        self.bind("<Delete>", self.on_delete)
        self.bind("<Control-Key-c>", self.on_control_c)
        self.bind("<Control-Key-v>", self.on_control_v)

    def _invoke_active_tool_method(self, method_name, event):
        self.toolManager.invoke_tool_method(method_name, event)

    def on_mouse_over(self, event):
        self._invoke_active_tool_method("on_mouse_over", event)

    def on_button_press(self, event):
        self.focus_set()
        
        self._invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event):
        self._invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event):
        self._invoke_active_tool_method("on_button_release", event)

    def on_delete(self, event):
        self._invoke_active_tool_method("on_delete", event)

    def on_control_c(self, event):
        self._invoke_active_tool_method("on_control_c", event)

    def on_control_v(self, event):
        self._invoke_active_tool_method("on_control_v", event)