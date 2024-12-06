from PIL import Image, ImageTk
import os

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

from DrawLibrary.Graphics.canvasEntity import CanvasEntity

class CanvasImage(CanvasEntity):
    #region Constructor
    
    """
    A class representing a image on a tk.Canvas
    The class handle operation tied to the images

    Attributes
    -----------
    id : int
        The id of the CanvasImage drawn on a tk.Canvas
    filePath : str
        The file path of the image
    _width : int
        The width of the image
    _height : int
        The height of the image
    image : Image
    photoImage : ImageTK.PhotoImage
    bbox : AABB
        The bounding box tied to the image. It's used to know the position of the canvasEntity is etc.
    debugBbox : int
        The ID of the rectangle rendered on a tk.Canvas
    """

    def __init__(self) -> None:
        super().__init__()
        self.filePath: str = ""
        self._width: int = 0
        self._height: int = 0
        self.image: Image = None
        self.photoImage: ImageTk.PhotoImage = None

    @staticmethod
    def createBlank(width: int, height: int) -> 'CanvasImage':
        blankCanvasImage = CanvasImage()
        blankCanvasImage.width = width
        blankCanvasImage.height = height

        blankImage = Image.new("RGB", (width, height), "white")
        blankCanvasImage.image = blankImage
        blankCanvasImage.photoImage = ImageTk.PhotoImage(blankImage)

        return blankCanvasImage
    
    @classmethod
    def fromPath(cls, filePath: str) -> 'CanvasImage':
        """
        Load a image from a filepath

        Parameters
        -----------
        filePath : str
            The file path where the image is going to be loaded
        """

        try:
            # Check if the file exists
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"The file '{filePath}' does not exist.")
            canvasImage = CanvasImage()
            canvasImage.filePath = filePath
            canvasImage.image = Image.open(filePath)
            canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
            canvasImage.width, canvasImage.height = canvasImage.image.size
            return canvasImage
        except FileNotFoundError as e:
            print(e)

    #endregion Constructor

    #region Property

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width: int):
        self._width = width
        # Update the width of the AABB
        if self.bbox:
            self.bbox.width = self.width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height: int):
        self._height = height
        # Update the height of the AABB
        if self.bbox:
            self.bbox.height = self.height

    #endregion Property

    #region Public Methods

    def clone(self) -> 'CanvasImage':
        """
        Clone a existing CanvasImage

        Returns
        -----------
        CanvasImage
            The CanvasImage that was cloned
        """
        canvasImage = CanvasImage()
        canvasImage.id = -1
        canvasImage.image = self.image.copy()
        canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
        canvasImage.width = self.width
        canvasImage.height = self.height
        canvasImage.filePath = self.filePath
        canvasImage.bbox = self.bbox

        return canvasImage

    def cut(self, x: int, y: int, width: int, height: int) -> None:
        """
        Cut a CanvasImage, aka erasing a part of it

        Parameters
        -----------
        x : int
            The x position where the image is going to be cut from
        y : int
            The y position where the image is going to be cut from
        width : int
            The width the image is going to be cut from
        height : int
            The height the image is going to be cut from
        """

        # Create a blank image
        new_img = self.image.convert("RGBA")
        mask = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        # Paste it so the image feel it's cut
        new_img.paste(mask, (x, y))

        # Update the image
        self.image = new_img
        self.photoImage = ImageTk.PhotoImage(new_img)
    
    def resize(self, width: int, height: int) -> None: 
        """
        Resize a CanvasImage

        Parameters
        -----------
        width : int
            The width the image is going to be resized
        height : int
            The height the image is going to be resized
        """
        self.width = width
        self.height = height
        resizedImage = self.image.resize((self.width, self.height))
        # Update the photo image, keep the original one in the attribute image so it's doesn't resize the resized one
        self.photoImage = ImageTk.PhotoImage(resizedImage)

    def crop(self, x: int, y: int, width: int, height: int) -> None:
        self.image = self.image.crop((x, y, x + width, y + height))

    def copy(self, x: int, y: int, width: int, height: int) -> 'CanvasImage':
        """
        Copy a CanvasImage

        Parameters
        -----------
        x : int
            The x position of the image that is going to be copied
        y : int
            The y position of the image that is going to be copied
        width : int
            The width of the image that is going to be copied
        height : int
            The height of the image that is going to be copied

        Returns
        -----------
        CanvasImage
            A new CanvasImage that has been copied from another
        """
        newCanvasImage = self.clone()
        newCanvasImage.crop(x, y, width, height)

        return newCanvasImage

    def paste(self, x: int, y: int, canvasImage: 'CanvasImage') -> None:
        """
        Paste a CanvasImage

        Parameters
        -----------
        x : int
            The x position where the image is going to be pasted
        y : int
            The y position where the image is going to be pasted
        canvasImage : CanvasImage
            The CanvasImage that is going to be pasted
        """

        self.image.paste(canvasImage.image, (x, y))

    def createAABB(self, x, y, width=0, height=0):
        self.bbox = AABB(x, y, width, height)

    #endregion Public Methods