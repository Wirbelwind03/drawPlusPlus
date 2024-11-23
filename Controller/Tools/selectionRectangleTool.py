import tkinter as tk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Controller.canvasController import CanvasController
from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from Model.canvasImages import CanvasImages
from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class SelectionRectangleTool:
    """
    A class for the selection tool used in the canvas.
    The class handle the events and the functions tied to the selection tool

    Attributes
    -----------
    canvasViewModel : CanvasViewModel
        The canvas widget where the selection tool is used
    selectionRectangle : SelectionRectangle
        The selection rectangle that is present on the Canvas
    __tempStartCoordinates : Vector2
        Temporary variable to stock when the selection rectangle is going to be created
    __tempCanvasSelectionRectangle : int
        The ID of the selection rectangle drawn on the canvas, when the user is still resizing it
    """

    def __init__(self, view: tk.Canvas, model: CanvasImages, cc: CanvasController, srcc: SelectionRectangleCanvasController):
        # Connect the tool to the canvas
        self.view = view
        self.model = model
        # Connect the selection rectangle controller to the canvas
        self.CC = cc
        self.SRCC = srcc
        
        self.__debugBbox = -1

        self.__tempStartCoordinates = None
        self.__tempCanvasSelectionRectangle = -1
        
    def createDebugBbox(self):
        if self.__debugBbox:
            self.view.delete(self.__debugBbox)

        self.__debugBbox = self.view.create_rectangle(self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y, self.SRCC.selectionRectangle.max.x, self.SRCC.selectionRectangle.max.y, outline="black", width=2)

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

        if self.SRCC.hasSelectionRectangle() and self.SRCC.setAction(SelectionRectangleAction.NONE):
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
        
        # if the selection rectangle already exist on the canvas, delete it
        if self.SRCC.hasSelectionRectangle():
            self.SRCC.erase()

        # Save the starting point for the rectangle
        self.__tempStartCoordinates = mouseCoords

        # Create a rectangle (but don't specify the end point yet)
        self.__tempCanvasSelectionRectangle = self.view.create_rectangle(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, outline="black", width=2, dash=(2, 2))

    def on_mouse_drag(self, event):
        """
        A event for when the mouse is dragged over on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction != SelectionRectangleAction.NONE:
            # Update the coordinates and move the selection rectangle
            self.SRCC.on_mouse_drag(event)
            return

        # Update the rectangle as the mouse is dragged
        self.view.coords(self.__tempCanvasSelectionRectangle, self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y)

    def on_button_release(self, event):
        """
        A event for when the left click is released on the canvas

        Parameters
        -----------
        event : 
        """

        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.setAction(SelectionRectangleAction.NONE):
            return
        
        # On release, finalize the rectangle selection by setting its end coordinates
        # and draw the actual selection rectangle
        self.view.delete(self.__tempCanvasSelectionRectangle)

        # If the user has only clicked on the canvas and didn't resize the selection rectangle, 
        # don't create it
        if self.__tempStartCoordinates == mouseCoords:
            return

        self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(self.__tempStartCoordinates.x, self.__tempStartCoordinates.y, mouseCoords.x, mouseCoords.y, 10))
        self.SRCC.draw()

    def on_delete(self, event):
        if self.SRCC.hasSelectionRectangle():
            for imageId, image in self.model.images.items():
                if self.SRCC.selectionRectangle.attachedImage and self.SRCC.selectionRectangle.attachedImage.id == imageId:
                    break
                # check overlap with image and selection tool
                if self.SRCC.selectionRectangle.isIntersecting(image.bbox):
                    x1 = max(self.SRCC.selectionRectangle.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(self.SRCC.selectionRectangle.topRight.y, image.bbox.topRight.y)
                    x2 = min(self.SRCC.selectionRectangle.topRight.x, image.bbox.topRight.x)
                    y2 = min(self.SRCC.selectionRectangle.bottomRight.y, image.bbox.bottomRight.y)
                    #intersectRectangle = selectionToolRectangleBbox.getIntersectRectangle(image.bbox)
                    # Get the relative (to the image) position of the selection tool rectangle
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    
                    image.cut(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    
                    if DEBUG:
                        self.view.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
            
            self.CC.update()
            self.view.delete(self.__debugBbox)

    def on_control_c(self, event):
        if self.SRCC.hasSelectionRectangle():
            blankCanvasImage = CanvasImage.createBlank(self.SRCC.selectionRectangle.width, self.SRCC.selectionRectangle.height)
            isBlank = True
            for imageId, image in self.model.images.items():
                # check overlap with image and selection tool
                if self.SRCC.selectionRectangle.isIntersecting(image.bbox):
                    x1 = max(self.SRCC.selectionRectangle.topLeft.x, image.bbox.topLeft.x)
                    y1 = max(self.SRCC.selectionRectangle.topRight.y, image.bbox.topRight.y)
                    x2 = min(self.SRCC.selectionRectangle.topRight.x, image.bbox.topRight.x)
                    y2 = min(self.SRCC.selectionRectangle.bottomRight.y, image.bbox.bottomRight.y)
                    relativeCoords = Vector2(x1 - image.bbox.topLeft.x, y1 - image.bbox.topLeft.y)
                    
                    region = image.copy(relativeCoords.x, relativeCoords.y, x2 - x1, y2 - y1)
                    blankCanvasImage.paste(x1 - self.SRCC.selectionRectangle.topLeft.x, y1 - self.SRCC.selectionRectangle.topLeft.y, region)
                    isBlank = False

                    if DEBUG:
                        self.view.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

            if not isBlank:
                blankCanvasImage = self.CC.drawImage(blankCanvasImage, self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y)
                self.SRCC.selectionRectangle.attachedImage = blankCanvasImage

    def on_control_v(self, event):
        mouseCoords = Vector2(event.x, event.y)
        
        if self.SRCC.selectionRectangle.attachedImage:
            self.model.addImage(self.SRCC.selectionRectangle.attachedImage)
            self.CC.drawImage(self.SRCC.selectionRectangle.attachedImage, self.SRCC.selectionRectangle.min.x, self.SRCC.selectionRectangle.min.y)