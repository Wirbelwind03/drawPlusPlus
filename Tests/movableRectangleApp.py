import tkinter as tk

class MovableRectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movable Rectangle")
        
        # Create a canvas
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()
        
        # Create a rectangle
        self.rect = self.canvas.create_rectangle(200, 200, 300, 300, fill="blue")
        
        # Variables to track the offset
        self.offset_x = 0
        self.offset_y = 0
        
        # Bind events
        self.canvas.tag_bind(self.rect, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)

    def on_click(self, event):
        # Calculate the offset of the click within the rectangle
        rect_coords = self.canvas.coords(self.rect)
        self.offset_x = event.x - rect_coords[0]
        self.offset_y = event.y - rect_coords[1]

    def on_drag(self, event):
        # Move the rectangle to follow the cursor
        x = event.x - self.offset_x
        y = event.y - self.offset_y
        self.canvas.coords(self.rect, x, y, x + 100, y + 100)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovableRectangleApp(root)
    root.mainloop()
