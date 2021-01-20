from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.path_construction.close_subpath import CloseSubpath
from ptext.pdf.canvas.operator.path_painting.stroke_path import StrokePath


class CloseAndStrokePath(CanvasOperator):
    """
    Close and stroke the path. This operator shall have the same effect as the
    sequence h S.
    """

    def __init__(self):
        super().__init__("s", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        CloseSubpath().invoke(canvas, [])
        StrokePath().invoke(canvas, [])
