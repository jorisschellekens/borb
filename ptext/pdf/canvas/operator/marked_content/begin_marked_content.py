from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_name import PDFName
from ptext.io.tokenize.types.pdf_object import PDFObject


class BeginMarkedContent(CanvasOperator):
    """
    Begin a marked-content sequence terminated by a balancing EMC
    operator. tag shall be a name object indicating the role or significance of
    the sequence.
    """

    def __init__(self):
        super().__init__("BMC", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFName):
            raise PDFTypeError(
                expected_type=PDFName, received_type=operands[0].__class__
            )
        canvas.marked_content_stack.append(operands[0])
