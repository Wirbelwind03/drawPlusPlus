import tkinter as tk
from PIL import Image, ImageTk

from config import DEBUG

from Controller.canvasController import CanvasController

from DrawLibrary.Core.Math.vector2 import Vector2
from DrawLibrary.Core.Collision.aabb import AABB
from DrawLibrary.Graphics.canvasImage import CanvasImage
from DrawLibrary.Graphics.imageUtils import ImageUtils

from Model.canvasImages import CanvasImages
from Model.selectionRectangle import SelectionRectangle
from Model.selectionRectangle import SelectionRectangleAction

from Controller.toolBarController import ToolBarController

from View.Resources.Widgets.toolBar import ToolBar

class GapOffset:
    """
    The gap offset between the cursor and interior of the rectangle

    Attributes
    -----------
    start : Vector2
        The coordinates of the start gap offset
    end : Vector2
        The coordinates of the end gap offset
    """
    def __init__(self) -> None:
        self.start = Vector2(0, 0)
        self.end = Vector2(0, 0)

class SelectionRectangleCanvasController:
    """
    A class to manage the selection rectangle in the Canvas

    Attributes
    -----------
    CC : CanvasController
        A Controller used to communicate with the Canvas
    TBC : ToolBarController
        A Controller used to communicate with the ToolBar
    selectionRectangle : SelectionRectangle
        The selection rectangle present on the canvas
    clipBoardImage : CanvasImage
        The Canvas image stored in the clip board
    """

    def __init__(self, CC: CanvasController, TBC: ToolBarController) -> None:
        # Connect the controller to the canvas
        self.CC = CC
        self.TBC = TBC
        self.selectionRectangle: SelectionRectangle = None
        self.clipBoardImage : CanvasImage = None
        
        # Connect event to the input of the rotation
        self.toolBar.selectionRectangleRotation.trace_add("write", lambda *args: self.on_selection_rectangle_dimension_change("rotation"))
        self.toolBar.rotationInput.configure(command=self.on_rotation_input_change)

        # Connect event to the inputs of the resize
        self.toolBar.selectionRectangleWidth.trace_add("write", lambda *args: self.on_selection_rectangle_dimension_change("width"))
        self.toolBar.selectionRectangleHeight.trace_add("write", lambda *args: self.on_selection_rectangle_dimension_change("height"))
        self.toolBar.widthInput.configure(command=self.on_width_input_change)
        self.toolBar.heightInput.configure(command=self.on_height_input_change)

        self.toolBar.copyButton.configure(command=self.on_copy_button_click)
        self.toolBar.pasteButton.configure(command=self.on_paste_button_click)
        self.toolBar.cutButton.configure(command=self.on_cut_button_click)
        self.toolBar.eraserButton.configure(command=self.on_delete_button_click)

        self.__gapOffset = GapOffset()

    #region Properties

    @property
    def canvas(self) -> tk.Canvas:
        return self.CC.view
    
    @property
    def canvasImages(self):
        return self.CC.model.images.items()

    @property
    def toolBar(self) -> ToolBar:
        return self.TBC.view
    
    @property
    def action(self) -> SelectionRectangleAction:
        """
        Get the current action of the selection rectangle.

        Returns
        -----------
        SelectionRectangleAction
            The current action of the selection rectangle
        """
        return self.selectionRectangle.action
    
    @action.setter
    def action(self, action: SelectionRectangleAction) -> None:
        """
        Set the action of the selection rectangle.
        Also set the cursor.

        Parameters
        -----------
        action : SelectionRectangleAction
            What action to set for the selection rectangle
        """
        self.selectionRectangle.action = action
        if self.action == SelectionRectangleAction.RESIZE:
            self.CC.view.config(cursor="umbrella")
        elif self.action == SelectionRectangleAction.MOVE:
            self.CC.view.config(cursor="fleur")
        else:
            self.CC.view.config(cursor="arrow")

        # if DEBUG:
        #     print(f"Selection Rectangle Action set: {action.name}")

    #endregion

    #region Public Methods

    def setSelectionRectangle(self, selectionRectangle: SelectionRectangle, attachedImage: CanvasImage = None) -> None:
        """
        Set the selection rectangle on this controller

        Parameters
        -----------
        selectionRectangle : SelectionRectangle
            The selection rectangle the user want to set on this controller
        attachedImage: CanvasImage
            The image attached to the selection rectangle
        """
        self.selectionRectangle = selectionRectangle
        if attachedImage:
            self.selectionRectangle.attachedImage = attachedImage

        # Draw the main frame of the selection rectangle
        self.selectionRectangle.canvasIdRectangle = self.CC.view.create_rectangle(
            self.selectionRectangle.x, self.selectionRectangle.y, 
            self.selectionRectangle.x + self.selectionRectangle.width, self.selectionRectangle.y + self.selectionRectangle.height, 
            outline="black", width=2, dash=(2, 2)
        )

    def hasSelectionRectangle(self) -> bool:
        """
        Check if the canvas has a selection rectangle

        Returns
        -----------
        Bool
            If there is a selection rectangle present on the canvas
        """
        return self.selectionRectangle is not None
        
    def processIntersections(self, callback: callable):
        """
        Process intersections between the selection rectangle and canvas images.
        For each intersection, a callback is called
        The callback need to have as arguments :
            image : CanvasImage
                The intersecting CanvasImage
            intersect_rectangle : Rectangle
                The intersecting rectangle.
            relative_coords : Vector2
                The relative position of the intersection.

        Parameters
        ----------
        callback : callable
            The callback the user want to call for processing the intersections
        """
        sr = self.selectionRectangle
        for image_id, image in self.canvasImages:
            if sr.isIntersecting(image.bbox):
                intersectRectangle = sr.getIntersectRectangle(image.bbox)
                relative_coords = Vector2(
                    intersectRectangle.min.x - image.bbox.min.x,
                    intersectRectangle.min.y - image.bbox.min.y
                )

                if DEBUG:
                    self.canvas.create_rectangle(
                        intersectRectangle.min.x, intersectRectangle.min.y,
                        intersectRectangle.max.x, intersectRectangle.max.y,
                        outline="red", width=2
                    )

                # Execute the callback
                callback(image, intersectRectangle, relative_coords)

    def render(self) -> None:
        """
        Render the selection rectangle on the canvas
        """
        sr = self.selectionRectangle

        # Render the selection rectangle to the new position
        self.CC.view.coords(sr.canvasIdRectangle, sr.topLeft.x, sr.topLeft.y, sr.bottomRight.x,  sr.bottomRight.y)
        
        # Render the image to the new position
        if self.selectionRectangle.attachedImage:
            self.CC.view.coords(self.selectionRectangle.attachedImage.id, self.selectionRectangle.center.x, self.selectionRectangle.center.y)

    def deleteSelectionRectangle(self) -> None:
        """
        Delete completly the selection rectangle and the image inside it if there's one on the canvas.
        """
        if not self.selectionRectangle:
            return
        
        # If there is a attached image in the selection rectangle
        if self.selectionRectangle.attachedImage:
            # Delete the image first
            self.CC.deleteImage(self.selectionRectangle.attachedImage)
            self.selectionRectangle.attachedImage = None
            self.TBC.handle_button_activation("paste", False)
            if DEBUG:
                print("Deleting the selection rectangle")
                self.CC.DCC.erase(self.selectionRectangle.attachedImage)
            self.deSelect()

        elif not self.selectionRectangle.attachedImage:
            def deleteCallBack(image: CanvasImage, intersectRectangle: AABB, relativeCoords: Vector2):
                # Cut the intersecting region from the image
                image.cut(
                    relativeCoords.x, relativeCoords.y,
                    intersectRectangle.width, intersectRectangle.height
                )
            
            self.processIntersections(deleteCallBack)
            self.CC.update()
        

    def deSelect(self):
        """
        Deselect the selection rectangle on the canvas.
        """
        # Erase the rendering of the selection rectangle
        self.CC.view.delete(self.selectionRectangle.canvasIdRectangle)
        # Completly remove the selection rectangle
        self.selectionRectangle = None
        # Set the cursor to default (arrow)
        self.CC.view.config(cursor="arrow")

        # Deactivate the buttons
        self.TBC.handle_button_activation("paste", False)
        self.TBC.handle_button_activation("copy", False)
        self.TBC.handle_button_activation("cut", False)
        self.TBC.handle_button_activation("eraser", False)

        # Deactive the inputs of the resize
        self.toolBar.selectionRectangleWidth.set(0)
        self.toolBar.selectionRectangleHeight.set(0)
        self.toolBar.selectionRectangleRotation.set(0)
        self.toolBar.widthInput.configure(state="disabled")
        self.toolBar.heightInput.configure(state="disabled")
        self.toolBar.rotationInput.configure(state="disabled")

    def selectImage(self, image: CanvasImage):
        """
        Select a image that is present on the canvas

        Parameters
        -----------
        image : CanvasImage
            The image the user want to select
        """
        # Create the selection rectangle around the selected image
        self.setSelectionRectangle(SelectionRectangle.fromCoordinates(image.bbox.min.x, image.bbox.min.y, image.bbox.max.x, image.bbox.max.y), image)

        # Update the values
        self.toolBar.selectionRectangleWidth.set(self.selectionRectangle.attachedImage.width) 
        self.toolBar.selectionRectangleHeight.set(self.selectionRectangle.attachedImage.height)  
        self.toolBar.selectionRectangleRotation.set(self.selectionRectangle.attachedImage.angle)
        self.activate_operations()

        # Check the action to move since the cursor is inside the image
        self.action = SelectionRectangleAction.MOVE # Set the action that the user can move the image
        self.CC.view.config(cursor="fleur") # Change the cursor look

    def activate_operations(self):
        """
        Activate the operations on the ToolBar
        """
        self.toolBar.widthInput.configure(state="normal") # Activate the width input to not be read only
        self.toolBar.heightInput.configure(state="normal") # Activate the height input to not be read only
        self.toolBar.rotationInput.configure(state="normal")

        # Activate clip board operations
        self.TBC.handle_button_activation("cut", True, self.clipBoardCut)
        self.TBC.handle_button_activation("copy", True, self.clipBoardCopy)
        self.TBC.handle_button_activation("eraser", True)

    def clipBoardPaste(self) -> None:
        """
        Paste (aka draw) the clip board image on the canvas
        """
        if self.hasSelectionRectangle() and self.clipBoardImage:
            if DEBUG:
                print("Pasting the image")
            newCanvasImage = self.CC.drawImage(
                self.clipBoardImage, 
                self.selectionRectangle.min.x + self.selectionRectangle.width // 2, 
                self.selectionRectangle.min.y + self.selectionRectangle.height // 2, 
                self.selectionRectangle.width, self.selectionRectangle.height,
                self.selectionRectangle.attachedImage.angle
            )
            #self.selectImage(newCanvasImage)

    def clipBoardCopy(self) -> None:
        """
        Copy the attached image/images of the selection rectangle in the clip board
        """
        if not self.hasSelectionRectangle():
            return
        
        # If there only a selection rectangle
        if not self.selectionRectangle.attachedImage:
            sr = self.selectionRectangle
            blankCanvasImage = CanvasImage.createTransparent(sr.width, sr.height)
            isBlank = True

            def copyCallBack(image: CanvasImage, intersectRectangle: AABB, relativeCoords: Vector2) -> None:
                nonlocal isBlank
                region = image.copy(
                    relativeCoords.x, relativeCoords.y,
                    intersectRectangle.width, intersectRectangle.height
                )
                blankCanvasImage.paste(
                    intersectRectangle.min.x - sr.topLeft.x,
                    intersectRectangle.min.y - sr.topLeft.y,
                    region
                )
                isBlank = False
            
            self.processIntersections(copyCallBack)

            # If there have images detected inside the selection rectangle
            # Attach it to the selection rectangle
            if not isBlank:
                # Draw the composed image (created from detected regions) on the canvas
                blankCanvasImage = self.CC.drawImage(
                    blankCanvasImage, 
                    self.selectionRectangle.min.x + self.selectionRectangle.width // 2, 
                    self.selectionRectangle.min.y + self.selectionRectangle.height // 2, 
                    self.selectionRectangle.width, 
                    self.selectionRectangle.height
                )
                # Attach the created image to the selection rectangle
                self.selectionRectangle.attachedImage = blankCanvasImage 

        # If a image has been selected
        if self.selectionRectangle.attachedImage:
            if DEBUG:
                print("Copying the image")
            self.clipBoardImage = self.selectionRectangle.attachedImage.clone()
            # Activate the paste function of the clipboard
            self.TBC.handle_button_activation("paste", True, self.clipBoardPaste)

    def clipBoardCut(self) -> None:
        """
        Cut the attached image/images of the selection rectangle in the clip board
        """
        if not self.hasSelectionRectangle:
            return
        
        if not self.selectionRectangle.attachedImage:
            self.clipBoardCopy()

        if self.selectionRectangle.attachedImage:
            if DEBUG:
                print("Cutting the image")
            self.clipBoardImage = self.selectionRectangle.attachedImage.clone()
            self.CC.deleteImage(self.selectionRectangle.attachedImage)
            # Activate the paste function of the clipboard
            self.TBC.handle_button_activation("paste", True, self.clipBoardPaste)
            # Deactive the cut and copy function of the clipboard
            self.TBC.handle_button_activation("copy", False, self.clipBoardCopy)
            self.TBC.handle_button_activation("cut", False, self.clipBoardCut)

    #endregion Public Methods

    #region Private Methods

    #endregion

    #region ToolBar Events

    def on_selection_rectangle_dimension_change(self, configure):
        """
        Function get triggered whenever the user change the number in the inputs

        Parameters
        ----------
        configure : str
            What to change in the selection rectangle
        """
        try:
            if (not self.selectionRectangle):
                return
            
            # If the rectangle is attached to an image, resize and update it
            if self.selectionRectangle.attachedImage:
                if configure == "width":
                    self.selectionRectangle.attachedImage.width = self.toolBar.selectionRectangleWidth.get()
                elif configure == "height":
                    self.selectionRectangle.attachedImage.height = self.toolBar.selectionRectangleHeight.get()
                elif configure == "rotation":
                    self.selectionRectangle.attachedImage.angle = self.toolBar.rotationInput.get()

                # Apply the transformations from the inputs
                self.CC.applyTransformations(
                    self.selectionRectangle.attachedImage,
                    self.selectionRectangle.attachedImage.width,
                    self.selectionRectangle.attachedImage.height,
                    self.selectionRectangle.attachedImage.angle
                )

                # Update the selection rectangle position and dimensions
                self.selectionRectangle.setCoords(
                    self.selectionRectangle.attachedImage.bbox.topLeft,
                    self.selectionRectangle.attachedImage.bbox.bottomRight
                )

                # Draw debug information if debugging is enabled
                if DEBUG and self.CC.DCC is not None:
                    self.CC.DCC.drawCanvasImageDebugInformations(self.selectionRectangle.attachedImage)

            # If there is not image in the selection rectangle, resize the selection rectangle
            else:
                if configure == "width":
                    self.selectionRectangle.width = self.toolBar.selectionRectangleWidth.get()
                elif configure == "height":
                    self.selectionRectangle.height = self.toolBar.selectionRectangleHeight.get()


            # Update the selection rectangle on the canvas
            self.CC.view.coords(
                self.selectionRectangle.canvasIdRectangle,
                self.selectionRectangle.x,
                self.selectionRectangle.y,
                self.selectionRectangle.bottomRight.x,
                self.selectionRectangle.bottomRight.y
            )

        # If the input is empty
        except tk.TclError:
            if configure == "width":
                self.toolBar.selectionRectangleWidth.set(0)
            elif configure == "height":
                self.toolBar.selectionRectangleHeight.set(0)
            elif configure == "rotation":
                self.toolBar.selectionRectangleRotation.set(0)

    def on_width_input_change(self):
        """
        Function get triggered whenever the user change the number in the width input with the spin box
        """
        self.toolBar.selectionRectangleWidth.set(int(self.toolBar.widthInput.get()))

    def on_height_input_change(self):
        """
        Function get triggered whenever the user change the number in the height input with the spin box
        """
        self.toolBar.selectionRectangleHeight.set(int(self.toolBar.heightInput.get()))

    def on_rotation_input_change(self):
        """
        Function get triggered whenever the user change the number in the rotation input with the spin box
        """
        self.toolBar.selectionRectangleRotation.set(int(self.toolBar.rotationInput.get()))

    def on_copy_button_click(self):
        """
        Function get triggered whenever the user click the copy button
        """
        self.clipBoardCopy()
        if DEBUG:
            print("Copy button clicked")

    def on_paste_button_click(self):
        """
        Function get triggered whenever the user click the paste button
        """
        self.clipBoardPaste()
        if DEBUG:
            print("Paste button clicked")

    def on_cut_button_click(self):
        """
        Function get triggered whenever the user click the cut button
        """
        self.clipBoardCut()
        if DEBUG:
            print("Cut button clicked")

    def on_delete_button_click(self):
        """
        Function get triggered whenever the user click the delete button
        """
        self.deleteSelectionRectangle()

    #endregion

    #region Events

    def on_mouse_over(self, event) -> None:
        """
        Triggered when the mouse is over the canvas

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the mouse event, such as position (x, y).
        """
        if not self.hasSelectionRectangle():
            return

        mouseCoords = Vector2(event.x, event.y)
        
        # Check if the mouse is inside the selection rectangle    
        if self.selectionRectangle.isInside(mouseCoords):
            # If it is, change that the action we want to do is moving the selection rectangle
            self.action = SelectionRectangleAction.MOVE
        else:
            # If it's not, change that the action we want to do is creating a selection rectangle
            self.action = SelectionRectangleAction.NONE

    def on_button_press(self, event: tk.Event) -> None:
        """
        Triggered when the left mouse button is pressed on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button press event, such as position (x, y).
        """
        mouseCoords = Vector2(event.x, event.y)

        if self.action == SelectionRectangleAction.MOVE:
            # Get the gap between the cursor and the min and max of the AABB
            # So the user can move the rectangle by clicking anywhere inside
            self.__gapOffset.start = mouseCoords - self.selectionRectangle.min
            self.__gapOffset.end = mouseCoords - self.selectionRectangle.max

    def on_mouse_drag(self, event: tk.Event) -> None:
        """
        Triggered when the mouse is dragged across the canvas while the mouse left click is hold.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the drag event, such as position (x, y) and button state.
        """
        mouseCoords = Vector2(event.x, event.y)

        sr = self.selectionRectangle

        if self.action == SelectionRectangleAction.MOVE:
            # Update the selection rectangle coordinates
            self.selectionRectangle.setCoords(mouseCoords - self.__gapOffset.start, mouseCoords - self.__gapOffset.end)
            
            # Render the selection rectangle to the new position
            self.render()

        if DEBUG and self.CC.DCC != None:
            if self.selectionRectangle.attachedImage:
                self.CC.DCC.drawCanvasImageDebugInformations(self.selectionRectangle.attachedImage)

    def on_button_release(self, event: tk.Event) -> None:
        """
        Triggered when the left mouse click is released on the canvas.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the button release event, such as position (x, y).
        """
        # Get the cursor position
        mouseCoords = Vector2(event.x, event.y)

    def on_left(self, event: tk.Event) -> None:
        """
        Triggered when the left arrow key on the keyboard is pressed.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        mouseCoords = Vector2(event.x, event.y)

        if not self.hasSelectionRectangle():
            return

        if self.selectionRectangle.attachedImage:
            self.TBC.view.selectionRectangleRotation.set(self.selectionRectangle.attachedImage.angle + 15)
            self.selectionRectangle.setCoords(self.selectionRectangle.attachedImage.bbox.topLeft, self.selectionRectangle.attachedImage.bbox.bottomRight)

        # Render the selection rectangle to the new position
        self.render()

        if DEBUG and self.CC.DCC != None:
            self.CC.DCC.drawCanvasImageDebugInformations(self.selectionRectangle.attachedImage)

    def on_right(self, event: tk.Event) -> None:
        """
        Triggered when the right arrow key on the keyboard is pressed.

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        mouseCoords = Vector2(event.x, event.y)

        self.TBC.view.selectionRectangleRotation.set(self.selectionRectangle.attachedImage.angle - 15)
        self.selectionRectangle.setCoords(self.selectionRectangle.attachedImage.bbox.topLeft, self.selectionRectangle.attachedImage.bbox.bottomRight)

        # Render the selection rectangle to the new position
        self.render()

        if DEBUG and self.CC.DCC != None:
            self.CC.DCC.drawCanvasImageDebugInformations(self.selectionRectangle.attachedImage)

    def on_control_c(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+C" keyboard shortcut is pressed (Copy command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.clipBoardCopy()

    def on_control_v(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+V" keyboard shortcut is pressed (Paste command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.clipBoardPaste()

    def on_control_x(self, event: tk.Event) -> None:
        """
        Triggered when the "Ctrl+X" keyboard shortcut is pressed (Cut command).

        Parameters
        ----------
        event : tk.Event
            The event object containing details about the keypress event.
        """
        self.clipBoardCut()

    #endregion Event
