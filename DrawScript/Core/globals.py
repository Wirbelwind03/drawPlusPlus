GLOBAL_SYMBOLS_FUNCTIONS = {
    "setColorRGB": 3,   #setColorRGB(r, g, b)
    "setColorRGBA": 4,  #setColorRGBA(r, g, b, a)
    "drawCircle": 3,    #drawCircle(x, y, radius)
    "drawSegment": 4,   #drawSegment(x0, y0, x1, y1)
    "drawSquare": 2,    #drawSquare(x, y, width, height)
    "drawPoint": 2,     #drawPoint(x, y)
}

GLOBAL_SYMBOLS_CURSOR_FUNCTIONS = {
    "move": 2,           # Remplacement de "moveTo" par "move(xOuY, pixels)"
    "rotate": 1,         # rotate(degrees)
    "drawCircle": 1,     # drawCircle(radius)
    "drawSegment": 2,    # drawSegment(x1, y1)
    "drawSquare": 2,     # drawSquare(width, height)
    "drawPoint": 0,      # drawPoint()
    "setColor": 1,       # Nouvelle méthode
    "setThickness": 1    # Nouvelle méthode
}

GLOBAL_SYMBOLS_VARIABLES = {
    "CANVAS_WIDTH" : "SCREEN_WIDTH",
    "CANVAS_HEIGHT" : "SCREEN_HEIGHT"
}