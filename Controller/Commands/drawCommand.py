from Controller.Commands.baseCommand import BaseCommand

class DrawCommand(BaseCommand):

    def __init__(self) -> None:
        self.cursor_name = None
        self.shape = ""
        self.radius = 0

    def prepare(self, tokens, line_number):
        if len(tokens) != 5:
            raise ValueError("Instruction DRAW mauvais format à la ligne {}".format(line_number))
        self.cursor_name = tokens[1]
        self.shape = tokens[3]
        self.radius = int(tokens[4])

    def execute(self, cursors, canvas):
        cursor_data = cursors.get(self.cursor_name)

        if cursor_data:
            x, y = cursor_data[0], cursor_data[1]
            if self.shape == "CIRCLE":
                canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, outline='black')  # Dessine un cercle
