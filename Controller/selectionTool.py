import tkinter as tk

class SelectionTool:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.width = None
        self.height = None
        self.rect = None
        self.action = "createRectangle"

        # Bind mouse events to canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_mouse_over)

    def on_mouse_over(self, event):
        if self.rect:
            # Check if the cursor is inside the selection rectangle
            if event.x > self.start_x and event.x < self.end_x and event.y > self.start_y and event.y < self.end_y:
                self.action = "moveRectangle"
                self.canvas.config(cursor="fleur")

            else:
                self.action = "createRectangle"
                self.canvas.config(cursor="arrow")

    def on_button_press(self, event):
        if self.action == "moveRectangle":
            # Calculate the offset between mouse click and rectangle's position
            self.gap_offset_x = self.start_x - event.x
            self.gap_offset_y = self.start_y - event.y
            return
        
        if self.rect:
            self.canvas.delete(self.rect)

        # Save the starting point for the rectangle
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # Create a rectangle (but don't specify the end point yet)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        if self.action == "moveRectangle":
            self.start_x = event.x + self.gap_offset_x
            self.start_y = event.y + self.gap_offset_y
            self.canvas.moveto(self.rect, self.start_x, self.start_y)
            return

        # Update the rectangle as the mouse is dragged
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        # Modify the coordinates of the rectangle
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        if self.action == "moveRectangle":
            self.end_x = self.start_x + self.width
            self.end_y = self.start_y + self.height
            return

        # On release, finalize the rectangle selection
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y

        # Final coordinates of the selection area
        selection_box = (self.start_x, self.start_y, self.end_x, self.end_y)
        print(f"Selection area: {selection_box}")