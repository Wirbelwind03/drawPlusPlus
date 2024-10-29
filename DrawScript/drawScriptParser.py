# Classe du compilateur
class DrawScriptParser:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cursors = {}  # Dictionnaire pour stocker les curseurs

    def parse_instruction(self, instruction, line_number):
        tokens = instruction.split()
        if not tokens:
            return
        command = tokens[0]

        try:
            if command == "CURSOR":
                if len(tokens) != 6:
                    raise ValueError("Instruction CURSOR incomplète à la ligne {}".format(line_number))
                cursor_name = tokens[1]
                x, y = int(tokens[3]), int(tokens[4])
                visible = tokens[5].upper() == "VISIBLE"

                # Stockez le curseur
                self.cursors[cursor_name] = (x, y, visible)

                # Affichage du curseur sur le canvas
                if visible:
                    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline='black', fill='black')  # Exemple de curseur

            elif command == "MOVE":
                if len(tokens) != 4:
                    raise ValueError("Instruction MOVE mauvais format à la ligne {}".format(line_number))
                cursor_name = tokens[1]
                distance = int(tokens[3])
                cursor_data = self.cursors.get(cursor_name)

                if cursor_data:
                    current_x, current_y = cursor_data[0], cursor_data[1]
                    new_x = current_x + distance
                    self.cursors[cursor_name] = (new_x, current_y, cursor_data[2])  # Mettre à jour la position

                    # Dessiner le curseur après le mouvement
                    visible = cursor_data[2]
                    if visible:
                        self.canvas.create_oval(new_x - 5, current_y - 5, new_x + 5, current_y + 5, outline='black', fill='black')

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
                        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='black')  # Dessine un cercle

        except Exception as e:
            raise ValueError(f"Erreur dans l'instruction '{instruction}' à la ligne {line_number}: {str(e)}")