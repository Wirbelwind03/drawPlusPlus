import tkinter as tk
from PIL import Image, ImageTk
import math


class ImageRotatorMover:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Rotator and Mover with Bounding Box")
        
        # Canvas setup
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load and resize image
        self.original_image = Image.open("data/assets/circle.jpg").resize((256, 256))
        self.image = self.original_image.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        
        # Image state
        self.image_id = None
        self.angle = 0
        self.image_center = [384, 384]  # Center of the image (mutable for movement)
        self.drag_start = None
        
        # Add image to canvas
        self.image_id = self.canvas.create_image(self.image_center, image=self.image_tk)
        
        # Add bounding boxes
        self.image_box = self.get_image_box(self.image)
        self.image_rect_id = self.canvas.create_rectangle(*self.image_box, outline="blue", width=2)
        self.bounding_box = self.image_box
        self.bounding_rect_id = self.canvas.create_rectangle(*self.bounding_box, outline="red", dash=(4, 4), width=2)
        
        # Add rotation button
        rotate_button = tk.Button(root, text="Rotate", command=self.rotate_image)
        rotate_button.pack()
        
        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_image)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)

    def get_image_box(self, image):
        """Returns the axis-aligned bounding box of the image."""
        width, height = image.size
        x0, y0 = self.image_center[0] - width // 2, self.image_center[1] - height // 2
        x1, y1 = self.image_center[0] + width // 2, self.image_center[1] + height // 2
        return (x0, y0, x1, y1)
    
    def rotate_image(self):
        """Rotates the image and updates its bounding box."""
        # Increase angle
        self.angle = (self.angle + 10) % 360
        
        # Rotate image
        self.image = self.original_image.rotate(self.angle, expand=True)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_id, image=self.image_tk)
        
        # Update image bounding box
        self.image_box = self.get_image_box(self.image)
        self.canvas.coords(self.image_rect_id, *self.image_box)
        
        # Update axis-aligned bounding box (dynamic bounding box)
        self.bounding_box = self.calculate_bounding_box()
        self.canvas.coords(self.bounding_rect_id, *self.bounding_box)
        
        # Display debug information
        self.update_debug_info()
    
    def calculate_bounding_box(self):
        """Calculate the axis-aligned bounding box of the rotated image."""
        width, height = self.image.size
        angle_rad = math.radians(self.angle)
        cos_a, sin_a = abs(math.cos(angle_rad)), abs(math.sin(angle_rad))
        
        # New bounding box dimensions
        new_width = width * cos_a + height * sin_a
        new_height = width * sin_a + height * cos_a
        
        x0 = self.image_center[0] - new_width // 2
        y0 = self.image_center[1] - new_height // 2
        x1 = self.image_center[0] + new_width // 2
        y1 = self.image_center[1] + new_height // 2
        
        return (x0, y0, x1, y1)
    
    def update_debug_info(self):
        """Display debug information on the canvas."""
        # Clear existing debug text
        self.canvas.delete("debug")
        
        # Image bounding box corners
        x0, y0, x1, y1 = self.image_box
        self.canvas.create_text(x0, y0 - 10, text=f"({int(x0)}, {int(y0)})", fill="blue", tag="debug")
        self.canvas.create_text(x1, y0 - 10, text=f"({int(x1)}, {int(y0)})", fill="blue", tag="debug")
        self.canvas.create_text(x0, y1 + 10, text=f"({int(x0)}, {int(y1)})", fill="blue", tag="debug")
        self.canvas.create_text(x1, y1 + 10, text=f"({int(x1)}, {int(y1)})", fill="blue", tag="debug")
        
        # Bounding box corners
        bx0, by0, bx1, by1 = self.bounding_box
        self.canvas.create_text(bx0, by0 - 10, text=f"({int(bx0)}, {int(by0)})", fill="red", tag="debug")
        self.canvas.create_text(bx1, by0 - 10, text=f"({int(bx1)}, {int(by0)})", fill="red", tag="debug")
        self.canvas.create_text(bx0, by1 + 10, text=f"({int(bx0)}, {int(by1)})", fill="red", tag="debug")
        self.canvas.create_text(bx1, by1 + 10, text=f"({int(bx1)}, {int(by1)})", fill="red", tag="debug")

    def start_drag(self, event):
        """Start dragging the image."""
        self.drag_start = (event.x, event.y)
    
    def drag_image(self, event):
        """Drag the image and update its position."""
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            
            # Update image center
            self.image_center[0] += dx
            self.image_center[1] += dy
            
            # Move image and bounding boxes
            self.canvas.move(self.image_id, dx, dy)
            self.canvas.move(self.image_rect_id, dx, dy)
            self.canvas.move(self.bounding_rect_id, dx, dy)
            
            # Update debug information
            self.image_box = self.get_image_box(self.image)
            self.bounding_box = self.calculate_bounding_box()
            self.update_debug_info()
            
            # Update drag start point
            self.drag_start = (event.x, event.y)
    
    def end_drag(self, event):
        """End the dragging action."""
        self.drag_start = None


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRotatorMover(root)
    root.mainloop()
