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
        self._angle: int = 0
        self.image: Image = None
        self.photoImage: ImageTk.PhotoImage = None
        self._angle = 0

    @staticmethod
    def createTransparent(width: int, height: int) -> 'CanvasImage':
        blankCanvasImage = CanvasImage()

        blankImage = Image.new("RGBA", (width, height), (0, 0, 0, 0))
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
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, degrees: int):
        self._angle = (self.angle + degrees) % 360

    @property
    def width(self):
        return self.image.size[0]
    
    @property
    def height(self):
        return self.image.size[1]
    
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
        canvasImage.bbox = self.bbox
        
        canvasImage.image = self.image.copy()
        canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
        canvasImage.filePath = self.filePath

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

    def updatePhotoImage(self, width: int, height: int, degrees: int = 0) -> None:
        # self.angle = degrees
        # rotatedImage: Image = self.image.rotate(self.angle, expand=True)
        # rotatedWidth, rotatedHeight = rotatedImage.size
        # # Resize the bbox of the CanvasImage
        # self.bbox.min = Vector2(self.center.x - rotatedWidth // 2, self.center.y - rotatedHeight // 2)
        # self.bbox.max = Vector2(self.center.x + rotatedWidth // 2, self.center.y + rotatedHeight // 2)
        # resizedImage = rotatedImage.resize((rotatedWidth, rotatedHeight))

        # # self.bbox.width = width
        # # self.bbox.height = height
        # #finalImage = resizedImage.resize((width, height))

        # self.photoImage = ImageTk.PhotoImage(resizedImage)
        testImage = self.updateImage(width, height, degrees)

        self.photoImage = ImageTk.PhotoImage(testImage)

        img_width, img_height = testImage.size
        
        # Draw a rectangle as the bounding box
        x0, y0 = (self.center.x - img_width // 2, self.center.y - img_height // 2)  # Top-left corner
        x1, y1 = (self.center.x + img_width // 2, self.center.y + img_height // 2)  # Bottom-right corner

        self.bbox.min = Vector2(x0, y0)
        self.bbox.max = Vector2(x1, y1)

    def updateImage(self, width, height, degrees = 0) -> Image:
        self.angle = degrees

        resizedImage: Image = self.image.resize((width, height))

        rotatedImage: Image = resizedImage.rotate(self.angle, expand=True)
        
        return rotatedImage
    
    def resizePhotoImage(self, width: int, height: int) -> None: 
        """
        Resize a CanvasImage

        Parameters
        -----------
        width : int
            The width the image is going to be resized
        height : int
            The height the image is going to be resized
        """
        # Resize the bbox of the CanvasImage
        self.bbox.width = width
        self.bbox.height = height
        resizedImage = self.image.resize((width, height))
        # Update the photoImage, keep the original one in the attribute image so it's doesn't resize the resized one
        self.photoImage = ImageTk.PhotoImage(resizedImage)

    def rotatePhotoImage(self, degrees: int):
        self.angle = degrees

        rotatedImage: Image = self.image.rotate(self.angle, expand=True)
        # Update the photoImage, keep the original one in the attribute image so it's doesn't resize the rotated one
        self.photoImage = ImageTk.PhotoImage(rotatedImage)

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

    def getImageBox(self):
        """Returns the axis-aligned bounding box of the image."""
        x0, y0 = self.center.x - self.width // 2, self.center.y - self.height // 2
        x1, y1 = self.center.x + self.width // 2, self.center.y + self.height // 2
        return (x0, y0, x1, y1)

    #endregion Public Methods