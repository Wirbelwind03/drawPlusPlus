class DrawScriptDeserializerC:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes
        self.line_test = 0
        self.code = ""

    def write_c(self):
        f = open("main.c", "w")
        
        self.code += "#include <SDL2/SDL.h>\n"
        self.code += "#include <stdbool.h>\n"
        self.code += "#include <stdio.h>\n"
        self.code += "\n"
        self.line_test = len(self.code)
        self.code += "int main(int argc, char *argv[])\n{\n"
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] != "function_declaration":
                self.code += self.deserialize_node_type(ast_node) 
            else:
                self.code = self.deserialize_node_type(ast_node) 
            print(self.code)
        self.code += "}\n"

        f.write(self.code)
        f.close()

    def detect_expression_type(self, ast_node):
        if ast_node["node_type"] == "binary_op" and ast_node["op"] == '/':
            return "float"
        elif ast_node["node_type"] == "binary_op":
            return "float"
        
    def deserialize_node_type(self, ast_node):
        if ast_node["node_type"] == "binary_op":
            return self.deserialize_binary_op(ast_node)
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
        elif ast_node["node_type"] == "bool_literal":
            return ast_node["value"]
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
        calle = ast_node["callee"]
        arguments = ""
        for i in range(len(ast_node["arguments"])):
            arguments += self.deserialize_node_type(ast_node["arguments"][i])
            if i != len(ast_node["arguments"]) - 1:
                arguments += ", "
        return f'{calle}({arguments})'