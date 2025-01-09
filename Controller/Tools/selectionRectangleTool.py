import tkinter as tk
import io
from PIL import ImageGrab, Image, ImageTk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.Graphics.imageUtils import ImageUtils

from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController
from Controller.toolBarController import ToolBarController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class TempRectangleState:
    """
    

    Attributes
    -----------
    startCoords : Vector2
        Temporary variable to stock when the selection rectangle is going to be created
    canvasRectangleID : int
        The ID of the selection rectangle drawn on the canvas, when the user is still resizing it
    """
    def __init__(self):
        self.startCoords = None
        self.canvasRectangleID = -1

class SelectionRectangleTool:
    """
    A Controller to manage the selection rectangle tool inside a canvas

    Attributes
    -----------
    srcc : SelectionRectangleCanvasController
        A Controller used to communicate with the selection rectangle
    __tempStartCoordinates : Vector2
        Temporary variable to stock when the selection rectangle is going to be created
    __tempCanvasSelectionRectangle : int
        The ID of the selection rectangle drawn on the canvas, when the user is still resizing it
    """

    def __init__(self, srcc: SelectionRectangleCanvasController, TBC : ToolBarController):
        # Connect the selection rectangle controller to the tool
        self.SRCC = srcc
        self.TBC = TBC
        
        self.__debugBbox = -1
        self.__tempRectangleState = TempRectangleState()

    @property
    def canvas(self) -> tk.Canvas:
        return self.SRCC.CC.view
    
    @property
    def selectionRectangle(self) -> SelectionRectangle:
        return self.SRCC.selectionRectangle
        
    def createDebugBbox(self):
        if self.__debugBbox:
            self.canvas.delete(self.__debugBbox)

        self.__debugBbox = self.canvas.create_rectangle(self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.max.x, self.selectionRectangle.max.y, outline="black", width=2)

    def handle_clipboard_activation(self, activate: bool) -> None:
        icon = "clipboard_on.png" if activate else "clipboard_off.png"
        command = self.clipBoardPaste if activate else None
        image = ImageUtils.resizePhotoImageFromPath(f"Data/Assets/{icon}", 64, 64)
        self.TBC.view.pasteButton.configure(image=image, command=command)
        self.TBC.view.pasteButton.image = image

    def clipBoardPaste(self):
        if self.selectionRectangle.attachedImage:
            self.SRCC.CC.drawImage(self.selectionRectangle.attachedImage, self.selectionRectangle.min.x, self.selectionRectangle.min.y)


    #region Event

    def on_mouse_over(self, event):
        """
        A event for when the mouse is hovering on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle():
            self.SRCC.on_mouse_over(event)

    def on_button_press(self, event):
        """
        A event for when the user left click on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.SRCC.hasSelectionRectangle():
            # If there is a attached image inside the selection rectangle
            if self.selectionRectangle.attachedImage:
                self.SRCC.CC.deleteImage(self.selectionRectangle.attachedImage)
                self.selectionRectangle.attachedImage = None
                self.handle_clipboard_activation(False)
            # Erase the selection rectangle
            self.SRCC.deSelect()
            # Then save the coordinates where the mouse has clicked
            

        # Save the starting point for the rectangle
        self.__tempRectangleState.startCoords = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self.__tempRectangleState.canvasRectangleID = self.canvas.create_rectangle(
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            outline="black", 
            width=2, 
            dash=(2, 2)
        )

    def on_mouse_drag(self, event):
        """
        A event for when the mouse is dragged over on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            # Update the coordinates and move the selection rectangle
            self.SRCC.on_mouse_drag(event)
            return

        # Update the rectangle as the mouse is dragged
        self.canvas.coords(
            self.__tempRectangleState.canvasRectangleID, 
            self.__tempRectangleState.startCoords.x, 
            self.__tempRectangleState.startCoords.y, 
            mouseCoords.x, 
            mouseCoords.y
        )

        self.TBC.view.selectionRectangleWidth.set(abs(mouseCoords.x - self.__tempRectangleState.startCoords.x))
        self.TBC.view.selectionRectangleHeight.set(abs(mouseCoords.y - self.__tempRectangleState.startCoords.y))

        
    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            return
        
        # On release, finalize the rectangle selection by setting its end coordinates
        # and draw the actual selection rectangle
        self.canvas.delete(self.__tempRectangleState.canvasRectangleID)

        # If the user has only clicked on the canvas and didn't resize the selection rectangle, 
        # don't create it
        if self.__tempRectangleState.startCoords == mouseCoords:
            return

        self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(self.__tempRectangleState.startCoords.x, self.__tempRectangleState.startCoords.y, mouseCoords.x, mouseCoords.y))
        self.SRCC.create()

        self.TBC.view.selectionRectangleWidth.set(self.selectionRectangle.width)
        self.TBC.view.selectionRectangleHeight.set(self.selectionRectangle.height)

    def on_delete(self, event):
        if self.SRCC.hasSelectionRectangle() and not self.selectionRectangle.attachedImage:
            selectionRectangle = self.selectionRectangle
            for imageId, image in self.SRCC.CC.model.images.items():
                if selectionRectangle.attachedImage and selectionRectangle.attachedImage.id == imageId:
                    break
                # check overlap with image and selection tool
                if selectionRectangle.isIntersecting(image.bbox):
                    intersectRectangle = selectionRectangle.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(intersectRectangle.min.x - image.bbox.topLeft.x, intersectRectangle.min.y - image.bbox.topLeft.y)
                    
                    if DEBUG:
                        self.canvas.create_rectangle(intersectRectangle.min.x, intersectRectangle.min.y, intersectRectangle.max.x, intersectRectangle.max.y, outline="red", width=2)

                    image.cut(relativeCoords.x, relativeCoords.y, intersectRectangle.width, intersectRectangle.height)
            
            self.SRCC.CC.update()
            self.canvas.delete(self.__debugBbox)

    def on_control_c(self, event):
        if self.SRCC.hasSelectionRectangle():
            selectionRectangle = self.selectionRectangle
            blankCanvasImage = CanvasImage.createTransparent(self.selectionRectangle.width, self.selectionRectangle.height)
            isBlank = True
            for imageId, image in self.SRCC.CC.model.images.items():
                # check overlap with image and selection tool
                if selectionRectangle.isIntersecting(image.bbox):
                    intersectRectangle = selectionRectangle.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(intersectRectangle.min.x - image.bbox.topLeft.x, intersectRectangle.min.y - image.bbox.topLeft.y)
                    
                    if DEBUG:
                        self.canvas.create_rectangle(intersectRectangle.min.x, intersectRectangle.min.y, intersectRectangle.max.x, intersectRectangle.max.y, outline="red", width=2)

                    region = image.copy(relativeCoords.x, relativeCoords.y, intersectRectangle.width, intersectRectangle.height)
                    blankCanvasImage.paste(intersectRectangle.min.x - selectionRectangle.topLeft.x, intersectRectangle.min.y - selectionRectangle.topLeft.y, region)
                    isBlank = False

            # If there have images in the selection rectangle
            # Attach it to the selection rectangle
            if not isBlank:
                blankCanvasImage = self.SRCC.CC.drawImage(blankCanvasImage, self.selectionRectangle.min.x, self.selectionRectangle.min.y, self.selectionRectangle.width, self.selectionRectangle.height)
                self.selectionRectangle.attachedImage = blankCanvasImage
                self.activateClipBoardPaste()

        if self.SRCC.hasSelectionRectangle() and self.selectionRectangle.attachedImage:
            # If there is a attached image inside the selection rectangle
            self.SRCC.CC.deleteImage(self.selectionRectangle.attachedImage)
            self.selectionRectangle.attachedImage = None
            self.handle_clipboard_activation(True)

    def on_control_v(self, event):
        self.clipBoardPaste()

    #endregion Event