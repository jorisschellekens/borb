#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains all classes needed to apply redaction on a Page in a PDF Document
"""
import typing
from decimal import Decimal

from ptext.io.read.types import AnyPDFType, List, String
from ptext.pdf.canvas.canvas import Canvas
from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class CopyCommandOperator(CanvasOperator):
    """
    This CanvasOperator copies an existing operator and writes its bytes to the content stream of the canvas
    """

    def __init__(self, operator_to_copy: CanvasOperator):
        super().__init__("", 0)
        self.operator_to_copy = operator_to_copy

    def get_text(self) -> str:
        """
        Return the str that invokes this CanvasOperator
        """
        return self.operator_to_copy.get_text()

    def get_number_of_operands(self) -> int:
        """
        Return the number of operands for this CanvasOperator
        """
        return self.operator_to_copy.get_number_of_operands()

    def invoke(self, canvas: "Canvas", operands: typing.List[AnyPDFType] = []) -> None:
        """
        Invokes this CanvasOperator
        """

        # execute command
        self.operator_to_copy.invoke(canvas, operands)
        # copy command in content stream
        assert isinstance(canvas, RedactedCanvas)
        canvas.content_stream += "\n" + self.get_text()


#
# special copies of text-rendering operators
#


class ShowTextMod(CanvasOperator):
    """
    Show a text string.
    """

    def __init__(self):
        super().__init__("Tj", 1)

    def invoke(self, canvas: "Canvas", operands: typing.List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invokes this CanvasOperator
        """

        assert isinstance(operands[0], String)

        # get bounding box
        bounding_box: typing.Optional[Rectangle] = ChunkOfTextRenderEvent(
            canvas.graphics_state, operands[0]
        ).get_bounding_box()
        assert bounding_box is not None

        # check intersection with redacted rectangles from canvas
        assert isinstance(canvas, RedactedCanvas)
        should_be_redacted = any(
            [x.intersects(bounding_box) for x in canvas.redacted_rectangles]
        )

        if should_be_redacted:
            # update text-position matrices
            pass
        else:
            # write command
            canvas.content_stream += "\n" + str(operands[0]) + " Tj"


class ShowTextWithGlyphPositioningMod(CanvasOperator):
    """
    This operator represents a modified version of the TJ operator
    In stead of always rendering the text, it takes into account the location
    at which the text is to be rendered, if the text falls in one of the redacted areas
    it will not render the text.
    """

    def __init__(self):
        super().__init__("TJ", 1)

    def invoke(self, canvas: "Canvas", operands: typing.List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the TJ operator
        """

        assert isinstance(operands[0], List)
        for i in range(0, len(operands[0])):
            obj = operands[0][i]

            # display string
            if isinstance(obj, String):
                assert isinstance(obj, String)

                # get bounding box
                evt = ChunkOfTextRenderEvent(canvas.graphics_state, obj)
                bounding_box: typing.Optional[Rectangle] = evt.get_bounding_box()
                assert bounding_box is not None

                # check intersection with redacted rectangles from canvas
                assert isinstance(canvas, RedactedCanvas)
                should_be_redacted = any(
                    [x.intersects(bounding_box) for x in canvas.redacted_rectangles]
                )

                if should_be_redacted:
                    # update text-position matrices
                    pass
                else:
                    # write content
                    pass

                # update text rendering location
                canvas.graphics_state.text_matrix[2][0] += evt.get_baseline().width
                continue

            # adjust
            if isinstance(obj, Decimal):
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


#
# redacted version of Canvas
#


class RedactedCanvas(Canvas):
    """
    In computer science and visualization, a canvas is a container that holds various drawing elements
    (lines, shapes, text, frames containing other elements, etc.).
    It takes its name from the canvas used in visual arts.
    This implementation of Canvas automatically handles redaction (removal of content).
    """

    def __init__(self, redacted_rectangles: typing.List[Rectangle]):
        super(RedactedCanvas, self).__init__()

        # redacted rectangle
        self.redacted_rectangles = redacted_rectangles

        # content stream being rebuilt
        self.content_stream = ""

        # every operator is replaced by the CopyCommandOperator
        for name, operator in self.canvas_operators.items():
            self.canvas_operators[name] = CopyCommandOperator(
                self.canvas_operators[name]
            )

        # Tj
        self.canvas_operators["Tj"] = ShowTextMod()

        # TJ
        self.canvas_operators["TJ"] = ShowTextWithGlyphPositioningMod()
