from typing import List

import PIL

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_object import PDFObject


class Do(CanvasOperator):
    """
    Paint the specified XObject. The operand name shall appear as a key in
    the XObject subdictionary of the current resource dictionary (see 7.8.3,
    "Resource Dictionaries"). The associated value shall be a stream whose
    Type entry, if present, is XObject.

    The effect of Do depends on the value
    of the XObject’s Subtype entry, which may be Image (see 8.9.5, "Image
    Dictionaries"), Form (see 8.10, "Form XObjects"), or PS (see 8.8.2,
    "PostScript XObjects").
    """

    def __init__(self):
        super().__init__("Do", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFName):
            raise PDFTypeError(
                expected_type=PDFName, received_type=operands[0].__class__
            )

        # get Page
        page = canvas.get_parent()

        # get XObject
        resource_name = operands[0].name
        xobject = (
            page["Resources"]["XObject"][resource_name]
            if resource_name in page["Resources"]["XObject"]
            else None
        )

        if isinstance(xobject, PIL.Image.Image):
            canvas.event_occurred(
                ImageRenderEvent(graphics_state=canvas.graphics_state, image=xobject)
            )
