#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains all classes needed to apply redaction on a Page in a PDF Document
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.read.types import HexadecimalString
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class CopyCommandOperator(CanvasOperator):
    """
    This CanvasOperator copies an existing operator and writes its bytes to the content stream of the canvas
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, operator_to_copy: CanvasOperator):
        super().__init__("", 0)
        self._operator_to_copy = operator_to_copy

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_number_of_operands(self) -> int:
        """
        Return the number of operands for this CanvasOperator
        """
        return self._operator_to_copy.get_number_of_operands()

    def get_text(self) -> str:
        """
        Return the str that invokes this CanvasOperator
        """
        return self._operator_to_copy.get_text()

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore[name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore[name-defined]
    ) -> None:
        """
        Invokes this CanvasOperator
        """

        # execute command
        self._operator_to_copy.invoke(canvas_stream_processor, operands)

        # copy command in content stream
        canvas = canvas_stream_processor.get_canvas()

        # copy operand string
        op_str: typing.List[str] = []
        for op in operands:
            if isinstance(op, Decimal):
                op_str.append(str(op))
                continue
            if isinstance(op, HexadecimalString):
                op_str.append("<" + str(op) + ">")
                continue
            if isinstance(op, String):
                op_str.append("(" + str(op) + ")")
                continue
            if isinstance(op, Name):
                op_str.append("/" + str(op))
                continue

        assert isinstance(canvas_stream_processor, RedactedCanvasStreamProcessor)
        canvas_stream_processor.append_to_redacted_content(
            ("\n" + "".join([(s + " ") for s in op_str]) + self.get_text()).encode(
                "latin1"
            )
        )


class ShowTextMod(CanvasOperator):
    """
    Show a text string.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("Tj", 1)

    #
    # PRIVATE
    #

    def _show_text_unmodified(
        self, canvas_stream_processor: "CanvasStreamProcessor", s: String
    ) -> None:
        assert isinstance(canvas_stream_processor, RedactedCanvasStreamProcessor)
        if isinstance(s, HexadecimalString):
            canvas_stream_processor.append_to_redacted_content(
                ("\n<" + str(s) + "> Tj").encode("latin1")
            )
            return
        if isinstance(s, String):
            canvas_stream_processor.append_to_redacted_content(
                ("\n(" + str(s) + ") Tj").encode("latin1")
            )

    def _write_chunk_of_text(
        self, canvas_stream_processor: "CanvasStreamProcessor", s: str, f: "Font"  # type: ignore[name-defined]
    ):
        from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText

        assert isinstance(canvas_stream_processor, RedactedCanvasStreamProcessor)
        canvas_stream_processor.append_to_redacted_content(b"\n")
        canvas_stream_processor.append_to_redacted_content(
            ChunkOfText(s, f)._write_text_bytes().encode("latin1")
        )

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore[name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore[name-defined]
    ) -> None:
        """
        Invokes this CanvasOperator
        """

        assert isinstance(operands[0], String)
        assert isinstance(canvas_stream_processor, RedactedCanvasStreamProcessor)

        # handle Font being a Name (optimization)
        canvas = canvas_stream_processor.get_canvas()
        assert canvas.graphics_state.font is not None
        font_name: typing.Optional[Name] = None
        if isinstance(canvas.graphics_state.font, Name):
            font_name = canvas.graphics_state.font
            canvas.graphics_state.font = canvas_stream_processor.get_resource(
                "Font", str(canvas.graphics_state.font)
            )

        # get bounding box
        bounding_box: typing.Optional[Rectangle] = ChunkOfTextRenderEvent(
            canvas.graphics_state, operands[0]
        ).get_previous_layout_box()
        assert bounding_box is not None

        # write every glyph
        jump_from_redacted: bool = False
        for evt in ChunkOfTextRenderEvent(
            canvas.graphics_state, operands[0]
        ).split_on_glyphs():
            evt_previous_layout_box: typing.Optional[
                Rectangle
            ] = evt.get_previous_layout_box()
            assert evt_previous_layout_box is not None
            letter_should_be_redacted: bool = any(
                [
                    x.intersects(evt_previous_layout_box)
                    for x in canvas_stream_processor._redacted_rectangles  # type: ignore[attr-defined]
                ]
            )
            graphics_state = canvas_stream_processor.get_canvas().graphics_state
            w: Decimal = evt_previous_layout_box.get_width()

            if letter_should_be_redacted:
                # update text_matrix
                graphics_state.text_matrix[2][0] += w
                # this flag is useful to ensure we only write the Tm command once
                # it could not hurt to write it several times, but it would be a wasted effort
                jump_from_redacted = True
            else:
                # write position command if needed
                if jump_from_redacted:
                    canvas_stream_processor._redacted_content += "\n%f %f %f %f %f %f Tm" % (  # type: ignore[attr-defined]
                        graphics_state.text_matrix[0][0],
                        graphics_state.text_matrix[0][1],
                        graphics_state.text_matrix[1][0],
                        graphics_state.text_matrix[1][1],
                        graphics_state.text_matrix[2][0],
                        graphics_state.text_matrix[2][1],
                    )
                    jump_from_redacted = False
                # write command
                self._write_chunk_of_text(
                    canvas_stream_processor, evt.get_text(), evt.get_font()
                )
                # update text_matrix
                graphics_state.text_matrix[2][0] += w

        # restore
        if font_name is not None:
            canvas.graphics_state.font = font_name


