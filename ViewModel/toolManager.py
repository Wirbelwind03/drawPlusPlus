class ToolManager:
    def __init__(self) -> None:
        self.tools: dict = {
        }
        self.activeTool = None

    def addTool(self, toolName: str, cls) -> None:
        self.tools[toolName] = cls

    def setActiveTool(self, toolName: str) -> None:
        if toolName in self.tools:
            self.active_tool = toolName

    def getActiveTool(self):
        return self.tools.get(self.active_tool)

    def invoke_tool_method(self, method_name: str, event) -> None:
        tool = self.getActiveTool()
        # Check if the event exist in the class
        if tool and hasattr(tool, method_name):
            # Call the event
            getattr(tool, method_name)(event)