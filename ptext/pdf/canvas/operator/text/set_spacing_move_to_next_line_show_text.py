from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.text.move_to_next_line_show_text import (
    MoveToNextLineShowText,
)
from ptext.pdf.canvas.operator.text.set_character_spacing import SetCharacterSpacing
from ptext.pdf.canvas.operator.text.set_word_spacing import SetWordSpacing


class SetSpacingMoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string, using a w as the word spacing
    and a c as the character spacing (setting the corresponding parameters in
    the text state). a w and a c shall be numbers expressed in unscaled text
    space units. This operator shall have the same effect as this code:
    aw Tw
    ac Tc
    string '
    """

    def __init__(self):
        super().__init__('"', 3)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        SetWordSpacing().invoke(canvas, [operands[0]])
        SetCharacterSpacing().invoke(canvas, [operands[1]])
        MoveToNextLineShowText().invoke(canvas, [operands[2]])
