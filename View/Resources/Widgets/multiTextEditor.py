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
        
        text = tk.Text(frame, wrap="word")
        vsb = tk.Scrollbar(frame, orient="vertical", command=text.yview, width=20)
        text.configure(yscrollcommand=vsb.set)
        text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        
        text.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Add it as a new "tab" to the Notebook
        self.notebook.add(frame, text=title)

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    textEditor = MultiTextEditor(root)
    textEditor.pack()
    root.mainloop()