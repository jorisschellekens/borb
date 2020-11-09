import copy
import io
import os

from ptext.exception.pdf_exception import IllegalGraphicsStateError
from ptext.io.tokenizer.high_level_tokenizer import HighLevelTokenizer
from ptext.object.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.object.canvas.operator.color.set_cmyk_non_stroking import SetCMYKNonStroking
from ptext.object.canvas.operator.color.set_cmyk_stroking import SetCMYKStroking
from ptext.object.canvas.operator.color.set_color_non_stroking import (
    SetColorNonStroking,
)
from ptext.object.canvas.operator.color.set_color_stroking import SetColorStroking
from ptext.object.canvas.operator.color.set_gray_non_stroking import SetGrayNonStroking
from ptext.object.canvas.operator.color.set_gray_stroking import SetGrayStroking
from ptext.object.canvas.operator.color.set_rgb_non_stroking import SetRGBNonStroking
from ptext.object.canvas.operator.color.set_rgb_stroking import SetRGBStroking
from ptext.object.canvas.operator.state.modify_transformation_matrix import (
    ModifyTransformationMatrix,
)
from ptext.object.canvas.operator.state.pop_graphics_state import PopGraphicsState
from ptext.object.canvas.operator.state.push_graphics_state import PushGraphicsState
from ptext.object.canvas.operator.state.set_line_width import SetLineWidth
from ptext.object.canvas.operator.text.begin_text import BeginTextObject
from ptext.object.canvas.operator.text.end_text import EndTextObject
from ptext.object.canvas.operator.text.move_text_position import MoveTextPosition
from ptext.object.canvas.operator.text.move_text_position_set_leading import (
    MoveTextPositionSetLeading,
)
from ptext.object.canvas.operator.text.move_to_next_line import MoveToNextLine
from ptext.object.canvas.operator.text.move_to_next_line_show_text import (
    MoveToNextLineShowText,
)
from ptext.object.canvas.operator.text.set_character_spacing import SetCharacterSpacing
from ptext.object.canvas.operator.text.set_font_and_size import SetFontAndSize
from ptext.object.canvas.operator.text.set_horizontal_text_scaling import (
    SetHorizontalScaling,
)
from ptext.object.canvas.operator.text.set_spacing_move_to_next_line_show_text import (
    SetSpacingMoveToNextLineShowText,
)
from ptext.object.canvas.operator.text.set_text_leading import SetTextLeading
from ptext.object.canvas.operator.text.set_text_matrix import SetTextMatrix
from ptext.object.canvas.operator.text.set_text_rendering_mode import (
    SetTextRenderingMode,
)
from ptext.object.canvas.operator.text.set_text_rise import SetTextRise
from ptext.object.canvas.operator.text.set_word_spacing import SetWordSpacing
from ptext.object.canvas.operator.text.show_text import ShowText
from ptext.object.canvas.operator.text.show_text_with_glyph_positioning import (
    ShowTextWithGlyphPositioning,
)
from ptext.object.canvas.operator.xobject.do import Do
from ptext.object.pdf_high_level_object import PDFHighLevelObject
from ptext.primitive.pdf_canvas_operator_name import PDFCanvasOperatorName


class Canvas(PDFHighLevelObject):
    def __init__(self):
        super().__init__()
        # initialize operators
        self.canvas_operators = [
            # color
            SetCMYKNonStroking(),
            SetCMYKStroking(),
            SetColorNonStroking(self),
            SetColorStroking(self),
            SetGrayNonStroking(),
            SetGrayStroking(),
            SetRGBNonStroking(),
            SetRGBStroking(),
            # state
            ModifyTransformationMatrix(),
            PopGraphicsState(),
            PushGraphicsState(),
            SetLineWidth(),
            # text
            BeginTextObject(),
            EndTextObject(),
            MoveTextPosition(),
            MoveTextPositionSetLeading(),
            MoveToNextLineShowText(),
            MoveToNextLine(),
            SetCharacterSpacing(),
            SetFontAndSize(),
            SetHorizontalScaling(),
            SetSpacingMoveToNextLineShowText(),
            SetTextLeading(),
            SetTextMatrix(),
            SetTextRenderingMode(),
            SetTextRise(),
            SetWordSpacing(),
            ShowText(),
            ShowTextWithGlyphPositioning(),
            # xobject
            Do(),
        ]
        # set initial graphics state
        self.graphics_state = CanvasGraphicsState()
        # set graphics state stack
        self.graphics_state_stack = []

    def add_listener(self, canvas_listener: "CanvasListener") -> "Canvas":
        self.listeners.append(canvas_listener)
        return self

    def read(self, io_source: io.IOBase) -> "Canvas":

        io_source.seek(0, os.SEEK_END)
        length = io_source.tell()
        io_source.seek(0)

        canvas_tokenizer = HighLevelTokenizer(io_source)

        # process content
        operand_stk = []
        while canvas_tokenizer.tell() != length:

            # attempt to read object
            obj = canvas_tokenizer.read_object()
            if obj is None:
                break

            # push argument onto stack
            if not isinstance(obj, PDFCanvasOperatorName):
                operand_stk.append(obj)
                continue

            # process operator
            candidate_ops = [
                x for x in self.canvas_operators if x.get_text() == str(obj)
            ]
            if len(candidate_ops) == 1:
                operator = candidate_ops[0]
                if len(operand_stk) < operator.get_number_of_operands():
                    raise IllegalGraphicsStateError(
                        message="Unable to execute operator %s. Expected %d arguments, received %d."
                        % (
                            operator.text,
                            operator.get_number_of_operands(),
                            len(operand_stk),
                        )
                    )
                operands = []
                for _ in range(0, operator.get_number_of_operands()):
                    operands.insert(0, operand_stk.pop(-1))

                # append
                if not self.has_key("Instructions"):
                    self.set("Instructions", PDFHighLevelObject())

                instruction_number = len(self.get("Instructions"))

                self.get("Instructions").set(
                    instruction_number,
                    PDFHighLevelObject().set("Type", operator.get_text()),
                )
                if len(operands) > 0:
                    for i in range(0, len(operands)):
                        self.get(["Instructions", instruction_number]).set(
                            i, operands[i]
                        )

                # invoke
                operator.invoke(self, operands)

            # unknown operator
            if len(candidate_ops) == 0:
                # print("Missing OPERATOR %s" % obj)
                pass

        # return
        return self
