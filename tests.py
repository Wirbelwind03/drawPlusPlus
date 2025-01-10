import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        
        # Load image
        self.image_path = "Data/assets/trash.png"
        self.original_image = Image.open(self.image_path)
        self.image = self.original_image
        
        # Canvas to display image
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(200, 200, image=self.tk_image)
        self.bounding_box_id = None  # ID for the bounding box rectangle

        # Controls
        tk.Label(self.root, text="Width:").grid(row=1, column=0, sticky="e")
        self.width_entry = ttk.Entry(self.root)
        self.width_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Height:").grid(row=2, column=0, sticky="e")
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Angle:").grid(row=3, column=0, sticky="e")
        self.angle_entry = ttk.Entry(self.root)
        self.angle_entry.grid(row=3, column=1)

        apply_button = ttk.Button(self.root, text="Apply", command=self.apply_transformations)
        apply_button.grid(row=4, column=0, columnspan=3)

    def apply_transformations(self):
        try:
            # Get new dimensions and rotation angle
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
            angle = int(self.angle_entry.get())
            
            # Resize and rotate the image
            resized_image = self.original_image.resize((new_width, new_height))
            rotated_image = resized_image.rotate(angle, expand=True)
            
            # Update canvas with transformed image
            self.image = rotated_image
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            
            # Get the bounding box and draw it
            self.draw_bounding_box()
        except ValueError:
            print("Invalid input. Please enter numeric values for width, height, and angle.")

    def draw_bounding_box(self):
        # Get the dimensions of the image
        width, height = self.image.size
        
        # Calculate bounding box coordinates (centered in the canvas)
        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])
        x1 = (canvas_width - width) // 2
        y1 = (canvas_height - height) // 2
        x2 = x1 + width
        y2 = y1 + height
        
        # Remove the old bounding box (if any)
        if self.bounding_box_id:
            self.canvas.delete(self.bounding_box_id)
        
        # Draw a rectangle for the bounding box
        self.bounding_box_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="red", width=2
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
