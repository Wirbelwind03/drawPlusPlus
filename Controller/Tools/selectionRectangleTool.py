import tkinter as tk
import io
from PIL import ImageGrab, Image, ImageTk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Controller.canvasController import CanvasController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

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

    def __init__(self, srcc: SelectionRectangleCanvasController):
        # Connect the selection rectangle controller to the tool
        self.SRCC = srcc
        
        self.__debugBbox = -1

        self.__tempStartCoordinates = None
        self.__tempCanvasSelectionRectangle = -1
        
    def createDebugBbox(self):
        if self.__debugBbox:
            self.SRCC.CC.view.delete(self.__debugBbox)

        self.__debugBbox = self.SRCC.CC.view.create_rectangle(self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y, self.SRCC.selectionRectangle.max.x, self.SRCC.selectionRectangle.max.y, outline="black", width=2)

    def findOverlaps(self):
        if self.SRCC.hasSelectionRectangle():
            selectionRectangle = self.SRCC.selectionRectangle
            for imageId, image in self.SRCC.CC.model.images.items():
                # check overlap with image and selection tool
                if selectionRectangle.isIntersecting(image.bbox):
                    intersectRectangle = selectionRectangle.getIntersectRectangle(image.bbox)
                    relativeCoords = Vector2(selectionRectangle.min.x - image.bbox.topLeft.x, selectionRectangle.min.y - image.bbox.topLeft.y)
                    
                    if DEBUG:
                        self.SRCC.CC.view.create_rectangle(selectionRectangle.min.x, selectionRectangle.min.y, selectionRectangle.max.x, selectionRectangle.max.y, outline="red", width=2)

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
            if self.SRCC.selectionRectangle.attachedImage:
                self.SRCC.CC.deleteImage(self.SRCC.selectionRectangle.attachedImage)
                self.SRCC.selectionRectangle.attachedImage = None
            # Erase the selection rectangle
            self.SRCC.deSelect()
            # Then save the coordinates where the mouse has clicked
            

        # Save the starting point for the rectangle
        self.__tempStartCoordinates = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self.__tempCanvasSelectionRectangle = self.SRCC.CC.view.create_rectangle(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, outline="black", width=2, dash=(2, 2))

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
        self.SRCC.CC.view.coords(self.__tempCanvasSelectionRectangle, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

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
        self.SRCC.CC.view.delete(self.__tempCanvasSelectionRectangle)

        # If the user has only clicked on the canvas and didn't resize the selection rectangle, 
        # don't create it
        if self.__tempStartCoordinates == mouseCoords:
            return

        self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y, 10))
        self.SRCC.create()

    def on_delete(self, event):
        if self.SRCC.hasSelectionRectangle():
            selectionRectangle = self.SRCC.selectionRectangle
            for imageId, image in self.SRCC.CC.model.images.items():
                if selectionRectangle.attachedImage and selectionRectangle.attachedImage.id == imageId:
                    break
                # check overlap with image and selection tool
                if selectionRectangle.isIntersecting(image.bbox):
                    intersectRectangle = selectionRectangle.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(intersectRectangle.min.x - image.bbox.topLeft.x, intersectRectangle.min.y - image.bbox.topLeft.y)
                    
                    if DEBUG:
                        self.SRCC.CC.view.create_rectangle(intersectRectangle.min.x, intersectRectangle.min.y, intersectRectangle.max.x, intersectRectangle.max.y, outline="red", width=2)

                    image.cut(relativeCoords.x, relativeCoords.y, intersectRectangle.width, intersectRectangle.height)
            
            self.SRCC.CC.update()
            self.SRCC.CC.view.delete(self.__debugBbox)

    def on_control_c(self, event):
        if self.SRCC.hasSelectionRectangle():
            selectionRectangle = self.SRCC.selectionRectangle
            blankCanvasImage = CanvasImage.createTransparent(self.SRCC.selectionRectangle.width, self.SRCC.selectionRectangle.height)
            isBlank = True
            for imageId, image in self.SRCC.CC.model.images.items():
                # check overlap with image and selection tool
                if selectionRectangle.isIntersecting(image.bbox):
                    intersectRectangle = selectionRectangle.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(intersectRectangle.min.x - image.bbox.topLeft.x, intersectRectangle.min.y - image.bbox.topLeft.y)
                    
                    if DEBUG:
                        self.SRCC.CC.view.create_rectangle(intersectRectangle.min.x, intersectRectangle.min.y, intersectRectangle.max.x, intersectRectangle.max.y, outline="red", width=2)

                    region = image.copy(relativeCoords.x, relativeCoords.y, intersectRectangle.width, intersectRectangle.height)
                    blankCanvasImage.paste(intersectRectangle.min.x - selectionRectangle.topLeft.x, intersectRectangle.min.y - selectionRectangle.topLeft.y, region)
                    isBlank = False

            if not isBlank:
                blankCanvasImage = self.SRCC.CC.drawImage(blankCanvasImage, self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y)
                self.SRCC.selectionRectangle.attachedImage = blankCanvasImage

    def on_control_v(self, event):
        if self.SRCC.selectionRectangle.attachedImage:
            self.SRCC.CC.drawImage(self.SRCC.selectionRectangle.attachedImage, self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y)

    #endregion Event