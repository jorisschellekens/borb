#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This class processes a given bytes stream of instructions on a Canvas and Page.
    By abstracting this logic into one class, we can easily change the resources it uses
    (which is needed to handle /Form XObjects).
"""
import io
import logging
import os
import time
import typing

from ptext.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from ptext.io.read.types import AnyPDFType, CanvasOperatorName, Dictionary
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.color.set_cmyk_non_stroking import SetCMYKNonStroking
from ptext.pdf.canvas.operator.color.set_cmyk_stroking import SetCMYKStroking
from ptext.pdf.canvas.operator.color.set_color_non_stroking import SetColorNonStroking
from ptext.pdf.canvas.operator.color.set_color_space_non_stroking import (
    SetColorSpaceNonStroking,
)
from ptext.pdf.canvas.operator.color.set_color_space_stroking import (
    SetColorSpaceStroking,
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
from ptext.pdf.canvas.operator.marked_content.end_marked_content import EndMarkedContent
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
from ptext.pdf.canvas.operator.text.set_text_rendering_mode import SetTextRenderingMode
from ptext.pdf.canvas.operator.text.set_text_rise import SetTextRise
from ptext.pdf.canvas.operator.text.set_word_spacing import SetWordSpacing
from ptext.pdf.canvas.operator.text.show_text import ShowText
from ptext.pdf.canvas.operator.text.show_text_with_glyph_positioning import (
    ShowTextWithGlyphPositioning,
)
from ptext.pdf.canvas.operator.xobject.do import Do

logger = logging.getLogger(__name__)


class CanvasStreamProcessor:
    """
    This class processes a given bytes stream of instructions on a Canvas and Page.
    By abstracting this logic into one class, we can easily change the resources it uses
    (which is needed to handle /Form XObjects).
    """

    def __init__(
        self,
        page: "Page",  # type: ignore[name-defined]
        canvas: "Canvas",  # type: ignore[name-defined]
        resource_dictionaries: typing.List[Dictionary] = [],
    ):
        self.page: "Page" = page  # type: ignore[name-defined]
        self.canvas: "Canvas" = canvas  # type: ignore[name-defined]
        self.resource_dictionaries: typing.List[Dictionary] = resource_dictionaries

        # initialize operators
        self.canvas_operators: typing.Dict[str, CanvasOperator] = {
            x.get_text(): x
            for x in [
                # color
                SetCMYKNonStroking(),
                SetCMYKStroking(),
                SetColorNonStroking(self),
                SetColorStroking(self),
                SetGrayNonStroking(),
                SetGrayStroking(),
                SetRGBNonStroking(),
                SetRGBStroking(),
                SetColorSpaceStroking(),
                SetColorSpaceNonStroking(),
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
        }

    def create_child_canvas_stream_processor(
        self, resource_dictionaries: typing.List[Dictionary]
    ) -> "CanvasStreamProcessor":
        """
        This function creates a (child) CanvasStreamProcessor.
        The child processor will have the same resource dictionaries (fonts, images, etc) as its parent (self),
        but can optionally add more resources (such as when a content stream is defined in an XObject).
        """
        return CanvasStreamProcessor(
            self.page, self.canvas, self.resource_dictionaries + resource_dictionaries
        )

    def get_operator(self, name: str) -> typing.Optional["CanvasOperator"]:  # type: ignore [name-defined]
        """
        This function returns the CanvasOperator matching the given operator-name.
        This allows operator re-use between different implementations of Canvas
        """
        return self.canvas_operators.get(name)

    def get_page(self) -> "Page":  # type: ignore[name-defined]
        """
        This function returns the Page on which this CanvasStreamProcessor is active.
        """
        return self.page

    def get_canvas(self) -> "Canvas":  # type: ignore[name-defined]
        """
        This function returns the Canvas on which this CanvasStreamProcessor is active.
        """
        return self.canvas

    def get_resource(
        self, resource_type_name: str, name: str
    ) -> typing.Optional[typing.Any]:
        """
        This functions looks up a resource (e.g. Font, Image, XObject) in the given resource hierarchy.
        e.g. for a content stream in an XObject, first its own /Resources entry is tried, and lastly the Page resources.
        """
        # check external Resources
        for i in range(0, len(self.resource_dictionaries)):
            i = len(self.resource_dictionaries) - i - 1
            rd = self.resource_dictionaries[i]
            if (resource_type_name in rd) and (name in rd[resource_type_name]):
                return rd[resource_type_name][name]
        # check Page[Resources]
        if (
            resource_type_name in self.page["Resources"]
            and name in self.page["Resources"][resource_type_name]
        ):
            return self.page["Resources"][resource_type_name][name]
        return None

    def read(
        self, io_source: typing.Union[io.BytesIO, io.IOBase]
    ) -> "CanvasStreamProcessor":
        """
        This method reads a byte stream of canvas operators, and processes them, returning this Canvas afterwards
        """
        io_source.seek(0, os.SEEK_END)
        length = io_source.tell()
        io_source.seek(0)

        canvas_tokenizer = HighLevelTokenizer(io_source)

        # process content
        operand_stk = []
        instruction_number: int = 0
        time_per_operator: typing.Dict[str, float] = {}
        calls_per_operator: typing.Dict[str, int] = {}
        while canvas_tokenizer.tell() != length:

            # print("<canvas pos='%d' length='%d' percentage='%d'/>" % ( canvas_tokenizer.tell(), length, int(canvas_tokenizer.tell() * 100 / length)))

            # attempt to read object
            tell_before: int = canvas_tokenizer.tell()
            obj = canvas_tokenizer.read_object()
            tell_after: int = canvas_tokenizer.tell()
            if obj is None and tell_before == tell_after:
                break

            # push argument onto stack
            if not isinstance(obj, CanvasOperatorName):
                operand_stk.append(obj)
                continue

            # process operator
            instruction_number += 1
            operator = self.canvas_operators.get(str(obj), None)
            if operator is None:
                logger.debug("Missing operator %s" % obj)
                continue

            if not self.canvas.in_compatibility_section:
                assert len(operand_stk) >= operator.get_number_of_operands()
            operands: typing.List[AnyPDFType] = []  # type: ignore [name-defined]
            for _ in range(0, operator.get_number_of_operands()):
                operands.insert(0, operand_stk.pop(-1))

            # invoke
            try:
                on: str = operator.get_text()
                if on not in time_per_operator:
                    time_per_operator[on] = 0
                if on not in calls_per_operator:
                    calls_per_operator[on] = 1
                else:
                    calls_per_operator[on] += 1
                delta: float = time.time()
                operator.invoke(self, operands)
                delta = time.time() - delta
                time_per_operator[on] += delta

            except Exception as e:
                if not self.canvas.in_compatibility_section:
                    raise e

        # return
        return self
