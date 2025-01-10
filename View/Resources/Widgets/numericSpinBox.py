import tkinter as tk

class NumericSpinBox(tk.Spinbox):
    def __init__(self, parent: tk.Frame, *args, **kwargs):
        self.validate_cmd = parent.register(self.validate_input)

        super().__init__(
            parent,
            validate="key",
            validatecommand=(self.validate_cmd, "%P"),
            *args,  # Pass any additional positional arguments to the base Spinbox
            **kwargs  # Pass any additional keyword arguments to the base Spinbox
        )

    def validate_input(self, new_value: str):
        """
        Validate the Spinbox input to allow only numbers.

        Args:
            new_value (str): The proposed new value.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        return new_value.isdigit() or new_value == ""

    def get(self):
        """
        Get the current value of the Spinbox as an integer.

        Returns:
            int: The current numeric value of the Spinbox.
        """
        return int(super().get())

    def set(self, value):
        """
        Set the value of the Spinbox.

        Args:
            value (int): The value to set in the Spinbox.
        """
        self.delete(0, tk.END)
        self.insert(0, str(value))
