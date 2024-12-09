import tkinter as tk

class RectangleDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Drawer")
        
        # Canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # State variables
        self.start_x = None
        self.start_y = None
        self.current_rectangle = None
        self.text_ids = []  # To track debug text objects
        
        # Bind events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.update_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)

    def start_drawing(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="blue"
        )

    def update_rectangle(self, event):
        if self.current_rectangle:
            # Update rectangle dimensions
            self.canvas.coords(self.current_rectangle, self.start_x, self.start_y, event.x, event.y)
            self.update_debug_info(event.x, event.y)

    def finish_drawing(self, event):
        self.update_debug_info(event.x, event.y)

    def update_debug_info(self, end_x, end_y):
        # Clear previous debug text
        for text_id in self.text_ids:
            self.canvas.delete(text_id)
        self.text_ids.clear()
        
        # Get coordinates and dimensions
        x1, y1 = self.start_x, self.start_y
        x2, y2 = end_x, end_y
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        width = x_max - x_min
        height = y_max - y_min
        
        # Add debug information
        self.text_ids.append(self.canvas.create_text(x_min, y_min - 10, text=f"({x_min}, {y_min})", fill="red"))
        self.text_ids.append(self.canvas.create_text(x_max, y_min - 10, text=f"({x_max}, {y_min})", fill="red"))
        self.text_ids.append(self.canvas.create_text(x_min, y_max + 10, text=f"({x_min}, {y_max})", fill="red"))
        self.text_ids.append(self.canvas.create_text(x_max, y_max + 10, text=f"({x_max}, {y_max})", fill="red"))
        
        self.text_ids.append(self.canvas.create_text((x_min + x_max) / 2, y_min - 10, text=f"Width: {width}", fill="green"))
        self.text_ids.append(self.canvas.create_text(x_max + 30, (y_min + y_max) / 2, text=f"Height: {height}", fill="green"))

if __name__ == "__main__":
    root = tk.Tk()
    app = RectangleDrawer(root)
    root.mainloop()
