from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_name import PDFName
from ptext.primitive.pdf_object import PDFObject


class BeginMarkedContentWithPropertyList(CanvasOperator):
    """
    Begin a marked-content sequence with an associated property list,
    terminated by a balancing EMC operator. tag shall be a name object
    indicating the role or significance of the sequence. properties shall be
    either an inline dictionary containing the property list or a name object
    associated with it in the Properties subdictionary of the current resource
    dictionary (see 14.6.2, “Property Lists”).
    """

    def __init__(self):
        super().__init__("BDC", 2)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFName):
            raise PDFTypeError(
                expected_type=PDFName, received_type=operands[0].__class__
            )
        # TODO
        canvas.marked_content_stack.append(operands[0].name)
