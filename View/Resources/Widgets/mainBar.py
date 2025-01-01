import tkinter as tk
from tkinter import PhotoImage
from .gear import GearWindow

class MainBar(tk.Frame):
    def open_window(self):
        # Create a new window when the gear button is pressed
        new_window = GearWindow(self.master)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Create a gap between icons by setting "minsize=100" for each two column initializations
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1)

        self.rowconfigure(0)

        # Load the image
        gear_image = PhotoImage(file="Data/Assets/gear.png")
        
        # Tool - Gear
        gearButton = tk.Button(self, image=gear_image, height=50, width=50, command=self.open_window)
        gearButton.image = gear_image
        gearButton.grid(row=0, column=1)

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    mainBar = MainBar(root)
    mainBar.pack()
    root.mainloop()
