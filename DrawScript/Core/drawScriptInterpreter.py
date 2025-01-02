class DrawScriptInterpreter:
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
            if ast_node["node_type"] == "var_declaration":
                #deserialize += "\t"
                #deserialize += self.deserialize_var_declaration(ast_node)
                #deserialize += ";\n"
                pass
            elif ast_node["node_type"] == "function_declaration":
                #self.deserialize_function_declaration(ast_node)
                pass
            elif ast_node["node_type"] == "for_statement":
                deserialize += "\t"
                deserialize += self.deserialize_for_statement(ast_node)
                pass
            else:
                print(ast_node["node_type"])
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
        deserialize = "for (int "
        deserialize += self.deserialize_var_declaration(ast_node["init"])
        deserialize += "; "
        deserialize += self.deserialize_binary_op(ast_node["condition"])
        deserialize += "; "
        deserialize += self.deserialize_binary_op(ast_node["increment"])
        deserialize += ")\n"
        deserialize += self.deserialize_body(ast_node["body"])
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
    
    def deserialize_node_type(self, ast_node):
        deserialize = ""
        if ast_node["node_type"] == "binary_op":
            deserialize += self.deserialize_binary_op(ast_node)
        elif ast_node["node_type"] == "call_expr":
            pass
        elif ast_node["node_type"] == "identifier":
            deserialize += ast_node["value"]
        elif ast_node["node_type"] == "number":
            deserialize += str(ast_node["value"])
        elif ast_node["node_type"] == "var_declaration":
            deserialize += "\t"
            deserialize += self.deserialize_var_declaration(ast_node)
            deserialize += ";\n"
        else:
            print(ast_node)
        return deserialize
        
    def deserialize_body(self, ast_node):
        deserialize = "{\n"
        for statement in ast_node["statements"]:
            deserialize += self.deserialize_node_type(statement)
        deserialize += "}\n"
        return deserialize