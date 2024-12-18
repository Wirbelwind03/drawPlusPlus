import tkinter as tk
from PIL import Image, ImageTk

# Fixed center and image size
CENTER_X, CENTER_Y = 320, 384  # Center coordinates
IMAGE_SIZE = (128, 256)        # Original size: width, height

def rotate_and_resize_image(image_path, rotation_angle, new_size):
    # Open the image using Pillow
    original_image = Image.open(image_path)
    
    # Resize the image
    resized_image = original_image.resize(new_size)
    
    # Rotate the image
    rotated_image = resized_image.rotate(rotation_angle, expand=True)
    
    return rotated_image

def update_canvas():
    global img_tk  # Keep a reference to prevent garbage collection
    
    # Get user inputs
    rotation_angle = int(angle_entry.get())
    new_width = int(width_entry.get())
    new_height = int(height_entry.get())
    
    # Process the image
    processed_image = rotate_and_resize_image(image_path, rotation_angle, (new_width, new_height))
    
    # Convert to Tkinter-compatible format
    img_tk = ImageTk.PhotoImage(processed_image)
    
    # Update canvas image
    canvas.itemconfig(image_on_canvas, image=img_tk)
    
    # Draw BBOX and corner coordinates
    draw_bbox(processed_image)

def draw_bbox(image):
    # Get image dimensions
    img_width, img_height = image.size
    
    # Clear previous drawings
    canvas.delete("debug")
    
    # Calculate the bounding box corners based on center
    x0 = CENTER_X - img_width // 2
    y0 = CENTER_Y - img_height // 2
    x1 = CENTER_X + img_width // 2
    y1 = CENTER_Y + img_height // 2
    
    # Draw bounding box
    canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="debug")
    
    # Draw corner coordinates
    corner_texts = [
        (x0, y0, f"({x0}, {y0})"),  # Top-left
        (x1, y0, f"({x1}, {y0})"),  # Top-right
        (x0, y1, f"({x0}, {y1})"),  # Bottom-left
        (x1, y1, f"({x1}, {y1})")   # Bottom-right
    ]
    for x, y, text in corner_texts:
        canvas.create_text(x, y, text=text, anchor="nw", fill="blue", font=("Arial", 10), tags="debug")

    # Display central debug text
    bbox_text = f"BBOX: ({x0}, {y0}) -> ({x1}, {y1})"
    canvas.create_text(CENTER_X, y1 + 10, text=bbox_text, fill="green", tags="debug")

# Image path
image_path = "data/assets/pencil.png"

# Tkinter GUI setup
root = tk.Tk()
root.title("Image BBOX and Corner Coordinates")

# Create a Frame for the input widgets (on the left)
input_frame = tk.Frame(root, width=200, bg="lightgray", padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Input labels and entry fields
tk.Label(input_frame, text="Rotation Angle:", bg="lightgray").pack(anchor="w")
angle_entry = tk.Entry(input_frame)
angle_entry.pack(anchor="w")
angle_entry.insert(0, "0")

tk.Label(input_frame, text="New Width:", bg="lightgray").pack(anchor="w")
width_entry = tk.Entry(input_frame)
width_entry.pack(anchor="w")
width_entry.insert(0, str(IMAGE_SIZE[0]))

tk.Label(input_frame, text="New Height:", bg="lightgray").pack(anchor="w")
height_entry = tk.Entry(input_frame)
height_entry.pack(anchor="w")
height_entry.insert(0, str(IMAGE_SIZE[1]))

# Update button
update_button = tk.Button(input_frame, text="Apply Transformations", command=update_canvas)
update_button.pack(pady=10)

# Canvas setup (to the right of the input frame)
canvas = tk.Canvas(root, width=640, height=768, bg="white")
canvas.pack(side=tk.RIGHT, expand=True)

# Load and display the initial image
img = Image.open(image_path).resize(IMAGE_SIZE)
img_tk = ImageTk.PhotoImage(img)
image_on_canvas = canvas.create_image(CENTER_X, CENTER_Y, anchor=tk.CENTER, image=img_tk)

root.mainloop()
