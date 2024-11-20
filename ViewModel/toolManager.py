from typing import Type

class ToolManager:
    def __init__(self) -> None:
        self.tools: dict[str, Type] = {
        }
        self.activeTool: str = ""

    def addTool(self, toolName: str, cls: Type) -> None:
        self.tools[toolName] = cls

    def setActiveTool(self, toolName: str) -> None:
        if toolName in self.tools:
            self.activeTool = toolName

    def getActiveTool(self) -> Type:
        return self.tools.get(self.activeTool)

    def invoke_tool_method(self, method_name: str, event) -> None:
        tool = self.getActiveTool()
        # Check if the event exist in the class
        if tool and hasattr(tool, method_name):
            # Call the event
            getattr(tool, method_name)(event)