from Controller.Commands.baseCommand import BaseCommand

class CursorCommand(BaseCommand):

    def __init__(self) -> None:
        self.cursorName = None
        self.x, self.y = 0, 0
        self.visible = ""

    def prepare(self, tokens, line_number):
        if len(tokens) != 6:
            raise ValueError("Instruction CURSOR incomplète à la ligne {}".format(line_number))
        self.cursorName = tokens[1]
        self.x, self.y = int(tokens[3]), int(tokens[4])
        self.visible = tokens[5].upper()

    def execute(self, cursors, canvas):
        # Stockez le curseur
        cursors[self.cursorName] = (self.x, self.y, self.visible)

        # Affichage du curseur sur le canvas
        if self.visible:
            canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, outline='black', fill='black')  # Exemple de curseur