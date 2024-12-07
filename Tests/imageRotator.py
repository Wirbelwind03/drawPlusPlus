from PIL import Image, ImageTk
import tkinter as tk


class ImageRotatorWithAABB:
    def __init__(self, canvas, image_path, center):
        self.canvas = canvas
        self.image_path = image_path
        self.center = center  # Center point stays fixed
        self.angle = 0

        # Load the image
        self.original_image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.width, self.height = self.original_image.size

        # Calculate initial top-left position for NW anchor
        self.top_left = (center[0] - self.width // 2, center[1] - self.height // 2)

        # Place the image on the canvas
        self.image_on_canvas = self.canvas.create_image(
            self.top_left[0], self.top_left[1], image=self.tk_image, anchor="nw"
        )

        # Draw the initial AABB
        x1, y1 = self.top_left
        x2, y2 = x1 + self.width, y1 + self.height
        self.aabb = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def rotate(self, delta_angle):
        self.angle = (self.angle + delta_angle) % 360

        # Rotate the image
        rotated_image = self.original_image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)
        new_width, new_height = rotated_image.size

        # Recalculate top-left position to keep the center fixed
        cx, cy = self.center
        self.top_left = (cx - new_width // 2, cy - new_height // 2)

        # Update the image position
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
        self.canvas.coords(
            self.image_on_canvas, self.top_left[0], self.top_left[1]
        )

        # Update the AABB
        x1, y1 = self.top_left
        x2, y2 = x1 + new_width, y1 + new_height
        self.canvas.coords(self.aabb, x1, y1, x2, y2)


def rotate_image():
    rotator.rotate(10)


# Tkinter setup
root = tk.Tk()
root.title("Image Rotator with Centered Axis")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Path to your image
image_path = "data/assets/pencil.png"  # Replace with your image path
rotator = ImageRotatorWithAABB(canvas, image_path=image_path, center=(300, 300))

rotate_button = tk.Button(root, text="Rotate", command=rotate_image)
rotate_button.pack()

root.mainloop()

