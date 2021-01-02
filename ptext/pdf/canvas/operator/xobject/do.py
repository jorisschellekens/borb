from typing import List

import PIL  # type: ignore [import]

from ptext.io.read_transform.types import AnyPDFType, Name
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


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

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        # get Page
        page = canvas.get_parent()  # type: ignore [attr-defined]

        # get XObject
        assert isinstance(operands[0], Name)
        xobject = (
            page["Resources"]["XObject"][operands[0]]
            if operands[0] in page["Resources"]["XObject"]
            else None
        )

        if isinstance(xobject, PIL.Image.Image):
            canvas.event_occurred(
                ImageRenderEvent(graphics_state=canvas.graphics_state, image=xobject)
            )
