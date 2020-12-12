from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.color.color import CMYKColor, GrayColor, RGBColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class SetColorNonStroking(CanvasOperator):
    """
    (PDF 1.2) Same as SCN but used for nonstroking operations.
    """

    def __init__(self, canvas: "Canvas"):
        super().__init__("scn", 0)
        self.canvas = canvas

    def get_number_of_operands(self) -> int:
        none_stroke_color_space = self.canvas.graphics_state.stroke_color_space
        if none_stroke_color_space == PDFName("DeviceCMYK"):
            return 4
        if none_stroke_color_space == PDFName("DeviceGray"):
            return 1
        if none_stroke_color_space == PDFName("DeviceRGB"):
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
            canvas.graphics_state.non_stroke_color = CMYKColor(
                operands[0].get_decimal_value(),
                operands[1].get_decimal_value(),
                operands[2].get_decimal_value(),
                operands[3].get_decimal_value(),
            )
            return

        if non_stroke_color_space == PDFName("DeviceGray"):
            canvas.graphics_state.non_stroke_color = GrayColor(
                operands[0].get_decimal_value()
            )
            return

        if non_stroke_color_space == PDFName("DeviceRGB"):
            canvas.graphics_state.non_stroke_color = RGBColor(
                operands[0].get_decimal_value(),
                operands[1].get_decimal_value(),
                operands[2].get_decimal_value(),
            )
            return
