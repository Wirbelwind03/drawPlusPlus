from Controller.canvasController import CanvasController

from DrawScript.Core.globals import GLOBAL_SYMBOLS_FUNCTIONS, GLOBAL_SYMBOLS_CURSOR_FUNCTIONS, GLOBAL_SYMBOLS_VARIABLES

class DrawScriptDeserializerC:
    def __init__(self, ast_nodes, canvasController: CanvasController = None):
        """
        Initializes the deserializer with an AST (list of nodes) and optionally a CanvasController.
        The CanvasController is used to determine the window dimensions for code generation.
        """
        self.ast_nodes = ast_nodes
        self.code = ""
        self.current_color = [0, 0, 0, 255]  # Default color is black (in RGBA)
        self.CC = canvasController

    def write_c(self):
        """
        Writes the generated C code by reading a base 'body.c' file and replacing specific markers
        with variable declarations and drawing instructions derived from the AST nodes.
        """
        self.write_globals()

        # Read the content of 'body.c', which serves as a template
        bodyFile = open("body.c", "r")
        bodyCode = bodyFile.read()
        bodyFile.close()

        # Insert variable declarations
        variables = ""  
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] == "var_declaration":
                variables += self.deserialize_node_type(ast_node) 
        bodyCode = bodyCode.replace("// INSERT VARIABLES", variables)

        # Insert drawing operations or other statements
        drawings = ""
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] != "var_declaration":
                drawings += self.deserialize_node_type(ast_node)
        bodyCode = bodyCode.replace("// INSERT DRAWINGS", drawings)

        # Write the final code to 'main.c'
        with open("main.c", "w") as w:
            w.write(bodyCode)

    def write_globals(self):
        """
        Writes a 'globals.h' header file containing macro definitions for screen width and height.
        If a CanvasController is available, the width and height are taken from its current view.
        Otherwise, default values are used.
        """
        if self.CC is not None:
            globals_code = (f'#define SCREEN_WIDTH {self.CC.view.winfo_width()}\n'
                            f'#define SCREEN_HEIGHT {self.CC.view.winfo_height()}\n')
        else:
            globals_code = f'#define SCREEN_WIDTH 800\n#define SCREEN_HEIGHT 600\n'

        base_code = (
            f'#ifndef GLOBALS_H\n'
            f'#define GLOBALS_H\n'
            f'\n'
            f'{globals_code}'
            f'\n'
            f'#endif'
        )

        # Write the generated globals to the header file
        with open("DrawLibrary/C/Utils/globals.h", "w") as file:
            file.write(base_code)

    def detect_expression_type(self, ast_node):
        """
        Attempts to detect the resulting type of an expression based on its node type.
        For division or binary operations, it defaults to 'float'.
        """
        if ast_node["node_type"] == "binary_op" and ast_node["op"] == '/':
            return "float"
        elif ast_node["node_type"] == "binary_op":
            return "float"
        
        return ""
        
    def deserialize_node_type(self, ast_node):
        """
        Dispatch method: selects the deserialization function based on 'node_type'.
        Returns a string representing the C code equivalent of the provided AST node.
        """
        if ast_node["node_type"] == "binary_op":
            return self.deserialize_binary_op(ast_node)
        elif ast_node["node_type"] == "bool_literal":
            return ast_node["value"]
        elif ast_node["node_type"] == "cursor_declaration":
            return self.deserialize_cursor_declaration(ast_node)
        elif ast_node["node_type"] == "cursor_method":
            return self.deserialize_cursor_method(ast_node)
        elif ast_node["node_type"] == "call_expr":
            return self.deserialize_call_expr(ast_node)
        elif ast_node["node_type"] == "expression_statement":
            return self.deserialize_expression_statement(ast_node)
        elif ast_node["node_type"] == "identifier":
            # If the identifier is in the global symbol table, use its mapped value; otherwise, return as is
            if ast_node["value"] in GLOBAL_SYMBOLS_VARIABLES:
                return GLOBAL_SYMBOLS_VARIABLES[ast_node["value"]]
            return ast_node["value"]
        elif ast_node["node_type"] == "if_statement":
            return self.deserialize_if_statement(ast_node)
        elif ast_node["node_type"] == "number":
            return str(ast_node["value"])
        elif ast_node["node_type"] == "for_statement":
            return self.deserialize_for_statement(ast_node)
        elif ast_node["node_type"] == "var_declaration":
            return self.deserialize_var_declaration(ast_node) + "\n"
        elif ast_node["node_type"] == "while_statement":
            return self.deserialize_while_statement(ast_node)
        elif ast_node["node_type"] == "do_while_statement":
            return self.deserialize_do_while_statement(ast_node)

        else:
            # If the node type isn't handled, print it for debugging purposes
            print(ast_node["node_type"])

        return ""
    
    def deserialize_cursor_declaration(self, ast_node):
        """
        Generates C code to declare and construct a Cursor object using the provided constructor arguments.
        Example: Cursor* c = Cursor_Constructor(x, y);
        """
        constructor_args = ast_node["constructor_args"]
        return (f'Cursor* {ast_node["name"]} = '
                f'Cursor_Constructor({constructor_args[0]["value"]}, {constructor_args[1]["value"]});\n')

    def deserialize_function_declaration(self, ast_node):
        """
        (Currently not used in the code)
        Generates a C function declaration with given parameters and body.
        """
        params = ""
        for i in range(len(ast_node["params"])):
            params += f'{ast_node["params"][i]}'
            if i != len(ast_node["params"]) - 1:
                params += ","
        body = self.deserialize_block(ast_node["body"])
        return f'void {ast_node["name"]}({params}){body}'

    def deserialize_for_statement(self, ast_node):
        """
        Generates C code for a for loop:
        - The initializer is treated as a variable declaration
        - The condition and increment are treated as binary expressions
        - The body is parsed as a block
        """
        init = self.deserialize_var_declaration(ast_node["init"])
        condition = self.deserialize_binary_op(ast_node["condition"])
        increment = self.deserialize_binary_op(ast_node["increment"])
        body = self.deserialize_block(ast_node["body"])
        return f'for (int {init} {condition}; {increment})\n{body}'

    def deserialize_var_declaration(self, ast_node):
        """
        Generates C code for a variable declaration, e.g., 'int x = 5;'.
        If the variable type is not specified, detect the type from the expression (defaults to float).
        """
        var_type = ""
        if ast_node["type"] is not None:
            var_type = f'{ast_node["type"]}'
        expression = self.deserialize_node_type(ast_node["expression"])
        if var_type == "":
            var_type = self.detect_expression_type(ast_node["expression"])
        return f'{var_type} {ast_node["name"]} = {expression};'
    
    def deserialize_binary_op(self, ast_node):
        """
        Generates C code for a binary operation, e.g., '(x + y)'.
        """
        left = self.deserialize_node_type(ast_node["left"])
        right = self.deserialize_node_type(ast_node["right"])
        op = ast_node["op"]
        return f"({left} {op} {right})"
    
    def deserialize_if_statement(self, ast_node):
        """
        Generates C code for an if statement with an optional else part.
        Example:
            if (condition) {
                ...
            } else {
                ...
            }
        """
        condition = f'({self.deserialize_node_type(ast_node["condition"])})'
        then_block = self.deserialize_block(ast_node["then_block"])
        else_block = self.deserialize_block(ast_node["else_block"])
        return f'if {condition} {then_block} else\n{else_block}'
    
    def deserialize_while_statement(self, ast_node):
        """
        Generates C code for a while loop.
        Example:
            while (condition) {
                ...
            }
        """
        condition = self.deserialize_node_type(ast_node["condition"])
        body = self.deserialize_block(ast_node["body"])
        return f'while({condition})\n{body}'

    def deserialize_do_while_statement(self, ast_node):
        """
        Generates C code for a do-while loop.
        Example:
            do {
                ...
            } while(condition);
        A semicolon is appended at the end of the block.
        """
        condition = self.deserialize_node_type(ast_node["condition"])
        body = self.deserialize_block(ast_node["body"])
        return f'do\n{body} while({condition});\n'
                
    def deserialize_block(self, ast_node):
        """
        Generates C code for a block of statements, enclosed in curly braces.
        """
        statements = self.deserialize_statements(ast_node)
        return f'{{\n{statements}}}\n'
    
    def deserialize_statements(self, ast_node):
        """
        Iterates through a list of statement nodes, deserializing each in turn.
        """
        deserialize = ""
        for statement in ast_node["statements"]:
            deserialize += self.deserialize_node_type(statement)
        return deserialize
    
    def deserialize_expression_statement(self, ast_node):
        """
        Deserializes an expression statement, ensuring it ends with a semicolon in C.
        """
        expression = self.deserialize_node_type(ast_node["expression"])
        return f'{expression};\n'
    
    def deserialize_call_expr(self, ast_node):
        """
        Generates C code for a function call. If the callee matches a known drawing function,
        special code is emitted to handle drawing operations (including file output).
        Otherwise, returns the default function call.
        """
        deserialized = ""

        callee = ast_node["callee"]
        
        arguments = []
        arguments_deserialized = ""
        for i in range(len(ast_node["arguments"])):
            argument_deserialized = self.deserialize_node_type(ast_node["arguments"][i])
            arguments.append(argument_deserialized)
            arguments_deserialized += argument_deserialized
            if i != len(ast_node["arguments"]) - 1:
                arguments_deserialized += ", "

        # Default function call: callee(arg1, arg2, ...)
        deserialized = f'{callee}({arguments_deserialized})'

        # Check if it's a known function from GLOBAL_SYMBOLS_FUNCTIONS,
        # which typically corresponds to drawing operations
        if callee in GLOBAL_SYMBOLS_FUNCTIONS:

            def format_code(callee_name, *params):
                """
                Helper function that generates the code snippet for drawing operations,
                including saving the output to a BMP file and printing coordinates.
                """
                base_code = (
                    f'snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);\n'
                    f'{callee_name}(renderer, {", ".join(map(str, params))}, filename);\n'
                    f'fprintf(file, "%d,%d\\n", (int){params[0]}, (int){params[1]});\n'
                    f'drawing_index++;\n'
                )
                return base_code

            deserialized = ""
            r, g, b, a = self.current_color

            # Depending on the function name, generate appropriate calls
            if callee == "drawCircle":
                x, y, radius = arguments[:3]
                deserialized += format_code("drawCircle", x, y, radius, r, g, b, a)
            elif callee == "drawFilledCircle":
                x, y, radius = arguments[:3]
                deserialized += format_code("drawFilledCircle", x, y, radius, r, g, b, a)
            elif callee == "drawEllipse":
                x, y, rx, ry = arguments[:4]
                deserialized += format_code("drawEllipse", x, y, rx, ry, 0, r, g, b, a)
            elif callee == "drawFilledEllipse":
                x, y, rx, ry = arguments[:4]
                deserialized += format_code("drawFilledEllipse", x, y, rx, ry, 0, r, g, b, a)
            elif callee == "drawRoundedRectangle":
                x, y, width, height, radius = arguments[:5]
                deserialized += format_code("drawRoundedRectangle", x, y, width, height, radius, 0, r, g, b, a)
            elif callee == "drawBox":
                x, y, width, height = arguments[:4]
                deserialized += format_code("drawBox", x, y, width, height, 0, r, g, b, a)
            elif callee == "drawRoundedBox":
                x, y, width, height, radius = arguments[:5]
                deserialized += format_code("drawRoundedBox", x, y, width, height, radius, 0, r, g, b, a)
            elif callee == "drawSegment":
                x0, y0, x1, y1 = arguments[:4]
                deserialized += format_code("drawSegment", x0, y0, x1, y1, 1, r, g, b, a)
            elif callee == "drawTriangle":
                x0, y0, x1, y1, x2, y2 = arguments[:6]
                deserialized += format_code("drawTriangle", x0, y0, x1, y1, x2, y2, 0, r, g, b, a)
            elif callee == "drawRectangle":
                x, y, width, height = arguments[:4]
                deserialized += format_code("drawRectangle", x, y, width, height, 0, r, g, b, a)
            elif callee == "setRGBA":
                r, g, b, a = arguments[:4]
                # Ensure the RGBA components do not exceed 255, and invert if over that limit
                r, g, b, a = [255 - int(value) if int(value) > 255 else int(value) for value in (r, g, b, a)]
                self.current_color = [r, g, b, a]
            else:
                # If the function is recognized but not specifically handled above, just print its name
                print(callee)

        return deserialized
    
    def deserialize_cursor_method(self, ast_node):
        """
        Generates C code for cursor methods (e.g., moving or drawing with a cursor).
        If the method is a known drawing method, it includes code to save the output and print coordinates.
        """
        cursor_name = ast_node["cursor_name"]
        method = ast_node["method"]
        
        arguments = []
        for i in range(len(ast_node["arguments"])):
            argument_deserialized = self.deserialize_node_type(ast_node["arguments"][i])
            arguments.append(argument_deserialized)

        def format_code(callee_name, *params):
            """
            Helper function for cursor drawing operations, similar to the one in deserialize_call_expr.
            """
            base_code = (
                f'snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);\n'
                f'{callee_name}({cursor_name}, renderer, {", ".join(map(str, params))}, filename);\n'
                f'fprintf(file, "%d,%d\\n", (int){cursor_name}->x, (int){cursor_name}->y);\n'
                f'drawing_index++;\n'
            )
            return base_code

        deserialized = ""
        if method == "move":
            # Moves the cursor by dx, dy
            deserialized += f'Cursor_Move({cursor_name}, {arguments[0]}, {arguments[1]});\n'
        elif method == "rotate":
            deserialized += f'Cursor_Rotate({cursor_name}, {arguments[0]});\n'
        elif method == "drawCircle":
            radius = arguments[0]
            deserialized += format_code("Cursor_DrawCircle", radius)
        elif method == "drawFilledCircle":
            radius = arguments[0]
            deserialized += format_code("Cursor_DrawFilledCircle", radius)
        elif method == "drawEllipse":
            rx, ry = arguments[:2]
            deserialized += format_code("Cursor_DrawEllipse", rx, ry)
        elif method == "drawFilledEllipse":
            rx, ry = arguments[:2]
            deserialized += format_code("Cursor_DrawFilledEllipse", rx, ry)
        elif method == "drawRoundedRectangle":
            width, height, radius = arguments[:3]
            deserialized += format_code("Cursor_DrawRoundedRectangle", width, height, radius)
        elif method == "drawBox":
            width, height = arguments[:2]
            deserialized += format_code("Cursor_DrawBox", width, height)
        elif method == "drawRoundedBox":
            width, height, radius = arguments[:3]
            deserialized += format_code("Cursor_DrawRoundedBox", width, height, radius)
        elif method == "drawRectangle":
            width, height = arguments[:2]
            deserialized += format_code("Cursor_DrawRectangle", width, height)
        elif method == "drawSegment":
            length = arguments[0]
            deserialized += format_code("Cursor_DrawSegment", length)
        elif method == "drawTriangle":
            x0, y0, x1, y1 = arguments[:4]
            deserialized += format_code("Cursor_DrawTriangle", x0, y0, x1, y1)
        elif method == "setRGBA":
            r, g, b, a = arguments[:4]
            r, g, b, a = [255 - int(value) if int(value) > 255 else int(value) for value in (r, g, b, a)]
            deserialized += format_code("Cursor_SetRGBA", r, g, b, a)

        return deserialized
