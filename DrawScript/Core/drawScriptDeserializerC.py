class DrawScriptDeserializerC:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes

    def write_c(self):
        f = open("main.c", "w")
        
        deserialize = ""
        deserialize += "#include <SDL2/SDL.h>\n"
        deserialize += "#include <stdbool.h>\n"
        deserialize += "#include <stdio.h>\n"
        deserialize += "\n"
        deserialize += "int main(int argc, char *argv[]){\n"
        for ast_node in self.ast_nodes:
            deserialize += self.deserialize_node_type(ast_node)
        deserialize += "}\n"

        f.write(deserialize)
        f.close()

    def deserialize_function_declaration(self, ast_node):
        deserialize = f'void {ast_node["name"]}('
        for i in range(len(ast_node["params"])):
            deserialize += f'{ast_node["params"][i]}'
            if i != len(ast_node["params"]) - 1:
                deserialize += ","
        deserialize += "){\n"
        deserialize += "}\n"
        return deserialize

    def deserialize_for_statement(self, ast_node):
        deserialize = "\tfor (int "
        deserialize += self.deserialize_var_declaration(ast_node["init"])
        deserialize += "; "
        deserialize += self.deserialize_binary_op(ast_node["condition"])
        deserialize += "; "
        deserialize += self.deserialize_binary_op(ast_node["increment"])
        deserialize += ")\n"
        deserialize += self.deserialize_block(ast_node["body"])
        return deserialize

    def deserialize_var_declaration(self, ast_node):
        deserialize = ""
        if ast_node["type"] != None:
            deserialize += f'{ast_node["type"]} ' 
        deserialize += f'{ast_node["name"]} = '
        deserialize += self.deserialize_node_type(ast_node["expression"])
        return deserialize
    
    def deserialize_binary_op(self, ast_node):
        deserialize = ""
        deserialize += self.deserialize_node_type(ast_node["left"])
        deserialize += " "
        deserialize += ast_node["op"]
        deserialize += " "
        deserialize += self.deserialize_node_type(ast_node["right"])
        return deserialize
    
    def deserialize_if_statement(self, ast_node):
        deserialize = "\tif "
        deserialize += f'({self.deserialize_node_type(ast_node["condition"])})'
        deserialize += self.deserialize_block(ast_node["then_block"])
        deserialize += "\telse"
        deserialize += self.deserialize_block(ast_node["else_block"])
        return deserialize
    
    def deserialize_while_statement(self, ast_node):
        deserialize = "\twhile "
        deserialize += f'({self.deserialize_node_type(ast_node["condition"])})'
        deserialize += self.deserialize_block(ast_node["body"])
        return deserialize
    
    def deserialize_node_type(self, ast_node):
        deserialize = ""
        if ast_node["node_type"] == "binary_op":
            deserialize += self.deserialize_binary_op(ast_node)
        elif ast_node["node_type"] == "call_expr":
            deserialize += self.deserialize_call_expr(ast_node)
        elif ast_node["node_type"] == "expression_statement":
            deserialize += self.deserialize_expression_statement(ast_node)
        elif ast_node["node_type"] == "identifier":
            deserialize += ast_node["value"]
        elif ast_node["node_type"] == "if_statement":
            deserialize += self.deserialize_if_statement(ast_node)
        elif ast_node["node_type"] == "number":
            deserialize += str(ast_node["value"])
        elif ast_node["node_type"] == "bool_literal":
            deserialize += ast_node["value"]
        elif ast_node["node_type"] == "for_statement":
            deserialize += self.deserialize_for_statement(ast_node)
            pass
        elif ast_node["node_type"] == "function_declaration":
            #self.deserialize_function_declaration(ast_node)
            pass
        elif ast_node["node_type"] == "var_declaration":
            deserialize += "\t"
            deserialize += self.deserialize_var_declaration(ast_node)
            deserialize += ";\n"
        elif ast_node["node_type"] == "while_statement":
            deserialize += self.deserialize_while_statement(ast_node)
        else:
            print(ast_node["node_type"])
        return deserialize
            
    def deserialize_block(self, ast_node):
        deserialize = "\t{\n"
        deserialize += self.deserialize_statements(ast_node)
        deserialize += "\t}\n"
        return deserialize
    
    def deserialize_statements(self, ast_node):
        deserialize = ""
        for statement in ast_node["statements"]:
            deserialize += "\t"
            deserialize += self.deserialize_node_type(statement)
        return deserialize
    
    def deserialize_expression_statement(self, ast_node):
        deserialize = "\t"
        deserialize += self.deserialize_node_type(ast_node["expression"])
        deserialize += ";\n"
        return deserialize
    
    def deserialize_call_expr(self, ast_node):
        deserialize = f'{ast_node["callee"]}('
        for i in range(len(ast_node["arguments"])):
            deserialize += self.deserialize_node_type(ast_node["arguments"][i])
            if i != len(ast_node["arguments"]) - 1:
                deserialize += ", "
        deserialize += ")"
        return deserialize