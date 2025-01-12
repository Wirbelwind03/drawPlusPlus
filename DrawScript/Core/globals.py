GLOBAL_SYMBOLS_FUNCTIONS = {
    "setRGBA": 4,  #(r, g, b, a)
    "drawCircle": 3,    #(x, y, radius)
    "drawFilledCircle": 3,    #(x, y, radius)
    "drawEllipse": 4,   #(x, y, rx, ry)
    "drawFilledEllipse": 4,   #(x, y, rx, ry)
    "drawRoundedRectangle": 5,   #(x, y, width, height, radius)
    "drawBox": 4,       #(x, y, width, height)
    "drawRoundedBox": 5,       #(x, y, width, height, radius)
    "drawSegment": 4,   #(x0, y0, x1, y1)
    "drawTriangle": 6,  #(x0, y0, x1, y1, x2, y2)
    "drawRectangle": 4, #(x, y, width, height)
    "drawPoint": 2,     #(x, y)
}

# Methods to draw with the cursor
GLOBAL_SYMBOLS_CURSOR_FUNCTIONS = {
    "move": 2,           # (x, y)"
    "rotate": 1,         # (degrees)
    "drawCircle": 1,     # (radius)
    "drawFilledCircle": 1,    #(radius)
    "drawEllipse": 2,   #(rx, ry)
    "drawFilledEllipse": 2,   #(rx, ry)
    "drawRoundedRectangle": 3,   #(width, height, radius)
    "drawBox": 2,       #(width, height)
    "drawRoundedBox": 3,       #(width, height, radius)
    "drawSegment": 1,    # (length)
    "drawTriangle": 4,   # (x0, y0, x1, y1)
    "drawRectangle": 2,  # (width, height)
    "drawPoint": 0,      # ()
    "setRGBA": 4,       #  
    "setThickness": 1    # 
}

GLOBAL_SYMBOLS_VARIABLES = {
    "CANVAS_WIDTH" : "SCREEN_WIDTH",
    "CANVAS_HEIGHT" : "SCREEN_HEIGHT"
}