import turtle

class Cursor:

    def __init__(self, x = 0, y = 0) -> None:
        turtle.setpos(x, y)

    def setPos(self, x, y):
        turtle.setpos(x, y)

    def setThickness(self, thickness):
        turtle.width(thickness)