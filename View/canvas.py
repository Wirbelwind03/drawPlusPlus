import tkinter as tk
from enum import Enum

from ViewModel.canvasVievModel import CanvasViewModel

class Tools(Enum):
    SELECTION_TOOL = 0
    SELECTION_TOOL_RECTANGLE = 1

class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.canvasViewModel = CanvasViewModel(self)
        
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Motion>", self.on_mouse_over)
        self.bind("<Delete>", self.on_delete)

    def _invoke_active_tool_method(self, method_name, event):
        tool = self.canvasViewModel.getActiveTool()
        # If the tool exists and has the desired method, call it
        if tool and hasattr(tool, method_name):
            getattr(tool, method_name)(event)

    def on_mouse_over(self, event):
        self._invoke_active_tool_method("on_mouse_over", event)

    def on_mouse_move(self, event):
        pass

    def on_button_press(self, event):
        self.focus_set()
        
        self._invoke_active_tool_method("on_button_press", event)

    def on_mouse_drag(self, event):
        self._invoke_active_tool_method("on_mouse_drag", event)

    def on_button_release(self, event):
        self._invoke_active_tool_method("on_button_release", event)

    def on_delete(self, event):
        self._invoke_active_tool_method("on_delete", event)