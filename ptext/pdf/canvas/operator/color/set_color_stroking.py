from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.color.color import GrayColor, RGBColor, CMYKColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class SetColorStroking(CanvasOperator):
    """
    (PDF 1.2) Same as SC but also supports Pattern, Separation, DeviceN
    and ICCBased colour spaces.
    If the current stroking colour space is a Separation, DeviceN, or
    ICCBased colour space, the operands c 1 ... c n shall be numbers. The
    number of operands and their interpretation depends on the colour space.
    If the current stroking colour space is a Pattern colour space, name shall
    be the name of an entry in the Pattern subdictionary of the current
    resource dictionary (see 7.8.3, "Resource Dictionaries"). For an
    uncoloured tiling pattern (PatternType = 1 and PaintType = 2), c 1 ... c n
    shall be component values specifying a colour in the pattern’s underlying
    colour space. For other types of patterns, these operands shall not be
    specified.
    """

    def __init__(self, canvas: "Canvas"):
        super().__init__("SCN", 0)
        self.canvas = canvas

    def get_number_of_operands(self) -> int:
        stroke_color_space = self.canvas.graphics_state.stroke_color_space
        if stroke_color_space == PDFName("DeviceCMYK"):
            return 4
        if stroke_color_space == PDFName("DeviceGray"):
            return 1
        if stroke_color_space == PDFName("DeviceRGB"):
            return 3
        return self.number_of_operands

    def invoke(self, canvas: "PDFCanvas", operands: List[PDFObject] = []):
        for i in range(0, len(operands)):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )
        non_stroke_color_space = self.canvas.graphics_state.non_stroke_color_space
        if non_stroke_color_space == PDFName("DeviceCMYK"):
            canvas.graphics_state.stroke_color = CMYKColor(
                operands[0].get_decimal_value(),
                operands[1].get_decimal_value(),
                operands[2].get_decimal_value(),
                operands[3].get_decimal_value(),
            )
            return

        if non_stroke_color_space == PDFName("DeviceGray"):
            canvas.graphics_state.stroke_color = GrayColor(
                operands[0].get_decimal_value()
            )
            return

        if non_stroke_color_space == PDFName("DeviceRGB"):
            canvas.graphics_state.stroke_color = RGBColor(
                operands[0].get_decimal_value(),
                operands[1].get_decimal_value(),
                operands[2].get_decimal_value(),
            )
            return
