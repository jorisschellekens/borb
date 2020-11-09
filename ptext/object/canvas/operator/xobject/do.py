from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.event.image_render_event import ImageRenderEvent
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.object.canvas.xobject.image import Image
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject


class Do(CanvasOperator):
    def __init__(self):
        super().__init__("Do", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFName):
            raise PDFTypeError(
                expected_type=PDFName, received_type=operands[0].__class__
            )

        # get Page
        page = canvas.parent.parent

        # get XObject
        xobject = page.get(["Resources", "XObject", operands[0].name])

        if isinstance(xobject, Image):
            canvas.event_occurred(
                ImageRenderEvent(graphics_state=canvas.graphics_state, image=xobject)
            )
