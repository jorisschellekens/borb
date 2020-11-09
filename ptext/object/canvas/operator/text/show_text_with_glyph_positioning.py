import copy
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.object.canvas.event.text_render_event import TextRenderEvent
from ptext.primitive.pdf_array import PDFArray
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject
from ptext.primitive.pdf_string import PDFString


class ShowTextWithGlyphPositioning(CanvasOperator):
    """
    Show one or more text strings, allowing individual glyph positioning. Each
    element of array shall be either a string or a number. If the element is a
    string, this operator shall show the string. If it is a number, the operator
    shall adjust the text position by that amount; that is, it shall translate the
    text matrix, T . The number shall be expressed in thousandths of a unit
    mof text space (see 9.4.4, "Text Space Details"). This amount shall be
    subtracted from the current horizontal or vertical coordinate, depending
    on the writing mode. In the default coordinate system, a positive
    adjustment has the effect of moving the next glyph painted either to the
    left or down by the given amount. Figure 46 shows an example of the
    effect of passing offsets to TJ.
    """

    def __init__(self):
        super().__init__("TJ", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        if not isinstance(operands[0], PDFArray):
            raise PDFTypeError(
                expected_type=PDFArray, received_type=operands[0].__class__
            )

        for i in range(0, len(operands[0])):
            obj = operands[0][i]

            # display string
            if isinstance(obj, PDFString):
                tri = TextRenderEvent(canvas.graphics_state, obj)
                # render
                canvas.event_occurred(tri)
                # update text rendering location
                canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().length()
                continue

            # adjust
            if isinstance(obj, PDFNumber):
                gs = canvas.graphics_state
                adjust_unscaled = obj.get_float_value()
                adjust_scaled = (
                    -adjust_unscaled
                    * 0.001
                    * gs.font_size
                    * (gs.horizontal_scaling / 100)
                )
                gs.text_matrix[2][0] -= adjust_scaled
