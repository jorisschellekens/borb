#!/usr/bin/env python

from typing import List

from ptext.io.read.types import AnyPDFType, Name
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


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

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the BDC operator
        """
        assert isinstance(operands[0], Name)
        canvas.marked_content_stack.append(operands[0])
