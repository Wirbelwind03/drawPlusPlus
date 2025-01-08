import tkinter as tk

from Controller.settingsWindowController import SettingsWindowController

from View.Resources.Widgets.mainBar import MainBar
from View.Resources.Widgets.gear import SettingsWindow

class MainBarController:
    def __init__(self, view: MainBar, SC: SettingsWindowController) -> None:
        self.view = view
        self.SC = SC

        self.on_settings_window_closed_callback = None  # Callback attribute
        
        self.view.openSettingsButton.configure(command=self.open_settings_window)

    def set_event_setting_window_close(self, event):
        self.on_settings_window_closed_callback = event

    def open_settings_window(self):
        # Create a new window when the gear button is pressed
        settingsWindow = SettingsWindow(self.view)
        # Bind the "<Destroy>" event to detect when the window is closed
        settingsWindow.bind("<Destroy>", self.on_settings_window_closed)
        self.SC.attach(settingsWindow)
        self.SC.load_settings()

    def on_settings_window_closed(self, event):
        """
        Callback triggered when the gearWindow is destroyed.
        """
        if event.widget == self.SC.gearWindow:  # Ensure it's the gearWindow that triggered the event
            self.SC.save_settings()
            if self.on_settings_window_closed_callback:
                self.on_settings_window_closed_callback()