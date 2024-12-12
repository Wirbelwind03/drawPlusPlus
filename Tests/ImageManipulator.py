from tkinter import Tk, Label
from PIL import Image, ImageTk

# Path to your image
image_path = "data/assets/pencil.png"

# Initialize Tkinter window
root = Tk()
root.title("Rotate and Resize Image")

# Load the image using Pillow
image = Image.open(image_path)

# Rotate the image (e.g., 45 degrees counterclockwise)
rotated_image = image.rotate(45, expand=True)

# Resize the image (e.g., to 200x200 pixels)
resized_image = rotated_image.resize((64, 64))

# Convert the image back to a Tkinter-compatible format
tk_image = ImageTk.PhotoImage(resized_image)

# Display the image in a Label widget
label = Label(root, image=tk_image)
label.pack()

# Run the Tkinter event loop
root.mainloop()

