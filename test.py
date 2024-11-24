import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import io

def copy_to_clipboard(canvas, bbox):
    """Copy the content of the bounding box to the clipboard."""
    # Get the bounding box coordinates relative to the screen
    x1 = canvas.winfo_rootx() + bbox[0]
    y1 = canvas.winfo_rooty() + bbox[1]
    x2 = canvas.winfo_rootx() + bbox[2]
    y2 = canvas.winfo_rooty() + bbox[3]

    # Capture the region using PIL
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    # Save the image data into a byte stream
    clipboard_data = io.BytesIO()
    image.save(clipboard_data, format="PNG")
    clipboard_data.seek(0)

    # Save to clipboard for later use
    canvas.clipboard_clear()
    canvas.clipboard_append(clipboard_data.getvalue())
    canvas.update()
    print("BBox copied to clipboard!")


def paste_from_clipboard(canvas, x, y):
    """Paste the content from the clipboard onto the canvas."""
    try:
        # Retrieve the clipboard data
        data = canvas.clipboard_get()
        image = Image.open(io.BytesIO(data.encode('latin1')))

        # Convert the image to a format usable by Tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Paste the image onto the canvas at the specified position
        canvas.create_image(x, y, anchor="nw", image=tk_image)
        canvas.image = tk_image  # Keep a reference to avoid garbage collection
        print("Pasted content from clipboard!")
    except Exception as e:
        print(f"Error while pasting: {e}")


# Tkinter application setup
root = tk.Tk()
root.geometry("600x600")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Draw some shapes on the canvas for testing
canvas.create_rectangle(50, 50, 150, 150, fill="blue")
canvas.create_oval(200, 50, 300, 150, fill="red")

# Define a bounding box (x1, y1, x2, y2) relative to the canvas
bbox = (50, 50, 150, 150)

# Buttons to copy and paste
copy_button = tk.Button(root, text="Copy BBox", command=lambda: copy_to_clipboard(canvas, bbox))
copy_button.pack()

paste_button = tk.Button(root, text="Paste Content", command=lambda: paste_from_clipboard(canvas, 300, 300))
paste_button.pack()

root.mainloop()
