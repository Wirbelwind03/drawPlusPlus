from PIL import Image, ImageTk
import tkinter as tk


class ImageRotatorWithAABB:
    def __init__(self, canvas, image_path, top_left):
        self.canvas = canvas
        self.image_path = image_path
        self.top_left = top_left  # Top-left coordinates determine the position
        self.angle = 0

        # Load the image
        self.original_image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.width, self.height = self.original_image.size

        # Calculate initial center based on the top-left position
        self.center = (top_left[0] + self.width // 2, top_left[1] + self.height // 2)

        # Place the image on the canvas
        self.image_on_canvas = self.canvas.create_image(
            self.top_left[0], self.top_left[1], image=self.tk_image, anchor="nw"
        )

        # Draw the initial AABB
        x1, y1 = self.top_left
        x2, y2 = x1 + self.width, y1 + self.height
        self.aabb = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")

        # Variables to track dragging state
        self.dragging = False
        self.drag_start = (0, 0)

        # Bind mouse events
        self.canvas.tag_bind(self.image_on_canvas, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.image_on_canvas, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.image_on_canvas, "<ButtonRelease-1>", self.stop_drag)

    def rotate(self, delta_angle):
        self.angle = (self.angle + delta_angle) % 360

        # Rotate the image
        rotated_image = self.original_image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)
        new_width, new_height = rotated_image.size

        # Recalculate the new center, keeping the same center position
        cx, cy = self.center

        # Calculate the new top-left position to keep the center fixed
        self.top_left = (cx - new_width // 2, cy - new_height // 2)

        # Update the image position on the canvas
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
        self.canvas.coords(self.image_on_canvas, self.top_left[0], self.top_left[1])

        # Update the AABB
        x1, y1 = self.top_left
        x2, y2 = x1 + new_width, y1 + new_height
        self.canvas.coords(self.aabb, x1, y1, x2, y2)

    def start_drag(self, event):
        self.dragging = True
        self.drag_start = (event.x, event.y)

    def drag(self, event):
        if self.dragging:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]

            # Update the top-left position
            self.top_left = (self.top_left[0] + dx, self.top_left[1] + dy)

            # Update the center position
            self.center = (self.center[0] + dx, self.center[1] + dy)

            # Update image position on the canvas
            self.canvas.coords(self.image_on_canvas, self.top_left[0], self.top_left[1])

            # Update the AABB
            x1, y1 = self.top_left
            x2, y2 = x1 + self.width, y1 + self.height
            self.canvas.coords(self.aabb, x1, y1, x2, y2)

            # Update drag start for the next motion
            self.drag_start = (event.x, event.y)

    def stop_drag(self, event):
        self.dragging = False


# Tkinter setup
root = tk.Tk()
root.title("Image Rotator and Draggable Object")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Path to your image
image_path = "data/assets/circle.jpg"  # Replace with your image path
rotator = ImageRotatorWithAABB(canvas, image_path=image_path, top_left=(100, 100))

# Rotate the image with the left arrow key
def on_key_press(event):
    if event.keysym == "Left":
        rotator.rotate(-10)

root.bind("<Left>", on_key_press)

root.mainloop()
