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

# fmt: off
from borb.io.read.tokenize.high_level_tokenizer import HighLevelTokenizer
from borb.io.read.types import AnyPDFType
from borb.io.read.types import CanvasOperatorName
from borb.io.read.types import Dictionary
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator
from borb.pdf.canvas.operator.color.set_cmyk_non_stroking import SetCMYKNonStroking
from borb.pdf.canvas.operator.color.set_cmyk_stroking import SetCMYKStroking
from borb.pdf.canvas.operator.color.set_color_non_stroking import SetColorNonStroking
from borb.pdf.canvas.operator.color.set_color_space_non_stroking import SetColorSpaceNonStroking
from borb.pdf.canvas.operator.color.set_color_space_stroking import SetColorSpaceStroking
from borb.pdf.canvas.operator.color.set_color_stroking import SetColorStroking
from borb.pdf.canvas.operator.color.set_gray_non_stroking import SetGrayNonStroking
from borb.pdf.canvas.operator.color.set_gray_stroking import SetGrayStroking
from borb.pdf.canvas.operator.color.set_rgb_non_stroking import SetRGBNonStroking
from borb.pdf.canvas.operator.color.set_rgb_stroking import SetRGBStroking
from borb.pdf.canvas.operator.compatibility.begin_compatibility_section import BeginCompatibilitySection
from borb.pdf.canvas.operator.compatibility.end_compatibility_section import EndCompatibilitySection
from borb.pdf.canvas.operator.marked_content.begin_marked_content import BeginMarkedContent
from borb.pdf.canvas.operator.marked_content.begin_marked_content_with_property_list import \
    BeginMarkedContentWithPropertyList
from borb.pdf.canvas.operator.marked_content.end_marked_content import EndMarkedContent
from borb.pdf.canvas.operator.path_construction.append_cubic_bezier import AppendCubicBezierCurve1
from borb.pdf.canvas.operator.path_construction.append_cubic_bezier import AppendCubicBezierCurve2
from borb.pdf.canvas.operator.path_construction.append_cubic_bezier import AppendCubicBezierCurve3
from borb.pdf.canvas.operator.path_construction.append_line_segment import AppendLineSegment
from borb.pdf.canvas.operator.path_construction.append_rectangle import AppendRectangle
from borb.pdf.canvas.operator.path_construction.begin_subpath import BeginSubpath
from borb.pdf.canvas.operator.path_construction.close_subpath import CloseSubpath
from borb.pdf.canvas.operator.path_painting.close_and_stroke_path import CloseAndStrokePath
from borb.pdf.canvas.operator.path_painting.stroke_path import StrokePath
from borb.pdf.canvas.operator.state.modify_transformation_matrix import ModifyTransformationMatrix
from borb.pdf.canvas.operator.state.pop_graphics_state import PopGraphicsState
from borb.pdf.canvas.operator.state.push_graphics_state import PushGraphicsState
from borb.pdf.canvas.operator.state.set_line_width import SetLineWidth
from borb.pdf.canvas.operator.text.begin_text import BeginTextObject
from borb.pdf.canvas.operator.text.end_text import EndTextObject
from borb.pdf.canvas.operator.text.move_text_position import MoveTextPosition
from borb.pdf.canvas.operator.text.move_text_position_set_leading import MoveTextPositionSetLeading
from borb.pdf.canvas.operator.text.move_to_next_line import MoveToNextLine
from borb.pdf.canvas.operator.text.move_to_next_line_show_text import MoveToNextLineShowText
from borb.pdf.canvas.operator.text.set_character_spacing import SetCharacterSpacing
from borb.pdf.canvas.operator.text.set_font_and_size import SetFontAndSize
from borb.pdf.canvas.operator.text.set_horizontal_text_scaling import SetHorizontalScaling
from borb.pdf.canvas.operator.text.set_spacing_move_to_next_line_show_text import SetSpacingMoveToNextLineShowText
from borb.pdf.canvas.operator.text.set_text_leading import SetTextLeading
from borb.pdf.canvas.operator.text.set_text_matrix import SetTextMatrix
from borb.pdf.canvas.operator.text.set_text_rendering_mode import SetTextRenderingMode
from borb.pdf.canvas.operator.text.set_text_rise import SetTextRise
from borb.pdf.canvas.operator.text.set_word_spacing import SetWordSpacing
from borb.pdf.canvas.operator.text.show_text import ShowText
from borb.pdf.canvas.operator.text.show_text_with_glyph_positioning import ShowTextWithGlyphPositioning
from borb.pdf.canvas.operator.xobject.do import Do

