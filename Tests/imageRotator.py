from PIL import Image, ImageTk
import tkinter as tk


class ImageRotatorWithAABB:
    def __init__(self, canvas, image_path, top_left):
        self.canvas = canvas
        self.image_path = image_path
        self.top_left = top_left  # Top-left coordinates determine the position
        self.angle = 0

        # Load the image
        original_image = Image.open(image_path)
        self.original_image = original_image.resize((256, 256))
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


def rotate_image():
    rotator.rotate(10)


# Tkinter setup
root = tk.Tk()
root.title("Image Rotator with Fixed Top-Left Position")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Path to your image
image_path = "data/assets/circle.jpg"  # Replace with your image path
rotator = ImageRotatorWithAABB(canvas, image_path=image_path, top_left=(300, 300))

rotate_button = tk.Button(root, text="Rotate", command=rotate_image)
rotate_button.pack()

root.mainloop()
