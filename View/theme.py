class Theme:
    def __init__(self):
        pass

    @staticmethod
    def MainBackgroundColor(settings):
        return "#201c1c" if settings["dark_mode"] else "#f0f0f0"

    @staticmethod
    def BackgroundColor(settings):
        return "#1f1f1f" if settings["dark_mode"] else "white"
    
    @staticmethod
    def InsertBackgroundColor(settings):
        return "white" if settings["dark_mode"] else "black"
    
    @staticmethod
    def FontColor(settings):
        return "white" if settings["dark_mode"] else "black"