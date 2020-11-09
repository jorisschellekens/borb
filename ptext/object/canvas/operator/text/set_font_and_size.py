from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.font.font import Font
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_null import PDFNull
from ptext.primitive.pdf_object import PDFObject


class SetFontAndSize(CanvasOperator):
    """
    Set the text font, T f , to font and the text font size, T fs , to size. font shall be
    the name of a font resource in the Font subdictionary of the current
    resource dictionary; size shall be a number representing a scale factor.
    There is no initial value for either font or size; they shall be specified
    explicitly by using Tf before any text is shown.
    """

    def __init__(self):
        super().__init__("Tf", 2)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        # get document
        page = canvas.parent.parent

        # lookup font dictionary
        font_ref = page.get(["Resources", "Font", operands[0].name])
        if font_ref == PDFNull():
            raise PDFTypeError(expected_type=Font, received_type=PDFNull)

        # font size
        font_size = operands[1].get_float_value()

        # set state
        canvas.graphics_state.font_size = font_size
        canvas.graphics_state.font = font_ref
