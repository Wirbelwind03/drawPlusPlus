import re  # Pour gérer les expressions complexes et les tokens

class DrawScriptParser:
    def __init__(self, canvas):
        self.canvas = canvas
        self.variables = {}  # Stockage des variables
        self.functions = {}  # Stockage des fonctions
        self.cursors = {}    # Stockage des curseurs

    def parse_instruction(self, instruction, line_number):
        instruction = instruction.strip()
        if not instruction or instruction.startswith("//"):
            return  # Ignorer les lignes vides ou les commentaires
        
        if instruction.startswith("var "):
            self.handle_variable_declaration(instruction, line_number)
        elif "=" in instruction:
            self.handle_assignment(instruction, line_number)
        elif instruction.startswith("function"):
            self.handle_function_definition(instruction, line_number)
        elif instruction.startswith("if"):
            self.handle_if_statement(instruction, line_number)
        elif instruction.startswith("while"):
            self.handle_while_loop(instruction, line_number)
        elif instruction.startswith("cursor"):
            self.handle_cursor_statement(instruction, line_number)
        elif instruction.startswith("animate"):
            self.handle_animation(instruction, line_number)
        elif instruction.startswith("copy"):
            self.handle_copy_paste(instruction, line_number)
        elif instruction.startswith("DRAW") or instruction.startswith("MOVE"):
            self.handle_draw_or_move(instruction, line_number)
        else:
            raise ValueError(f"Ligne {line_number}\n La commande '{instruction}' n'existe pas")

    def handle_variable_declaration(self, instruction, line_number):
        match = re.match(r"var (\w+)(?: = (.+))?;", instruction)
        if not match:
            raise ValueError(f"Ligne {line_number}: Syntaxe incorrecte pour la déclaration de variable.")
        
        var_name = match.group(1)
        value = self.evaluate_expression(match.group(2)) if match.group(2) else None
        self.variables[var_name] = value

    def handle_assignment(self, instruction, line_number):
        match = re.match(r"(\w+) = (.+);", instruction)
        if not match:
            raise ValueError(f"Ligne {line_number}: Syntaxe incorrecte pour l'affectation.")
        
        var_name = match.group(1)
        value = self.evaluate_expression(match.group(2))
        if var_name not in self.variables:
            raise ValueError(f"Ligne {line_number}: La variable '{var_name}' n'a pas été déclarée.")
        self.variables[var_name] = value

    def handle_function_definition(self, instruction, line_number):
        raise NotImplementedError("La gestion des fonctions n'est pas encore implémentée.")

    def handle_if_statement(self, instruction, line_number):
        condition = instruction[instruction.index("(") + 1:instruction.index(")")]
        condition_result = self.evaluate_expression(condition)

        if condition_result:
            # Gérer les instructions dans le bloc de condition
            pass
        else:
            # Gérer les instructions dans le bloc "else" si présent
            pass

    def handle_while_loop(self, instruction, line_number):
        raise NotImplementedError("La gestion des boucles while n'est pas encore implémentée.")

    def handle_cursor_statement(self, instruction, line_number):
        match = re.match(r"cursor\(([^,]+),\s*([^\)]+)\);", instruction)
        if not match:
            raise ValueError(f"Ligne {line_number}: Syntaxe incorrecte pour cursor.")
        
        cursor_name = match.group(1).strip()
        x, y = map(int, match.group(2).split(","))
        self.cursors[cursor_name] = (x, y)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline='black', fill='black')

    def handle_animation(self, instruction, line_number):
        raise NotImplementedError("La gestion des animations n'est pas encore implémentée.")

    def handle_copy_paste(self, instruction, line_number):
        match = re.match(r"copy\((.+)\)\s*to\s*\((.+)\);", instruction)
        if not match:
            raise ValueError(f"Ligne {line_number}: Syntaxe incorrecte pour copy-paste.")
        # Exemple de copie de contenu d'un endroit à un autre
        pass

    def handle_draw_or_move(self, instruction, line_number):
        tokens = instruction.split()
        if tokens[0] == "MOVE":
            if len(tokens) != 4:
                raise ValueError(f"Ligne {line_number}: MOVE mauvais format.")
            cursor_name = tokens[1]
            distance = int(tokens[3])
            cursor_data = self.cursors.get(cursor_name)

            if cursor_data:
                current_x, current_y = cursor_data[0], cursor_data[1]
                new_x = current_x + distance
                self.cursors[cursor_name] = (new_x, current_y)

                # Dessiner le curseur après le mouvement
                self.canvas.create_oval(new_x - 5, current_y - 5, new_x + 5, current_y + 5, outline='black', fill='black')

        elif tokens[0] == "DRAW":
            if len(tokens) != 5:
                raise ValueError(f"Ligne {line_number}: DRAW mauvais format.")
            cursor_name = tokens[1]
            shape = tokens[3]
            cursor_data = self.cursors.get(cursor_name)

            if cursor_data:
                x, y = cursor_data[0], cursor_data[1]
                if shape == "CIRCLE":
                    radius = int(tokens[4])
                    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='black')

    def evaluate_expression(self, expr):
        try:
            return eval(expr, {}, self.variables)
        except Exception as e:
            raise ValueError(f"Erreur dans l'évaluation de l'expression: {expr}")
