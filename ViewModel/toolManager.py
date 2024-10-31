class ToolManager:
    def __init__(self):
        self.tools = {
        }
        self.activeTool = None

    def addTool(self, toolName, cls):
        self.tools[toolName] = cls

    def setActiveTool(self, toolName):
        if toolName in self.tools:
            self.active_tool = toolName

    def getActiveTool(self):
        return self.tools.get(self.active_tool)

    def invoke_tool_method(self, method_name, event):
        tool = self.getActiveTool()
        if tool and hasattr(tool, method_name):
            getattr(tool, method_name)(event)