GLOBAL_SYMBOLS_FUNCTIONS = {
    "setColorRGB": 3,   #setColorRGB(r, g, b)
    "setColorRGBA": 4,  #setColorRGBA(r, g, b, a)
    "drawCircle": 3,    #drawCircle(x, y, radius)
    "drawSegment": 4,   #drawSegment(x0, y0, x1, y1)
    "drawRectangle": 4, #drawRectangle(x, y, width, height)
    "drawPoint": 2,     #drawPoint(x, y)
}

# Methods to draw with the cursor
GLOBAL_SYMBOLS_CURSOR_FUNCTIONS = {
    "move": 2,           # move(x, y)"
    "rotate": 1,         # rotate(degrees)
    "drawCircle": 1,     # drawCircle(radius)
    "drawSegment": 1,    # drawSegment(length)
    "drawRectangle": 2,  # drawRectangle(width, height)
    "drawPoint": 0,      # drawPoint()
    "setColor": 1,       # Nouvelle méthode
    "setThickness": 1    # Nouvelle méthode
}

GLOBAL_SYMBOLS_VARIABLES = {
    "CANVAS_WIDTH" : "SCREEN_WIDTH",
    "CANVAS_HEIGHT" : "SCREEN_HEIGHT"
}