from Controller.canvasController import CanvasController

from DrawScript.Core.globals import GLOBAL_SYMBOLS_FUNCTIONS, GLOBAL_SYMBOLS_CURSOR_FUNCTIONS

class DrawScriptDeserializerC:
    def __init__(self, ast_nodes, canvasController : CanvasController = None):
        self.ast_nodes = ast_nodes
        self.code = ""
        self.current_color = [0, 0, 0, 255] # Default is black
        self.CC = canvasController

    def write_c(self):
        f = open("body.c", "r")
        code = f.read()

        insert_globals = code.find("// INSERT GLOBALS")
        if self.CC != None:
            globals = f'#define SCREEN_WIDTH {self.CC.view.winfo_width()}\n#define SCREEN_HEIGHT {self.CC.view.winfo_height()}\n\n'
        else:
            globals = f'#define SCREEN_WIDTH 800\n#define SCREEN_HEIGHT 600\n\n'
        code = code[:insert_globals] + globals + code[insert_globals:]

        insert_variables = code.find("// INSERT VARIABLES")
        variables = ""  
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] == "var_declaration":
                variables +=  self.deserialize_node_type(ast_node) 
        code = code[:insert_variables] + variables + code[insert_variables:]

        insert_drawings = code.find("// INSERT DRAWINGS")
        drawings = ""
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] != "var_declaration":
                drawings +=  self.deserialize_node_type(ast_node) 
        code = code[:insert_drawings] + drawings + code[insert_drawings:]
        
        f.close()

        w = open("main.c", "w")
        w.write(code)
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
            return ast_node["value"]
        elif ast_node["node_type"] == "if_statement":
            return self.deserialize_if_statement(ast_node)
        elif ast_node["node_type"] == "number":
            return str(ast_node["value"])
        elif ast_node["node_type"] == "for_statement":
            return self.deserialize_for_statement(ast_node)
        elif ast_node["node_type"] == "function_declaration":
            return self.code[:self.line_test] + self.deserialize_function_declaration(ast_node) + self.code[self.line_test:]
        elif ast_node["node_type"] == "var_declaration":
            return self.deserialize_var_declaration(ast_node) + "\n"
        elif ast_node["node_type"] == "while_statement":
            return self.deserialize_while_statement(ast_node)
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
        if method == "move":
            return f'Cursor_Move({cursor_name}, {arguments[0]["value"]}, {arguments[1]["value"]});\n'
        elif method == "rotate":
            return f'Cursor_Rotate({cursor_name}, {arguments[0]["value"]});\n'
        elif method == "drawCircle":
            return f'Cursor_DrawCircle({cursor_name}, renderer, {arguments[0]["value"]});\n'
        elif method == "drawSquare":
            return f'Cursor_DrawRectangle({cursor_name}, renderer, {arguments[0]["value"]}, {arguments[1]["value"]});\n'
        elif method == "drawSegment":
            return f'Cursor_DrawSegment({cursor_name}, renderer, {arguments[0]["value"]}, {arguments[1]["value"]});\n'

        return ""

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
        # Add detect type if type == ""
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
                
    def deserialize_block(self, ast_node):
        statements = self.deserialize_statements(ast_node)
        return f'{{\n{statements}}}\n'
    
    def deserialize_statements(self, ast_node):
        deserialize = ""
        for statement in ast_node["statements"]:
            deserialize += "\t"
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
            if callee == "drawCircle":
                deserialized = f'circleRGBA(renderer, {arguments_deserialized}, {self.current_color[0]}, {self.current_color[1]}, {self.current_color[2]}, {self.current_color[3]});\n'
                deserialized += f'fprintf(file, "%d,%d\\n", (int){arguments[0]["value"]}, (int){arguments[1]["value"]})'
            else:
                print(callee)

        return deserialized