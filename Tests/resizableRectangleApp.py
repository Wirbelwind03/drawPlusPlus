import tkinter as tk

class ResizableRectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resizable Rectangle")

        # Create a canvas
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        # Create a rectangle
        self.rect = self.canvas.create_rectangle(200, 200, 300, 300, fill="blue")

        # Create handles at each corner
        self.handles = {
            "top_left": self.canvas.create_rectangle(190, 190, 210, 210, fill="red"),
            "top_right": self.canvas.create_rectangle(290, 190, 310, 210, fill="red"),
            "bottom_left": self.canvas.create_rectangle(190, 290, 210, 310, fill="red"),
            "bottom_right": self.canvas.create_rectangle(290, 290, 310, 310, fill="red"),
        }

        # Variables to track resizing
        self.active_handle = None
        self.offset_x = 0
        self.offset_y = 0

        # Bind events for handles
        for handle in self.handles.values():
            self.canvas.tag_bind(handle, "<Button-1>", self.on_handle_click)
            self.canvas.tag_bind(handle, "<B1-Motion>", self.on_handle_drag)

    def on_handle_click(self, event):
        # Determine which handle is clicked and calculate the offset
        self.active_handle = self.canvas.find_closest(event.x, event.y)[0]
        self.offset_x = event.x
        self.offset_y = event.y

    def on_handle_drag(self, event):
        if self.active_handle is None:
            return

        # Get the rectangle's current coordinates
        rect_coords = self.canvas.coords(self.rect)

        # Calculate the new size based on the handle being dragged
        if self.active_handle == self.handles["top_left"]:
            new_coords = [event.x, event.y, rect_coords[2], rect_coords[3]]
        elif self.active_handle == self.handles["top_right"]:
            new_coords = [rect_coords[0], event.y, event.x, rect_coords[3]]
        elif self.active_handle == self.handles["bottom_left"]:
            new_coords = [event.x, rect_coords[1], rect_coords[2], event.y]
        elif self.active_handle == self.handles["bottom_right"]:
            new_coords = [rect_coords[0], rect_coords[1], event.x, event.y]
        else:
            return

        # Update the rectangle's size
        self.canvas.coords(self.rect, *new_coords)

        # Update the handles' positions
        self.update_handles()

    def update_handles(self):
        # Sync handle positions with the rectangle
        rect_coords = self.canvas.coords(self.rect)
        self.canvas.coords(self.handles["top_left"], rect_coords[0] - 10, rect_coords[1] - 10, rect_coords[0] + 10, rect_coords[1] + 10)
        self.canvas.coords(self.handles["top_right"], rect_coords[2] - 10, rect_coords[1] - 10, rect_coords[2] + 10, rect_coords[1] + 10)
        self.canvas.coords(self.handles["bottom_left"], rect_coords[0] - 10, rect_coords[3] - 10, rect_coords[0] + 10, rect_coords[3] + 10)
        self.canvas.coords(self.handles["bottom_right"], rect_coords[2] - 10, rect_coords[3] - 10, rect_coords[2] + 10, rect_coords[3] + 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableRectangleApp(root)
    root.mainloop()
