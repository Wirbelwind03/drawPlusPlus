from Controller.canvasController import CanvasController

from DrawScript.Core.globals import GLOBAL_SYMBOLS_FUNCTIONS, GLOBAL_SYMBOLS_CURSOR_FUNCTIONS, GLOBAL_SYMBOLS_VARIABLES

class DrawScriptDeserializerC:
    def __init__(self, ast_nodes, canvasController : CanvasController = None):
        self.ast_nodes = ast_nodes
        self.code = ""
        self.current_color = [0, 0, 0, 255] # Default is black
        self.CC = canvasController

    def write_c(self):
        bodyFile = open("body.c", "r")
        bodyCode = bodyFile.read()

        if self.CC != None:
            globals = f'#define SCREEN_WIDTH {self.CC.view.winfo_width()}\n#define SCREEN_HEIGHT {self.CC.view.winfo_height()}\n'
        else:
            globals = f'#define SCREEN_WIDTH 800\n#define SCREEN_HEIGHT 600\n'
        bodyCode = bodyCode.replace("// INSERT GLOBALS", globals)

        variables = ""  
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] == "var_declaration":
                variables +=  self.deserialize_node_type(ast_node) 
        bodyCode = bodyCode.replace("// INSERT VARIABLES", variables)

        drawings = ""
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] != "var_declaration":
                drawings +=  self.deserialize_node_type(ast_node) 
        bodyCode = bodyCode.replace("// INSERT DRAWINGS", drawings)
        
        bodyFile.close()

        w = open("main.c", "w")
        w.write(bodyCode)
        w.close()

    def detect_expression_type(self, ast_node):
        if ast_node["node_type"] == "binary_op" and ast_node["op"] == '/':
            return "float"
        elif ast_node["node_type"] == "binary_op":
            return "float"
        
        return ""
        
    def deserialize_node_type(self, ast_node):
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
            print(ast_node["node_type"])

        return ""
    
    def deserialize_cursor_declaration(self, ast_node):
        constructor_args = ast_node["constructor_args"]
        return f'Cursor* {ast_node["name"]} = Cursor_Constructor({constructor_args[0]["value"]}, {constructor_args[1]["value"]});\n'

    def deserialize_cursor_method(self, ast_node):
        cursor_name = ast_node["cursor_name"]
        method = ast_node["method"]
        arguments = ast_node["arguments"]

        def format_code(callee_name, *params):
            base_code = (
                f'snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);\n'
                f'{callee_name}({cursor_name}, renderer, SCREEN_WIDTH, SCREEN_HEIGHT, {", ".join(map(str, params))}, filename);\n'
                f'fprintf(file, "%d,%d\\n", (int){cursor_name}->x, (int){cursor_name}->y);\n'
                f'drawing_index++;\n'
            )
            return base_code

        deserialized = ""
        if method == "move":
            deserialized += f'Cursor_Move({cursor_name}, {arguments[0]["value"]}, {arguments[1]["value"]});\n'
        elif method == "rotate":
            deserialized += f'Cursor_Rotate({cursor_name}, {arguments[0]["value"]});\n'
        elif method == "drawCircle":
            radius = arguments[0]["value"]
            # Cursor_DrawCircle(radius)
            deserialized += format_code("Cursor_DrawCircle", radius)
        elif method == "drawRectangle":
            width, height = arguments[0]["value"], arguments[1]["value"]
            # Cursor_DrawRectangle(width, height) 
            deserialized += format_code("Cursor_DrawRectangle", width, height)
        elif method == "drawSegment":
            length = arguments[0]["value"]
            # Cursor_DrawSegment(length)
            deserialized += format_code("Cursor_DrawSegment", length)

        return deserialized

    def deserialize_function_declaration(self, ast_node):
        params = ""
        for i in range(len(ast_node["params"])):
            params += f'{ast_node["params"][i]}'
            if i != len(ast_node["params"]) - 1:
                params += ","
        body = self.deserialize_block(ast_node["body"])
        return f'void {ast_node["name"]}({params}){body}'

    def deserialize_for_statement(self, ast_node):
        init = self.deserialize_var_declaration(ast_node["init"])
        condition = self.deserialize_binary_op(ast_node["condition"])
        increment = self.deserialize_binary_op(ast_node["increment"])
        body = self.deserialize_block(ast_node["body"])
        return f'for (int {init} {condition}; {increment})\n{body}'

    def deserialize_var_declaration(self, ast_node):
        type = ""
        if ast_node["type"] != None:
            type = f'{ast_node["type"]}'
        expression = self.deserialize_node_type(ast_node["expression"])
        if type == "" : type = self.detect_expression_type(ast_node["expression"])
        return f'{type} {ast_node["name"]} = {expression};'
    
    def deserialize_binary_op(self, ast_node):
        left = self.deserialize_node_type(ast_node["left"])
        right = self.deserialize_node_type(ast_node["right"])
        op = ast_node["op"]
        return f"({left} {op} {right})"
    
    def deserialize_if_statement(self, ast_node):
        condition = f'({self.deserialize_node_type(ast_node["condition"])})'
        then_block = self.deserialize_block(ast_node["then_block"])
        else_block = self.deserialize_block(ast_node["else_block"])
        return f'if {condition} {then_block} else\n{else_block}'
    
    def deserialize_while_statement(self, ast_node):
        condition = self.deserialize_node_type(ast_node["condition"])
        body = self.deserialize_block(ast_node["body"])
        return f'while({condition})\n{body}'

    def deserialize_do_while_statement(self, ast_node):
        condition = self.deserialize_node_type(ast_node["condition"])
        body = self.deserialize_block(ast_node["body"])
        # Ajout d'un point-virgule final
        return f'do\n{body} while({condition});\n'
                
    def deserialize_block(self, ast_node):
        statements = self.deserialize_statements(ast_node)
        return f'{{\n{statements}}}\n'
    
    def deserialize_statements(self, ast_node):
        deserialize = ""
        for statement in ast_node["statements"]:
            deserialize += self.deserialize_node_type(statement)
        return deserialize
    
    def deserialize_expression_statement(self, ast_node):
        expression = self.deserialize_node_type(ast_node["expression"])
        return f'{expression};\n'
    
    def deserialize_call_expr(self, ast_node):
        deserialized = ""

        callee = ast_node["callee"]
        
        arguments = ast_node["arguments"]
        arguments_deserialized = ""
        for i in range(len(ast_node["arguments"])):
            arguments_deserialized += self.deserialize_node_type(ast_node["arguments"][i])
            if i != len(ast_node["arguments"]) - 1:
                arguments_deserialized += ", "

        deserialized = f'{callee}({arguments_deserialized})'

        if callee in GLOBAL_SYMBOLS_FUNCTIONS:
            def format_code(callee_name, *params):
                base_code = (
                    f'snprintf(filename, sizeof(filename), "Data/Outputs/drawing_%d.bmp", drawing_index);\n'
                    f'{callee_name}(renderer, SCREEN_WIDTH, SCREEN_HEIGHT, {", ".join(map(str, params))}, filename);\n'
                    f'fprintf(file, "%d,%d\\n", (int){params[0]}, (int){params[1]});\n'
                    f'drawing_index++;\n'
                )
                return base_code

            deserialized = ""
            r, g, b, a = self.current_color

            # drawCircle(x, y, radius, r, g, b, a)
            if callee == "drawCircle":
                x, y, radius = (arg["value"] for arg in arguments[:3])
                deserialized += format_code("drawCircle", x, y, radius, r, g, b, a)
            # drawSegment(x0, y0, x1, y1, int thickness, r, g, b, a);
            elif callee == "drawSegment":
                x0, y0, x1, y1 = (arg["value"] for arg in arguments[:4])
                deserialized += format_code("drawSegment", x0, y0, x1, y1, 1, r, g, b, a)
            # drawRectangle(x, y, width, height, angle, r, g, b, a);
            elif callee == "drawRectangle":
                x, y, width, height = (arg["value"] for arg in arguments[:4])
                deserialized += format_code("drawRectangle", x, y, width, height, 0, r, g, b, a)
            else:
                print(callee)

        return deserialized