class DrawScriptInterpreter:
    def __init__(self, ast_nodes):
        self.ast_nodes = ast_nodes

    def write_c(self):
        f = open("main.c", "w")
        f.write("#include <SDL2/SDL.h>\n")
        f.write("int main(int argc, char *argv[]){\n")
        for ast_node in self.ast_nodes:
            if ast_node["node_type"] == "var_declaration":
                self.write_var_declaration(f, ast_node)
        f.write("}")
        f.close()

    def write_var_declaration(self, file, ast_node):
        string = "\t"
        if ast_node["type"] != None:
            string += f'{ast_node["type"]} ' 
        string += f'{ast_node["name"]} = {ast_node["expression"]["value"]};\n'
        file.write(string)