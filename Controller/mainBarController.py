import tkinter as tk

from Controller.settingsWindowController import SettingsWindowController

from View.Resources.Widgets.mainBar import MainBar
from View.Resources.Widgets.gear import SettingsWindow

class MainBarController:
    """
        Attributes
        -----------
        view : MainBar
        SC : SettingsWindowController
        on_settings_window_closed_callback : callable
    """
    def __init__(self, view: MainBar, SC: SettingsWindowController) -> None:
        self.view = view
        self.SC = SC

        self.on_settings_window_closed_callback: callable = None
        
        # Attach the open settings window event to the button
        self.view.openSettingsButton.configure(command=self.open_settings_window)

    def set_event_setting_window_close(self, event: callable) -> None:
        """
        Set the event to be triggered when the settings window get closed 

        Parameters
        ----------
        event : tk.Event
            The event to be called when the settings window get closed
        """
        self.on_settings_window_closed_callback = event

    def open_settings_window(self) -> None:
        """
        Open the settings window, bind the event when it's get closed
        Attach the setting controller to it, and load the settings saved in "appSettings.json"
        """
        # Create a new window when the gear button is pressed
        settingsWindow = SettingsWindow(self.view)
        # Bind the "<Destroy>" event to detect when the window is closed
        settingsWindow.bind("<Destroy>", self.on_settings_window_closed)
        # Attach the setting controller to the settings window that has been opened
        self.SC.attach(settingsWindow)
        # Load the settings saved in "appSettings.json"
        self.SC.load_settings()

    def on_settings_window_closed(self, event: tk.Event) -> None:
        """
        Call the callback when the settings window get closed

        Parameters
        ----------
        event : tk.Event
            The event to be called when the settings window get closed
        """
        if event.widget == self.SC.gearWindow:  # Ensure it's the gearWindow that triggered the event
            self.SC.save_settings()
            if self.on_settings_window_closed_callback:
                self.on_settings_window_closed_callback()