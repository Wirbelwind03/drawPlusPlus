import tkinter as tk
from tkinter import PhotoImage

class MainBar(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="new")

        # Creating a gap between icons by setting "minsize=100" every two column initializations
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1)
        self.rowconfigure(0, minsize=30)

        # Load images
        gear_image = PhotoImage(file="Data/Assets/gear.png")  # Make sure the image exists

        # Tool - Gear
        gearButton = tk.Button(self, image=gear_image, height=50, width=50, command=self.open_settings_window)
        gearButton.image = gear_image  # Required to prevent the image from being collected by the garbage collector
        gearButton.grid(row=0, column=1)

        # Instance variable to track the settings window
        self.settings_window = None

    def open_settings_window(self):
        """Open the settings window if not already open."""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            # Create the settings window
            self.settings_window = tk.Toplevel(self)
            self.settings_window.title("Réglages")

            # Setting window size
            self.geometry("1080x1920")

            # Example content for the settings window
            label = tk.Label(self.settings_window, text="Réglages", font=("Arial", 14))
            label.pack(pady=20)

            close_button = tk.Button(self.settings_window, text="Fermer", command=self.settings_window.destroy)
            close_button.pack(pady=10)
        else:
            # If the window is already open, bring it to the front
            self.settings_window.lift()

# Main window
if __name__ == "__main__":
    root = tk.Tk()
    mainBar = MainBar(root)
    mainBar.pack()
    root.mainloop()
