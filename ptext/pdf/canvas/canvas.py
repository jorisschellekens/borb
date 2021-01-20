import io
import logging
import os
import typing

from ptext.exception.pdf_exception import IllegalGraphicsStateError
from ptext.io.read_transform.types import (
    Dictionary,
    List,
    CanvasOperatorName,
)
from ptext.io.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.pdf.canvas.operator.color.set_cmyk_non_stroking import SetCMYKNonStroking
from ptext.pdf.canvas.operator.color.set_cmyk_stroking import SetCMYKStroking
from ptext.pdf.canvas.operator.color.set_color_non_stroking import (
    SetColorNonStroking,
)
from ptext.pdf.canvas.operator.color.set_color_stroking import SetColorStroking
from ptext.pdf.canvas.operator.color.set_gray_non_stroking import SetGrayNonStroking
from ptext.pdf.canvas.operator.color.set_gray_stroking import SetGrayStroking
from ptext.pdf.canvas.operator.color.set_rgb_non_stroking import SetRGBNonStroking
from ptext.pdf.canvas.operator.color.set_rgb_stroking import SetRGBStroking
from ptext.pdf.canvas.operator.compatibility.begin_compatibility_section import (
    BeginCompatibilitySection,
)
from ptext.pdf.canvas.operator.compatibility.end_compatibility_section import (
    EndCompatibilitySection,
)
from ptext.pdf.canvas.operator.marked_content.begin_marked_content import (
    BeginMarkedContent,
)
from ptext.pdf.canvas.operator.marked_content.begin_marked_content_with_property_list import (
    BeginMarkedContentWithPropertyList,
)
from ptext.pdf.canvas.operator.marked_content.end_marked_content import (
    EndMarkedContent,
)
from ptext.pdf.canvas.operator.path_construction.append_cubic_bezier import (
    AppendCubicBezierCurve1,
    AppendCubicBezierCurve2,
    AppendCubicBezierCurve3,
)
from ptext.pdf.canvas.operator.path_construction.append_line_segment import (
    AppendLineSegment,
)
from ptext.pdf.canvas.operator.path_construction.begin_subpath import BeginSubpath
from ptext.pdf.canvas.operator.path_construction.close_subpath import CloseSubpath
from ptext.pdf.canvas.operator.path_painting.close_and_stroke_path import (
    CloseAndStrokePath,
)
from ptext.pdf.canvas.operator.path_painting.stroke_path import StrokePath
from ptext.pdf.canvas.operator.state.modify_transformation_matrix import (
    ModifyTransformationMatrix,
)
from ptext.pdf.canvas.operator.state.pop_graphics_state import PopGraphicsState
from ptext.pdf.canvas.operator.state.push_graphics_state import PushGraphicsState
from ptext.pdf.canvas.operator.state.set_line_width import SetLineWidth
from ptext.pdf.canvas.operator.text.begin_text import BeginTextObject
from ptext.pdf.canvas.operator.text.end_text import EndTextObject
from ptext.pdf.canvas.operator.text.move_text_position import MoveTextPosition
from ptext.pdf.canvas.operator.text.move_text_position_set_leading import (
    MoveTextPositionSetLeading,
)
from ptext.pdf.canvas.operator.text.move_to_next_line import MoveToNextLine
from ptext.pdf.canvas.operator.text.move_to_next_line_show_text import (
    MoveToNextLineShowText,
)
from ptext.pdf.canvas.operator.text.set_character_spacing import SetCharacterSpacing
from ptext.pdf.canvas.operator.text.set_font_and_size import SetFontAndSize
from ptext.pdf.canvas.operator.text.set_horizontal_text_scaling import (
    SetHorizontalScaling,
)
from ptext.pdf.canvas.operator.text.set_spacing_move_to_next_line_show_text import (
    SetSpacingMoveToNextLineShowText,
)
from ptext.pdf.canvas.operator.text.set_text_leading import SetTextLeading
from ptext.pdf.canvas.operator.text.set_text_matrix import SetTextMatrix
from ptext.pdf.canvas.operator.text.set_text_rendering_mode import (
    SetTextRenderingMode,
)
from ptext.pdf.canvas.operator.text.set_text_rise import SetTextRise
from ptext.pdf.canvas.operator.text.set_word_spacing import SetWordSpacing
from ptext.pdf.canvas.operator.text.show_text import ShowText
from ptext.pdf.canvas.operator.text.show_text_with_glyph_positioning import (
    ShowTextWithGlyphPositioning,
)
from ptext.pdf.canvas.operator.xobject.do import Do

logger = logging.getLogger(__name__)


class Canvas(Dictionary):
    def __init__(self):
        super(Canvas, self).__init__()
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
            # compatibility
            BeginCompatibilitySection(),
            EndCompatibilitySection(),
            # marked content
            BeginMarkedContent(),
            BeginMarkedContentWithPropertyList(),
            EndMarkedContent(),
            # path construction
            AppendCubicBezierCurve1(),
            AppendCubicBezierCurve2(),
            AppendCubicBezierCurve3(),
            AppendLineSegment(),
            BeginSubpath(),
            CloseSubpath(),
            # path painting
            CloseAndStrokePath(),
            StrokePath(),
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
        # compatibility mode
        self.in_compatibility_section = False
        # set initial graphics state
        self.graphics_state = CanvasGraphicsState()
        # canvas tag hierarchy is (oddly enough) not considered to be part of the graphics state
        self.marked_content_stack = []
        # set graphics state stack
        self.graphics_state_stack = []

    def add_listener(self, event_listener: "EventListener") -> "Canvas":  # type: ignore [name-defined]
        """
        This method adds a generic EventListener to this Canvas
        """
        self.listeners.append(event_listener)  # type: ignore [attr-defined]
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
            if not isinstance(obj, CanvasOperatorName):
                operand_stk.append(obj)
                continue

            # process operator
            candidate_ops = [
                x for x in self.canvas_operators if x.get_text() == str(obj)
            ]
            if len(candidate_ops) == 1:
                operator = candidate_ops[0]
                if len(operand_stk) < operator.get_number_of_operands():
                    # if we are in a compatibility section ignore any possible mistake
                    if self.in_compatibility_section:
                        continue
                    raise IllegalGraphicsStateError(
                        message="Unable to execute operator %s. Expected %d arguments, received %d."
                        % (
                            operator.text,
                            operator.get_number_of_operands(),
                            len(operand_stk),
                        )
                    )
                operands: typing.List["CanvasOperator"] = []  # type: ignore [name-defined]
                for _ in range(0, operator.get_number_of_operands()):
                    operands.insert(0, operand_stk.pop(-1))

                # append
                if "Instructions" not in self:
                    self["Instructions"] = List().set_parent(self)  # type: ignore [attr-defined]

                instruction_number = len(self["Instructions"])
                instruction_dictionary = Dictionary()
                instruction_dictionary["Name"] = operator.get_text()
                instruction_dictionary["Args"] = List().set_parent(  # type: ignore [attr-defined]
                    instruction_dictionary
                )

                if len(operands) > 0:
                    for i in range(0, len(operands)):
                        instruction_dictionary["Args"].append(operands[i])
                self["Instructions"].append(instruction_dictionary)

                # debug
                logger.debug(
                    "%d %s %s"
                    % (
                        instruction_number,
                        operator.text,
                        str([str(x) for x in operands]),
                    )
                )

                # invoke
                try:
                    operator.invoke(self, operands)
                except Exception as e:
                    if not self.in_compatibility_section:
                        raise e

            # unknown operator
            if len(candidate_ops) == 0:
                # print("Missing OPERATOR %s" % obj)
                pass

        # return
        return self
