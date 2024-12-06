import tkinter as tk
from PIL import Image, ImageTk

class ImageRotatorWithAABB:
    def __init__(self, canvas, image_path, center):
        self.canvas = canvas
        self.image_path = image_path
        self.center = center
        self.angle = 0

        # Load the image using Pillow
        self.original_image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.width, self.height = self.original_image.size

        # Place the image on the canvas
        cx, cy = center
        self.image_on_canvas = self.canvas.create_image(cx, cy, image=self.tk_image)

        # Draw the AABB (Axis-Aligned Bounding Box)
        self.aabb = self.canvas.create_rectangle(
            cx - self.width // 2, cy - self.height // 2,
            cx + self.width // 2, cy + self.height // 2,
            outline="red"
        )

    def rotate(self, delta_angle):
        self.angle = (self.angle + delta_angle) % 360

        # Rotate the image using Pillow
        rotated_image = self.original_image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated_image)

        # Update the image on the canvas
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

        # Update the AABB
        new_width, new_height = rotated_image.size
        cx, cy = self.center
        self.canvas.coords(
            self.aabb,
            cx - new_width // 2, cy - new_height // 2,
            cx + new_width // 2, cy + new_height // 2
        )


def rotate_image():
    rotator.rotate(10)  # Rotate the image by 10 degrees


# Initialize Tkinter
root = tk.Tk()
root.title("Image Rotator with Axis-Aligned Bounding Box")

# Create a Canvas
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Create an ImageRotatorWithAABB
image_path = "data/assets/pencil.png"  # Replace with the path to your image
rotator = ImageRotatorWithAABB(canvas, image_path=image_path, center=(300, 300))

# Create a Button to rotate the image
rotate_button = tk.Button(root, text="Rotate", command=rotate_image)
rotate_button.pack()

# Run the Tkinter event loop
root.mainloop()
