import tkinter as tk
from PIL import Image, ImageTk

def rotate_and_resize_image(image_path, rotation_angle, new_size):
    # Open the image using Pillow
    original_image = Image.open(image_path)
    
    # Resize the image
    resized_image = original_image.resize(new_size)  # Smooth resizing
    
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
    processed_image = rotate_and_resize_image("data/assets/pencil.png", rotation_angle, (new_width, new_height))
    
    # Convert the image to Tkinter-compatible format
    img_tk = ImageTk.PhotoImage(processed_image)
    
    # Update the canvas with the new image
    canvas.itemconfig(image_on_canvas, image=img_tk)
    
    # Draw the bounding box
    draw_bbox(processed_image)

def draw_bbox(image):
    # Get the size of the image
    img_width, img_height = image.size
    
    # Clear previous bounding boxes
    canvas.delete("bbox")
    
    # Draw a rectangle as the bounding box
    x0, y0 = (250 - img_width // 2, 250 - img_height // 2)  # Top-left corner
    x1, y1 = (250 + img_width // 2, 250 + img_height // 2)  # Bottom-right corner
    
    canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="bbox")

# Tkinter GUI setup
root = tk.Tk()
root.title("Rotate, Resize Image and Draw BBOX")

# Canvas to display the image
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Load and display the initial image
img = Image.open("data/assets/pencil.png")
img_tk = ImageTk.PhotoImage(img)
image_on_canvas = canvas.create_image(250, 250, anchor=tk.CENTER, image=img_tk)

# Entry fields for rotation angle and new size
tk.Label(root, text="Rotation Angle:").pack()
angle_entry = tk.Entry(root)
angle_entry.pack()
angle_entry.insert(0, "0")

tk.Label(root, text="New Width:").pack()
width_entry = tk.Entry(root)
width_entry.pack()
width_entry.insert(0, "200")

tk.Label(root, text="New Height:").pack()
height_entry = tk.Entry(root)
height_entry.pack()
height_entry.insert(0, "200")

# Button to apply transformations and draw BBOX
update_button = tk.Button(root, text="Apply Transformations", command=update_canvas)
update_button.pack()

root.mainloop()
