import tkinter as tk
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk  # Import Pillow for resize

class ImageUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def resizeImage(image, width: int, height: int) -> ImageTk.PhotoImage:
        resizedImage: Image = image.resize((width, height))
        return resizedImage
    
    @staticmethod
    def resizeImageFromPath(path: str, width: int, height: int) -> ImageTk.PhotoImage:
        image = Image.open(path)
        resizedImage: Image = image.resize((width, height))
        return resizedImage
        
    @staticmethod
    def resizePhotoImage(image: Image, width: int, height: int) -> ImageTk.PhotoImage:
        resizedImage: Image = image.resize((width, height))
        photoImage = ImageTk.PhotoImage(resizedImage)
        return photoImage
    
    @staticmethod
    def resizePhotoImageFromPath(path, width: int, height: int) -> ImageTk.PhotoImage:
        image = Image.open(path)
        resizedImage: Image = image.resize((width, height), Image.ANTIALIAS)
        photoImage = ImageTk.PhotoImage(resizedImage)
        return photoImage
    
    @staticmethod
    def removeWhiteBackground(image) -> None:
        image.convert("RGBA")
        datas = image.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        image.putdata(newData)
        return image