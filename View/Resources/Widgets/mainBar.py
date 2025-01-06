import tkinter as tk
from tkinter import PhotoImage
from .gear import GearWindow

class MainBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settingsWindow = None

        self.grid(row=0, column=0, sticky="new")

        # Create a gap between icons by setting "minsize=100" for each two column initializations
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1)
        self.rowconfigure(0)

        # Load the image
        gear_image = PhotoImage(file="Data/Assets/gear.png")
        
        # Tool - Gear
        self.openSettingsButton = tk.Button(self, image=gear_image, height=50, width=50)
        self.openSettingsButton.image = gear_image
        self.openSettingsButton.grid(row=0, column=1)