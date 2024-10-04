from Controller.Commands.baseCommand import BaseCommand

class MoveCommand(BaseCommand):

    def __init__(self) -> None:
        self.cursorName = None
        self.distance = 0

    def prepare(self, tokens, line_number):
        if len(tokens) != 4:
            raise ValueError("Instruction MOVE mauvais format à la ligne {}".format(line_number))
        self.cursorName = tokens[1]
        self.distance = int(tokens[3])

    def execute(self, cursors, canvas):
        cursor_data = cursors.get(self.cursorName)

        if cursor_data:
            current_x, current_y = cursor_data[0], cursor_data[1]
            new_x = current_x + self.distance
            self.cursors[self.cursorName] = (new_x, current_y, cursor_data[2])  # Mettre à jour la position

            # Dessiner le curseur après le mouvement
            visible = cursor_data[2]
            if visible:
                canvas.create_oval(new_x - 5, current_y - 5, new_x + 5, current_y + 5, outline='black', fill='black')