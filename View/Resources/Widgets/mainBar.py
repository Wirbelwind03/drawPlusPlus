import tkinter as tk
from tkinter import PhotoImage

class MainBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Creating a gap between icons by setting "minsize=100" every two column initializations
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1)

        self.rowconfigure(0, minsize=30)

        # Load images
        gear_image = PhotoImage(file="Data/Assets/gear.png")  # Make sure the image exists
        
        # Tool - Gear
        gearButton = tk.Button(self, image=gear_image, height=50, width=50)
        gearButton.image = gear_image  # Required to prevent the image from being collected by the garbage collector
        gearButton.grid(row=0, column=1)

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    mainBar = MainBar(root)
    mainBar.pack()
    root.mainloop()