# fmt: on

logger = logging.getLogger(__name__)


class CanvasStreamProcessor:
    """
    This class processes a given bytes stream of instructions on a Canvas and Page.
    By abstracting this logic into one class, we can easily change the resources it uses
    (which is needed to handle /Form XObjects).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: "Page",  # type: ignore[name-defined]
        canvas: "Canvas",  # type: ignore[name-defined]
        resource_dictionaries: typing.List[Dictionary] = [],
    ):
        self._page: "Page" = page  # type: ignore[name-defined]
        self._canvas: "Canvas" = canvas  # type: ignore[name-defined]
        self._resource_dictionaries: typing.List[Dictionary] = resource_dictionaries

        # initialize operators
        self._canvas_operators: typing.Dict[str, CanvasOperator] = {
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
                AppendRectangle(),
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

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def create_child_canvas_stream_processor(
        self, resource_dictionaries: typing.List[Dictionary]
    ) -> "CanvasStreamProcessor":
        """
        This function creates a (child) CanvasStreamProcessor.
        The child processor will have the same resource dictionaries (fonts, images, etc) as its parent (self),
        but can optionally add more resources (such as when a content stream is defined in an XObject).
        """
        return CanvasStreamProcessor(
            self._page,
            self._canvas,
            self._resource_dictionaries + resource_dictionaries,
        )

    def get_canvas(self) -> "Canvas":  # type: ignore[name-defined]
        """
        This function returns the Canvas on which this CanvasStreamProcessor is active.
        """
        return self._canvas

    def get_operator(self, name: str) -> typing.Optional["CanvasOperator"]:  # type: ignore[name-defined]
        """
        This function returns the CanvasOperator matching the given operator-name.
        This allows operator re-use between different implementations of Canvas
        """
        return self._canvas_operators.get(name)

    def get_page(self) -> "Page":  # type: ignore[name-defined]
        """
        This function returns the Page on which this CanvasStreamProcessor is active.
        """
        return self._page

    def get_resource(
        self, resource_type_name: str, name: str
    ) -> typing.Optional[typing.Any]:
        """
        This functions looks up a resource (e.g. Font, Image, XObject) in the given resource hierarchy.
        e.g. for a content stream in an XObject, first its own /Resources entry is tried, and lastly the Page resources.
        """
        # check external Resources
        for i in range(len(self._resource_dictionaries) - 1, -1, -1):
            rd = self._resource_dictionaries[i]
            if (resource_type_name in rd) and (name in rd[resource_type_name]):
                return rd[resource_type_name][name]
        # check Page[Resources]
        if (
            resource_type_name in self._page["Resources"]
            and name in self._page["Resources"][resource_type_name]
        ):
            return self._page["Resources"][resource_type_name][name]
        return None

    def read(
        self,
        io_source: typing.Union[io.BytesIO, io.IOBase],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore[name-defined]
    ) -> "CanvasStreamProcessor":  # type: ignore[name-defined]
        """
        This method reads a byte stream of canvas operators, and processes them, returning this Canvas afterwards
        """
        io_source.seek(0, os.SEEK_END)
        length = io_source.tell()
        io_source.seek(0)

        canvas_tokenizer = HighLevelTokenizer(io_source)

        # process content
        operand_stk: typing.List[typing.Optional[AnyPDFType]] = []
        instruction_number: int = 0
        time_per_operator: typing.Dict[str, float] = {}
        calls_per_operator: typing.Dict[str, int] = {}
        while canvas_tokenizer.tell() != length:
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
            operator = self._canvas_operators.get(str(obj), None)
            if operator is None:
                logger.debug("Missing operator %s" % obj)
                continue

            if not self._canvas.in_compatibility_section:
                assert len(operand_stk) >= operator.get_number_of_operands()
            operands: typing.List[AnyPDFType] = []  # type: ignore[name-defined]
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
                operator.invoke(self, operands, event_listeners)
                delta = time.time() - delta
                time_per_operator[on] += delta

            except Exception as e:
                if not self._canvas.in_compatibility_section:
                    raise e

        # return
        return self
