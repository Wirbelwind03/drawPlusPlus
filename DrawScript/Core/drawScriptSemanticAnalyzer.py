from DrawScript.Core.globals import GLOBAL_SYMBOLS_FUNCTIONS, GLOBAL_SYMBOLS_CURSOR_FUNCTIONS, GLOBAL_SYMBOLS_VARIABLES

class SemanticAnalyzer:
    def __init__(self):
        # Dictionary to store symbols (variables, functions, cursors) found during semantic analysis
        self.symbols = {}
        # List to store any semantic errors found
        self.errors = []

    def analyze(self, ast_nodes):
        """
        Analyzes a list of AST (Abstract Syntax Tree) nodes to perform semantic checks.
        Returns a list of semantic errors found.
        """
        for node in ast_nodes:
            self.analyze_statement(node)
        return self.errors

    def analyze_statement(self, node):
        """
        Dispatch method to analyze a statement based on its 'node_type'.
        """
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
        elif node_type == "do_while_statement":
            self.analyze_do_while_statement(node)
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
            # No operation needed for empty statements
            pass
        elif node_type == "expression_statement":
            self.analyze_expression_statement(node)
        elif node_type == "var_declaration_no_semi":
            # Treat this as a variable declaration but missing a semicolon
            self.analyze_var_declaration(node)
        else:
            self.errors.append(f"Unknown statement: {node_type}")

    def analyze_var_declaration(self, node):
        """
        Analyzes a variable declaration.
        Checks if the variable was already declared, and if not, records its type.
        """
        var_name = node["name"]
        if var_name in self.symbols:
            self.errors.append(
                f"Line {node['line']}: Variable '{var_name}' already declared."
            )
        else:
            # Example: store 'number' by default
            # In a more advanced analyzer, we'd use the type from the AST or symbol table
            self.symbols[var_name] = "number"

    def analyze_cursor_declaration(self, node):
        """
        Analyzes a cursor declaration.
        Checks if the cursor was already declared, and if not, records it.
        """
        cursor_name = node["name"]
        if cursor_name in self.symbols:
            self.errors.append(
                f"Line {node['line']}: Cursor '{cursor_name}' already declared."
            )
        else:
            self.symbols[cursor_name] = "cursor"

    def analyze_cursor_method(self, node):
        """
        Analyzes a method call on a cursor variable.
        Checks if the cursor is declared, if it's actually of type 'cursor',
        and if the method with the right number of arguments exists.
        """
        cursor_name = node["cursor_name"]
        if cursor_name not in self.symbols:
            self.errors.append(f"Line {node['line']}: Variable '{cursor_name}' not declared.")
            return
        if self.symbols[cursor_name] != "cursor":
            self.errors.append(f"Line {node['line']}: '{cursor_name}' is not a cursor.")
            return

        method = node["method"]
        args = node["arguments"]

        # Check if the called method is in the valid cursor methods
        if method not in GLOBAL_SYMBOLS_CURSOR_FUNCTIONS:
            self.errors.append(
                f"Line {node['line']}: Unknown method '{method}' for a cursor."
            )
            return

        # Check that the number of arguments matches
        expected_args = GLOBAL_SYMBOLS_CURSOR_FUNCTIONS[method]
        if len(args) != expected_args:
            self.errors.append(
                f"Line {node['line']}: Method '{method}' expects {expected_args} argument(s), received {len(args)}."
            )

    def analyze_if_statement(self, node):
        """
        Analyzes an if statement:
        1) Checks the condition expression.
        2) Analyzes the 'then' block.
        3) If present, analyzes the 'else' block.
        """
        self.analyze_expression(node["condition"])
        self.analyze_block(node["then_block"])
        if node["else_block"] is not None:
            self.analyze_block(node["else_block"])

    def analyze_block(self, block_node):
        """
        Analyzes a block, which is a list of statements.
        """
        for stmt in block_node["statements"]:
            self.analyze_statement(stmt)

    def analyze_expression_statement(self, node):
        """
        Analyzes an expression statement (a standalone expression used as a statement).
        """
        self.analyze_expression(node["expression"])

    def analyze_expression(self, expr):
        """
        Analyzes an expression of various possible types, such as binary operations,
        unary operations, function calls, or identifiers.
        """
        node_type = expr["node_type"]
        if node_type == "binary_op":
            self.analyze_expression(expr["left"])
            self.analyze_expression(expr["right"])
        elif node_type == "unary_op":
            self.analyze_expression(expr["expr"])
        elif node_type == "identifier":
            # Check if the identifier is declared either in the local symbols
            # or in the global list of variables
            if expr["value"] not in self.symbols and expr["value"] not in GLOBAL_SYMBOLS_VARIABLES:
                self.errors.append("Undeclared variable: " + expr["value"])
        elif node_type in ("number", "string", "bool_literal"):
            # These literals are always valid as expressions
            pass
        elif node_type == "call_expr":
            # Check if the function (callee) is known, then verify argument count
            if expr["callee"] in GLOBAL_SYMBOLS_FUNCTIONS:
                expected_args = GLOBAL_SYMBOLS_FUNCTIONS[expr["callee"]]
                if len(expr["arguments"]) != expected_args:
                    self.errors.append(
                        f"Function '{expr['callee']}' expects {expected_args} argument(s), received {len(expr['arguments'])}."
                    )
            # Analyze each argument in the function call
            for arg in expr["arguments"]:
                self.analyze_expression(arg)
        # In a more complete analyzer, more cases might be handled here

    def analyze_for_statement(self, node):
        """
        Analyzes a for-loop statement.
        1) Analyzes the init statement if present.
        2) Analyzes the condition expression if present.
        3) Analyzes the increment expression if present.
        4) Analyzes the body of the loop.
        """
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
        """
        Analyzes a while-loop statement.
        1) Analyzes the condition expression if present.
        2) Analyzes the body of the loop.
        """
        condition_node = node["condition"]
        if condition_node is not None:
            self.analyze_expression(condition_node)

        body_node = node["body"]
        self.analyze_block(body_node)

    def analyze_do_while_statement(self, node):
        """
        Analyzes a do-while-loop statement.
        Note that the body is analyzed before the condition.
        """
        self.analyze_block(node["body"])
        self.analyze_expression(node["condition"])

    def analyze_function_declaration(self, node):
        """
        Analyzes a function declaration.
        Checks if the function name was already declared, and if not, records it.
        Then analyzes the function body.
        """
        func_name = node["name"]
        if func_name in self.symbols:
            self.errors.append(
                f"Line {node['line']}: Function '{func_name}' already declared."
            )
        else:
            self.symbols[func_name] = "function"

        # Analyze the body of the function
        body_block = node["body"]
        self.analyze_block(body_block)

    def analyze_return_statement(self, node):
        """
        Analyzes a return statement by analyzing the returned expression if present.
        """
        if node["expression"] is not None:
            self.analyze_expression(node["expression"])

    def analyze_copy_statement(self, node):
        """
        Analyzes a copy statement, which has source and destination expressions.
        """
        for expr in node["source"]:
            self.analyze_expression(expr)
        for expr in node["destination"]:
            self.analyze_expression(expr)

    def analyze_animate_statement(self, node):
        """
        Analyzes an animate statement, which includes expressions and a body block
        to be semantically checked.
        """
        self.analyze_expression(node["obj_or_expr1"])
        self.analyze_expression(node["expr2"])
        self.analyze_block(node["body"])
