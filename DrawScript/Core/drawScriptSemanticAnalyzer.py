from DrawScript.Core.globals import GLOBAL_SYMBOLS_FUNCTIONS, GLOBAL_SYMBOLS_CURSOR_FUNCTIONS

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def analyze(self, ast_nodes):
        for node in ast_nodes:
            self.analyze_statement(node)
        return self.errors

    def analyze_statement(self, node):
        node_type = node["node_type"]
        if node_type == "var_declaration":
            self.analyze_var_declaration(node)
        elif node_type == "cursor_declaration":
            self.analyze_cursor_declaration(node)
        elif node_type == "if_statement":
            self.analyze_if_statement(node)
        elif node_type == "for_statement":
            self.analyze_for_statement(node)
        elif node_type == "while_statement":
            self.analyze_while_statement(node)
        elif node_type == "function_declaration":
            self.analyze_function_declaration(node)
        elif node_type == "return_statement":
            self.analyze_return_statement(node)
        elif node_type == "copy_statement":
            self.analyze_copy_statement(node)
        elif node_type == "animate_statement":
            self.analyze_animate_statement(node)
        elif node_type == "cursor_method":
            self.analyze_cursor_method(node)
        elif node_type == "empty_statement":
            pass
        elif node_type == "expression_statement":
            self.analyze_expression_statement(node)
        elif node_type == "var_declaration_no_semi":
            self.analyze_var_declaration(node)
        else:
            self.errors.append(f"Statement inconnu : {node_type}")

    def analyze_var_declaration(self, node):
        var_name = node["name"]
        if var_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Variable '{var_name}' déjà déclarée."
            )
        else:
            # Ex. on enregistre 'number' par défaut
            self.symbols[var_name] = "number"

    def analyze_cursor_declaration(self, node):
        cursor_name = node["name"]
        if cursor_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Cursor '{cursor_name}' déjà déclaré."
            )
        else:
            self.symbols[cursor_name] = "cursor"

    def analyze_cursor_method(self, node):
        cursor_name = node["cursor_name"]
        if cursor_name not in self.symbols:
            self.errors.append(f"Ligne {node['line']}: Variable '{cursor_name}' non déclarée.")
            return
        if self.symbols[cursor_name] != "cursor":
            self.errors.append(f"Ligne {node['line']}: '{cursor_name}' n'est pas un curseur.")
            return

        method = node["method"]
        args = node["arguments"]

        # Vérifie que la méthode appelée fait partie des méthodes valides
        if method not in GLOBAL_SYMBOLS_CURSOR_FUNCTIONS:
            self.errors.append(
                f"Ligne {node['line']}: Méthode '{method}' inconnue pour un curseur."
            )
            return

        # Vérifie que le nombre d’arguments correspond
        expected_args = GLOBAL_SYMBOLS_CURSOR_FUNCTIONS[method]
        if len(args) != expected_args:
            self.errors.append(
                f"Ligne {node['line']}: La méthode '{method}' attend {expected_args} argument(s), reçu {len(args)}."
            )


    # -- ICI on remet les méthodes d'analyse au même niveau que les autres --
    def analyze_if_statement(self, node):
        self.analyze_expression(node["condition"])
        self.analyze_block(node["then_block"])
        if node["else_block"] is not None:
            self.analyze_block(node["else_block"])

    def analyze_block(self, block_node):
        for stmt in block_node["statements"]:
            self.analyze_statement(stmt)

    def analyze_expression_statement(self, node):
        self.analyze_expression(node["expression"])

    def analyze_expression(self, expr):
        node_type = expr["node_type"]
        if node_type == "binary_op":
            self.analyze_expression(expr["left"])
            self.analyze_expression(expr["right"])
        elif node_type == "unary_op":
            self.analyze_expression(expr["expr"])
        elif node_type == "identifier":
            if expr["value"] not in self.symbols:
                self.errors.append("Variable non déclarée: " + expr["value"])
        elif node_type in ("number", "string", "bool_literal"):
            pass
        elif node_type == "call_expr":

            if expr["callee"] in GLOBAL_SYMBOLS_FUNCTIONS:
                # Vérifie que le nombre d’arguments correspond
                expected_args = GLOBAL_SYMBOLS_FUNCTIONS[expr["callee"]]
                if len(expr["arguments"]) != expected_args:
                    self.errors.append(f"La méthode '{expr['callee']}' attend {expected_args} argument(s), reçu {len(expr['arguments'])}.")

            # Gérer la sémantique d’un appel de fonction si besoin
            for arg in expr["arguments"]:
                self.analyze_expression(arg)
        # etc.

    def analyze_for_statement(self, node):
        init_node = node["init"]
        if init_node is not None:
            self.analyze_statement(init_node)

        condition_node = node["condition"]
        if condition_node is not None:
            self.analyze_expression(condition_node)

        increment_node = node["increment"]
        if increment_node is not None:
            self.analyze_expression(increment_node)

        body_node = node["body"]
        self.analyze_block(body_node)

    def analyze_while_statement(self, node):
        condition_node = node["condition"]
        if condition_node is not None:
            self.analyze_expression(condition_node)

        body_node = node["body"]
        self.analyze_block(body_node)

    def analyze_function_declaration(self, node):
        func_name = node["name"]
        if func_name in self.symbols:
            self.errors.append(
                f"Ligne {node['line']}: Fonction '{func_name}' déjà déclarée."
            )
        else:
            self.symbols[func_name] = "function"

        # Analyser le corps de la fonction
        body_block = node["body"]
        self.analyze_block(body_block)

    def analyze_return_statement(self, node):
        if node["expression"] is not None:
            self.analyze_expression(node["expression"])

    def analyze_copy_statement(self, node):
        for expr in node["source"]:
            self.analyze_expression(expr)
        for expr in node["destination"]:
            self.analyze_expression(expr)

    def analyze_animate_statement(self, node):
        self.analyze_expression(node["obj_or_expr1"])
        self.analyze_expression(node["expr2"])
        self.analyze_block(node["body"])