class ShowTextWithGlyphPositioningMod(CanvasOperator):
    """
    This operator represents a modified version of the TJ operator
    Instead of always rendering the text, it takes into account the location
    at which the text is to be rendered, if the text falls in one of the redacted areas
    it will not render the text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("TJ", 1)

    #
    # PRIVATE
    #

    def _write_chunk_of_text(
        self, canvas_stream_processor: "CanvasStreamProcessor", s: str, f: "Font"  # type: ignore[name-defined]
    ):
        from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText

        assert isinstance(canvas_stream_processor, RedactedCanvasStreamProcessor)
        canvas_stream_processor.append_to_redacted_content(b"\n")
        canvas_stream_processor.append_to_redacted_content(
            ChunkOfText(s, f)._write_text_bytes().encode("latin1")
        )

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore[name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore[name-defined]
    ) -> None:
        """
        Invoke the TJ operator
        """

        # handle Font being a Name (optimization)
        canvas = canvas_stream_processor.get_canvas()
        assert canvas.graphics_state.font is not None
        font_name: typing.Optional[Name] = None
        if isinstance(canvas.graphics_state.font, Name):
            font_name = canvas.graphics_state.font
            canvas.graphics_state.font = canvas_stream_processor.get_resource(
                "Font", str(canvas.graphics_state.font)
            )

        assert isinstance(operands[0], List)
        for i in range(0, len(operands[0])):
            obj = operands[0][i]

            # display string
            if isinstance(obj, String):
                assert isinstance(obj, String)

                # write every glyph
                jump_from_redacted: bool = False
                for evt in ChunkOfTextRenderEvent(
                    canvas.graphics_state, obj
                ).split_on_glyphs():
                    letter_should_be_redacted: bool = any(
                        [
                            x.intersects(evt.get_previous_layout_box())
                            for x in canvas_stream_processor._redacted_rectangles  # type: ignore[attr-defined]
                        ]
                    )
                    graphics_state = canvas_stream_processor.get_canvas().graphics_state
                    event_bounding_box: typing.Optional[
                        Rectangle
                    ] = evt.get_previous_layout_box()
                    assert event_bounding_box is not None
                    w: Decimal = event_bounding_box.get_width()

                    if letter_should_be_redacted:
                        # update text_matrix
                        graphics_state.text_matrix[2][0] += w
                        # this flag is useful to ensure we only write the Tm command once
                        # it could not hurt to write it several times, but it would be a wasted effort
                        jump_from_redacted = True
                    else:
                        # write position command if needed
                        if jump_from_redacted:
                            canvas_stream_processor._redacted_content += "\n%f %f %f %f %f %f Tm" % (  # type: ignore[attr-defined]
                                graphics_state.text_matrix[0][0],
                                graphics_state.text_matrix[0][1],
                                graphics_state.text_matrix[1][0],
                                graphics_state.text_matrix[1][1],
                                graphics_state.text_matrix[2][0],
                                graphics_state.text_matrix[2][1],
                            )
                            jump_from_redacted = False
                        # write command
                        self._write_chunk_of_text(
                            canvas_stream_processor, evt.get_text(), evt.get_font()
                        )
                        # update text_matrix
                        graphics_state.text_matrix[2][0] += w

            # process Decimal objects
            if isinstance(obj, Decimal):
                # calculate the adjustment
                assert isinstance(obj, Decimal)
                gs = canvas.graphics_state
                adjust_unscaled = obj
                adjust_scaled = (
                    -adjust_unscaled
                    * Decimal(0.001)
                    * gs.font_size
                    * (gs.horizontal_scaling / 100)
                )
                gs.text_matrix[2][0] -= adjust_scaled

                # write operator
                assert isinstance(
                    canvas_stream_processor, RedactedCanvasStreamProcessor
                )
                canvas_stream_processor.append_to_redacted_content(
                    b"\n%f %f %f %f %f %f Tm"
                    % (  # type: ignore [attr-defined]
                        gs.text_matrix[0][0],
                        gs.text_matrix[0][1],
                        gs.text_matrix[1][0],
                        gs.text_matrix[1][1],
                        gs.text_matrix[2][0],
                        gs.text_matrix[2][1],
                    )
                )

        # restore
        if font_name is not None:
            canvas.graphics_state.font = font_name


class RedactedCanvasStreamProcessor(CanvasStreamProcessor):
    """
    In computer science and visualization, a canvas is a container that holds various drawing elements
    (lines, shapes, text, frames containing other elements, etc.).
    It takes its name from the canvas used in visual arts.
    This implementation of Canvas automatically handles redaction (removal of content).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: "Page",  # type: ignore[name-defined]
        canvas: "Canvas",  # type: ignore[name-defined]
        redacted_rectangles: typing.List[Rectangle],
    ):
        super(RedactedCanvasStreamProcessor, self).__init__(page, canvas, [])

        # redacted content
        self._redacted_content: str = ""

        # redacted rectangle
        self._redacted_rectangles = redacted_rectangles

        # every operator is replaced by the CopyCommandOperator
        for name, operator in self._canvas_operators.items():
            self._canvas_operators[name] = CopyCommandOperator(
                self._canvas_operators[name]
            )

        # Tj
        self._canvas_operators["Tj"] = ShowTextMod()

        # TJ
        self._canvas_operators["TJ"] = ShowTextWithGlyphPositioningMod()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_redacted_content(self) -> bytes:
        """
        This function returns the redacted content of this implementation of CanvasStreamProcessor
        """
        return self._redacted_content.encode("latin1")

    def set_redacted_content(self, bts: bytes) -> "RedactedCanvasStreamProcessor":
        """
        This function sets the (redacted) content of this RedactedCanvasStreamProcessor
        :param bts:     the content to be set
        :return:        self
        """
        self._redacted_content = bts.decode("latin1")
        return self

    def append_to_redacted_content(self, bts: bytes) -> "RedactedCanvasStreamProcessor":
        """
        This function appends the given bytes to the (redacted) content of this RedactedCanvasStreamProcessor
        :param bts:     the bytes to append
        :return:        self
        """
        self._redacted_content += bts.decode("latin1")
        return self
