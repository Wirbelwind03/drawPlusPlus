from typing import Type

class ToolManager:
    """
    A model to manage the tools tied to a controller

    Attributes
    -----------
    tools : dict[str, Type]
        A dictionary that keep all the tools tied to a controller
        The key are the names of the tools
        The values are the class of the tools
    activeTool : str
        The name of the current active tool
    """
    def __init__(self) -> None:
        self.tools: dict[str, Type] = {
        }
        self.activeTool: str = ""

    def addTool(self, toolName: str, cls: Type) -> None:
        """
        Add a tool to the dictionary
        This function add to the dictionary the tool name as key
        And the class of the tool as value

        Parameters
        -----------
        toolName : str
            The tool name to be added in the dictionary as key
        cls : Type
            The tool class to be added in the dictionary as value
        """
        self.tools[toolName] = cls

    def setActiveTool(self, toolName: str) -> None:
        """
        Set the active tool with the name
        This function check if the tool name is present in the dictionary (thanks to the key)
        And if it is, then set it as the active tool.
        If not, throw a error.

        Parameters
        -----------
        toolName : str
            The tool name to be set as active
        """
        try:
            if toolName in self.tools:
                self.activeTool = toolName
        except Exception as e:
            raise TypeError()

    def getActiveTool(self) -> Type:
        """
        Get the active tool.

        Returns
        -----------
        Type
            The class of the tool
        """
        return self.tools.get(self.activeTool)

    def invoke_tool_method(self, method_name: str, event) -> None:
        # Get the current active tool class
        # So the function can be called
        tool = self.getActiveTool()
        # Check if the method_name entered as argument exist in the class of the tool
        # Example : "on_mouse_over" method exist in the selection tool, if it didn't, don't call it to avoid a error
        if tool and hasattr(tool, method_name):
            # Call the event
            getattr(tool, method_name)(event)