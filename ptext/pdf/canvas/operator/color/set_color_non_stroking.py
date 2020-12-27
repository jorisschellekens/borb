from decimal import Decimal
from typing import List

from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.color.color import CMYKColor, GrayColor, RGBColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetColorNonStroking(CanvasOperator):
    """
    (PDF 1.2) Same as SCN but used for nonstroking operations.
    """

    def __init__(self, canvas: "Canvas"):
        super().__init__("scn", 0)
        self.canvas = canvas

    def get_number_of_operands(self) -> int:
        none_stroke_color_space = self.canvas.graphics_state.stroke_color_space
        if none_stroke_color_space == "DeviceCMYK":
            return 4
        if none_stroke_color_space == "DeviceGray":
            return 1
        if none_stroke_color_space == "DeviceRGB":
            return 3
        return self.number_of_operands

    def invoke(self, canvas: "PDFCanvas", operands: List[AnyPDFType] = []):
        non_stroke_color_space = self.canvas.graphics_state.non_stroke_color_space
        if non_stroke_color_space == "DeviceCMYK":
            assert isinstance(operands[0], Decimal)
            assert isinstance(operands[1], Decimal)
            assert isinstance(operands[2], Decimal)
            assert isinstance(operands[3], Decimal)
            canvas.graphics_state.non_stroke_color = CMYKColor(
                operands[0],
                operands[1],
                operands[2],
                operands[3],
            )
            return

        if non_stroke_color_space == "DeviceGray":
            assert isinstance(operands[0], Decimal)
            canvas.graphics_state.non_stroke_color = GrayColor(operands[0])
            return

        if non_stroke_color_space == "DeviceRGB":
            assert isinstance(operands[0], Decimal)
            assert isinstance(operands[1], Decimal)
            assert isinstance(operands[2], Decimal)
            canvas.graphics_state.non_stroke_color = RGBColor(
                operands[0],
                operands[1],
                operands[2],
            )
            return
