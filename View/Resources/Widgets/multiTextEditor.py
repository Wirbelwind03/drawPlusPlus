import tkinter as tk
from tkinter import ttk

class MultiTextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a Notebook Widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add 4 tabs with text editors
        for i in range(1, 5):
            self.add_editor_tab(f"Tab {i}")

    def add_editor_tab(self, title):

        # Create an independent text editor
        frame = tk.Frame(self.notebook)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Create a canvas for line numbers
        line_numbers_canvas = tk.Canvas(frame, width=24)
        line_numbers_canvas.grid(row=0, column=0, sticky="ns")
        
        text = tk.Text(frame, wrap="word")
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=24)
        text.configure(yscrollcommand=vsb.set)
        text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        
        text.grid(row=0, column=1, sticky="nsew")
        vsb.grid(row=0, column=2, sticky="ns")

        # Function to update line numbers
        def update_line_numbers(event=None):
            line_numbers_canvas.delete("all")
            i = 0
            for line in text.get("1.0", "end-1c").split("\n"):
                line_numbers_canvas.create_text(5, i * 16.1, anchor="nw", text=str(i+1))
                i += 1

        # Bind the update function to the text widget changes
        text.bind("<KeyRelease>", update_line_numbers)
        text.bind("<MouseWheel>", update_line_numbers)

        # Add it as a new "tab" to the Notebook
        self.notebook.add(frame, text=title)
    
        # Initialize the line numbers
        update_line_numbers()

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    textEditor = MultiTextEditor(root)
    textEditor.pack()
    root.mainloop() 