import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Graphics.canvasImage import CanvasImage

from Controller.selectionRectangleCanvasController import SelectionRectangleCanvasController

from Model.selectionRectangle import SelectionRectangleAction, SelectionRectangle

class SelectionTool:
    """
    A Controller to manage the selection tool inside a canvas

    Attributes
    -----------
    srcc : SelectionRectangleCanvasController
        A Controller used to communicate with the selection rectangle
    __copiedCanvasImage : CanvasImage
        The copied Canvas image, used for the pasting
    """

    def __init__(self, SRCC: SelectionRectangleCanvasController):
        # Connect the selection rectangle controller to the tool
        self.SRCC = SRCC

        self.__copiedCanvasImage = None

    @property
    def toolBar(self):
        return self.SRCC.TBC.view
    
    @property
    def canvas(self):
        return self.SRCC.CC.view

    def getClickedImage(self, mouseCoords):
        # Loop all the images present on the canvas
        for imageId, image in self.SRCC.CC.model.images.items():
            # Check if the mouse is inside the bounding box of the image
            if image.bbox.isInside(mouseCoords):
                self.setSelectedImage(image)
                return
            
    def setSelectedImage(self, image: CanvasImage):
        # Create the selection rectangle around the selected image
        self.SRCC.setSelectionRectangle(SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y), image)
        self.SRCC.create()

        # Activate the resize tool input in the tool bar
        self.toolBar.selectionRectangleWidth.set(self.SRCC.selectionRectangle.attachedImage.bbox.width) # Update the width input in the resize tool bar
        self.toolBar.selectionRectangleHeight.set(self.SRCC.selectionRectangle.attachedImage.bbox.height) # Update the height input in the resize tool bar
        self.toolBar.widthInput.configure(state="normal") # Activate the width input to not be read only
        self.toolBar.heightInput.configure(state="normal") # Activate the height input to not be read only

        # Check the action to move since the cursor is inside the image
        self.SRCC.setAction(SelectionRectangleAction.MOVE) # Set the action that the user can move the image
        self.canvas.config(cursor="fleur") # Change the cursor look

    #region Event

    def on_mouse_over(self, event: tk.Event) -> None:
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle():
            self.SRCC.on_mouse_over(event)

    def on_button_press(self, event: tk.Event) -> None:
        mouseCoords = Vector2(event.x, event.y)

        # If there isn't any select image, check if the user has clicked on one
        if not self.SRCC.hasSelectionRectangle():
            self.getClickedImage(mouseCoords)
            self.SRCC.handle_clipboard_cut_activation(True)
            self.SRCC.handle_clipboard_copy_activation(True)
        
        # If the cursor is outside the selected image/selection rectangle, deselect it
        if self.SRCC.hasSelectionRectangle() and self.SRCC.selectionRectangle.isOutside(mouseCoords):
            self.SRCC.deSelect()
            # Check if the user has clicked on another image
            self.getClickedImage(mouseCoords)
            self.SRCC.handle_clipboard_cut_activation(True)
            self.SRCC.handle_clipboard_copy_activation(True)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            # Calculate the offset between mouse click and rectangle's position
            self.SRCC.on_button_press(event)
            return
           
    def on_mouse_drag(self, event: tk.Event) -> None:
        mouseCoords = Vector2(event.x, event.y)

        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            self.SRCC.on_mouse_drag(event)
            return
        
    def on_button_release(self, event: tk.Event) -> None:
        mouseCoords = Vector2(event.x, event.y)
        
        if self.SRCC.hasSelectionRectangle() and self.SRCC.getAction() != SelectionRectangleAction.NONE:
            self.SRCC.on_button_release(event)
            pass
            #self.SRCC.setAction(SelectionRectangleAction.NONE)

    def on_delete(self, event: tk.Event) -> None:
        if self.SRCC.hasSelectionRectangle():
            self.SRCC.deleteSelectionRectangle()

    def on_control_c(self, event: tk.Event) -> None:
        if self.SRCC.hasSelectionRectangle() and self.SRCC.selectionRectangle.attachedImage:
            self.__copiedCanvasImage = self.SRCC.selectionRectangle.attachedImage

    def on_control_v(self, event: tk.Event) -> None:
        if self.SRCC.hasSelectionRectangle():
            if (self.__copiedCanvasImage):
                newCanvasImage = self.SRCC.CC.drawImage(self.__copiedCanvasImage, 0, 0)
                self.SRCC.deSelect()
                self.setSelectedImage(newCanvasImage)

    def on_left(self, event: tk.Event) -> None:
        if self.SRCC.hasSelectionRectangle():
            sr = self.SRCC.selectionRectangle
            self.SRCC.CC.rotateImage(sr.attachedImage, 10)
            #self.SRCC.CC.applyTransformations(sr.attachedImage, sr.width, sr.height, 10)
            self.SRCC.on_left(event)

            #self.toolBar.selectionRectangleWidth.set(self.SRCC.selectionRectangle.attachedImage.width)
            #self.toolBar.selectionRectangleHeight.set(self.SRCC.selectionRectangle.attachedImage.height)

    #endregion Event




