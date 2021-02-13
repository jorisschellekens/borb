from typing import List, Optional

from ptext.io.read.types import AnyPDFType, Decimal
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


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

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        """
        Invoke the Tf operator
        """

        # get document
        page = canvas.get_parent()  # type: ignore [attr-defined]

        # lookup font dictionary
        font_ref: Optional[Font] = None
        if (
            "Resources" in page
            and "Font" in page["Resources"]
            and operands[0] in page["Resources"]["Font"]
        ):
            font_ref = page["Resources"]["Font"][operands[0]]
        assert font_ref is not None
        assert isinstance(font_ref, Font)

        # font size
        font_size = operands[1]
        assert isinstance(font_size, Decimal)

        # set state
        canvas.graphics_state.font_size = font_size
        canvas.graphics_state.font = font_ref
