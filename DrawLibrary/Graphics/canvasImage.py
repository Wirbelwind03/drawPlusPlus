from PIL import Image, ImageTk
import os

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB

class CutImageInfos:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class CanvasImage:
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
    _center : Vector2
        The center of the canvasImage, it also represent the position
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
        self.id: int = -1
        self._center : Vector2 = None
        self.bbox: AABB = None
        self.filePath: str = ""
        self.width = 0
        self.height = 0
        self._angle: int = 0
        self.originalImage : Image = None
        self.image: Image = None
        self.photoImage: ImageTk.PhotoImage = None
        self.cuts = []

        self.debugBbox: int = -1  

    @staticmethod
    def createTransparent(width: int, height: int) -> 'CanvasImage':
        blankCanvasImage = CanvasImage()

        blankImage = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        blankCanvasImage.originalImage = blankImage
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
            canvasImage.originalImage = Image.open(filePath)
            canvasImage.image = canvasImage.originalImage
            canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
            canvasImage.width = canvasImage.image.width
            canvasImage.height = canvasImage.image.height
            canvasImage.angle = 0
            return canvasImage
        except FileNotFoundError as e:
            print(e)

    #endregion Constructor

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"_center={self._center}, "
            f"bbox={self.bbox},"
            f"filePath='{self.filePath}', "
            f"width={self.width}, "
            f"height={self.height}, "
            f"_angle={self.angle}, "
            f"image={self.image}, "
            f"photoImage={self.photoImage}, "
            f"debugBbox={self.debugBbox})"
        )

    #region Property

    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, newValue: int):
        self._angle = newValue % 360
    
    #endregion Property

    #region Public Methods

    def createAABB(self, x, y, width=0, height=0):
        self.bbox = AABB(x, y, width, height)

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
        
        canvasImage.originalImage = self.originalImage
        canvasImage.image = self.image 
        canvasImage.photoImage = ImageTk.PhotoImage(canvasImage.image)
        canvasImage.filePath = self.filePath

        canvasImage.width = self.width
        canvasImage.height = self.height
        canvasImage._angle = self.angle

        canvasImage.cuts = self.cuts

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

        self.cuts.append(CutImageInfos(x, y, width, height))

        # Create a blank image
        new_img = self.image.convert("RGBA")
        mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        # Paste it so the image feel it's cut
        new_img.paste(mask, (x, y))

        # Update the image
        self.image = new_img
        self.photoImage = ImageTk.PhotoImage(new_img)
    
    def crop(self, x: int, y: int, width: int, height: int) -> None:
        self.image = self.image.crop((x, y, x + width, y + height))

    def copy(self, x: int, y: int, width: int, height: int) -> 'CanvasImage':
        """
        Copy a CanvasImage, the difference with clone is that with this function, you can choose the
        region of the copied image

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

    def applyTransformations(self, width: int, height: int, degrees: int = 0):
        self.angle = degrees
        # Resize and rotate the image
        resized_image = self.originalImage.resize((width, height))
        rotated_image = resized_image.rotate(self.angle, expand=True)

        img_width, img_height = rotated_image.size
        
        # Draw a rectangle as the bounding box
        x0, y0 = (self.bbox.center.x - img_width // 2, self.bbox.center.y - img_height // 2)  # Top-left corner
        x1, y1 = (self.bbox.center.x + img_width // 2, self.bbox.center.y + img_height // 2)  # Bottom-right corner

        self.bbox.min = Vector2(x0, y0)
        self.bbox.max = Vector2(x1, y1)
        
        # Update canvas with transformed image
        self.image = rotated_image
        self.photoImage = ImageTk.PhotoImage(rotated_image)

    def removeWhiteBackground(self) -> None:
        self.image.convert("RGBA")

        datas = self.image.getdata()
    
        newData = []
    
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
    
        self.image.putdata(newData)

    #endregion Public Methods