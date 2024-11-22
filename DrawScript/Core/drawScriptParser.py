# Compiler Class
class DrawScriptParser:
    def __init__(self):
        self.cursors = {}  # Dictionary for storing cursors

    def parse_instruction(self, instruction, line_number):
        tokens = instruction.split()
        if not tokens:
            return
        command = tokens[0]

        if command == "CURSOR":
            if len(tokens) != 6:
                raise ValueError("Instruction CURSOR incomplète à la ligne {}".format(line_number))
            cursor_name = tokens[1]
            x, y = int(tokens[3]), int(tokens[4])
            visible = tokens[5].upper() == "VISIBLE"

            # Store the cursor
            self.cursors[cursor_name] = (x, y, visible)

        elif command == "MOVE":
            if len(tokens) != 4:
                raise ValueError("Instruction MOVE mauvais format à la ligne {}".format(line_number))
            cursor_name = tokens[1]
            distance = int(tokens[3])
            cursor_data = self.cursors.get(cursor_name)

            if cursor_data:
                current_x, current_y = cursor_data[0], cursor_data[1]
                new_x = current_x + distance
                self.cursors[cursor_name] = (new_x, current_y, cursor_data[2])  # Update position

                # Draw cursor after movement
                visible = cursor_data[2]

        elif command == "DRAW":
            if len(tokens) != 5:
                raise ValueError("Instruction DRAW mauvais format à la ligne {}".format(line_number))
            cursor_name = tokens[1]
            shape = tokens[3]
            cursor_data = self.cursors.get(cursor_name)

            if cursor_data:
                x, y = cursor_data[0], cursor_data[1]
                if shape == "CIRCLE":
                    radius = int(tokens[4])

        else:
            raise ValueError(f"Ligne {line_number}\n La commande {command} n'existe pas")
