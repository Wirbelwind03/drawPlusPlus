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
        self.image: Image = None
        self.photoImage: ImageTk.PhotoImage = None

        self._angle: int = 0

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
            return canvasImage
        except FileNotFoundError as e:
            print(e)

    #endregion Constructor

    #region Property

    @property
    def width(self):
        return self.image.size[0]
    
    @property
    def height(self):
        return self.image.size[1]
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, degrees: int):
        self._angle = (self.angle + degrees) % 360

    @property
    def center(self):
        return Vector2(self.x + self.image.size[0] // 2, self.y + self.image.size[1] // 2)

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
        canvasImage.x, canvasImage.y = self.x, self.y
        canvasImage.image = self.image.copy()
        canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
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
        mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
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
        self.bbox.width, self.bbox.height = width, height
        resizedImage = self.image.resize((width, height))
        self.image = resizedImage
        self.photoImage = ImageTk.PhotoImage(resizedImage)

    def resizePhotoImage(self, width: int, height: int):
        """
        Resize the photo image of a CanvasImage
        The image attribute doesn't get replaced. 

        Parameters
        -----------
        width : int
            The width the image is going to be resized
        height : int
            The height the image is going to be resized
        """
        self.bbox.width, self.bbox.height = width, height
        resizedImage = self.image.resize((width, height))
        # Update the photo image, keep the original one in the attribute image so it's doesn't resize a resized one
        self.photoImage = ImageTk.PhotoImage(resizedImage)

    def rotatePhotoImage(self, degrees: int):
        self.angle = degrees

        rotatedImage: Image = self.image.rotate(self.angle, resample=Image.BICUBIC, expand=True)
        self.bbox.width, self.bbox.height = rotatedImage.size
        self.photoImage = ImageTk.PhotoImage(rotatedImage)
        self.bbox.min = Vector2(self.center.x - self.bbox.width // 2, self.center.y - self.bbox.height // 2)

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

    #endregion Public Methods