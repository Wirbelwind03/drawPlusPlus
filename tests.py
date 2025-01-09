import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Rotate and Resize")

        # Load the image
        self.original_image = Image.open("Data/assets/gear.png")
        self.display_image = self.original_image.copy()
        self.photo_image = ImageTk.PhotoImage(self.display_image)

        # Canvas to display the image
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.image_on_canvas = self.canvas.create_image(250, 250, image=self.photo_image)
        self.bounding_box = None

        # Rotate input
        rotate_label = ttk.Label(root, text="Rotate (degrees):")
        rotate_label.pack(pady=5)
        self.rotate_var = tk.DoubleVar()
        rotate_entry = ttk.Entry(root, textvariable=self.rotate_var)
        rotate_entry.pack(pady=5)

        # Resize width input
        resize_width_label = ttk.Label(root, text="Resize Width (pixels):")
        resize_width_label.pack(pady=5)
        self.resize_width_var = tk.IntVar(value=self.original_image.width)
        resize_width_entry = ttk.Entry(root, textvariable=self.resize_width_var)
        resize_width_entry.pack(pady=5)

        # Resize height input
        resize_height_label = ttk.Label(root, text="Resize Height (pixels):")
        resize_height_label.pack(pady=5)
        self.resize_height_var = tk.IntVar(value=self.original_image.height)
        resize_height_entry = ttk.Entry(root, textvariable=self.resize_height_var)
        resize_height_entry.pack(pady=5)

        # Apply button
        apply_button = ttk.Button(root, text="Apply", command=self.apply_transformations)
        apply_button.pack(pady=10)

    def apply_transformations(self):
        # Get rotation and resize values
        rotation_angle = self.rotate_var.get()
        new_width = self.resize_width_var.get()
        new_height = self.resize_height_var.get()

        # Apply transformations
        transformed_image = self.original_image.rotate(-rotation_angle, expand=True)
        transformed_image = transformed_image.resize((new_width, new_height))

        # Update the canvas with the transformed image
        self.display_image = transformed_image
        self.photo_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo_image)

        # Draw bounding box
        self.draw_bounding_box(new_width, new_height)

    def draw_bounding_box(self, width, height):
        # Remove the previous bounding box if it exists
        if self.bounding_box:
            self.canvas.delete(self.bounding_box)

        # Calculate the bounding box coordinates
        x0 = 250 - width // 2
        y0 = 250 - height // 2
        x1 = 250 + width // 2
        y1 = 250 + height // 2

        # Draw a new bounding box
        self.bounding_box = self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
