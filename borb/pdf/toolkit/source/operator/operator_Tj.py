#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Tj' operator: Show a text string.

This operator displays a text string at the current position in the user space,
using the font and size specified in the current text state. The string is shown
in the current text rendering mode and color.

The operand for this operator is a string, which represents the text to be displayed.
The operator updates the current position after the string is shown based on the
current text rendering mode and the text matrix.

Note:
    - The text is shown exactly as specified, including spaces and special characters.
    - After the text is shown, the current position is updated according to the current
      text matrix and text rendering mode.
    - This operator does not automatically add any additional spacing between characters
      beyond what is defined by the current text state.
"""
import typing

from borb.pdf.font.composite_font.composite_font import CompositeFont
from borb.pdf.font.simple_font.simple_font import SimpleFont
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, hexstr
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTj(Operator):
    """
    The 'Tj' operator: Show a text string.

    This operator displays a text string at the current position in the user space,
    using the font and size specified in the current text state. The string is shown
    in the current text rendering mode and color.

    The operand for this operator is a string, which represents the text to be displayed.
    The operator updates the current position after the string is shown based on the
    current text rendering mode and the text matrix.

    Note:
        - The text is shown exactly as specified, including spaces and special characters.
        - After the text is shown, the current position is updated according to the current
          text matrix and text rendering mode.
        - This operator does not automatically add any additional spacing between characters
          beyond what is defined by the current text state.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __cross(
        m: typing.List[typing.List[float]], v: typing.List[float]
    ) -> typing.List[float]:
        x: float = v[0]
        y: float = v[1]
        z: float = v[2]
        x2 = x * m[0][0] + y * m[1][0] + z * m[2][0]
        y2 = x * m[0][1] + y * m[1][1] + z * m[2][1]
        z2 = x * m[0][2] + y * m[1][2] + z * m[2][2]
        return [x2, y2, z2]

    @staticmethod
    def __mul(
        m0: typing.List[typing.List[float]], m1: typing.List[typing.List[float]]
    ) -> typing.List[typing.List[float]]:
        assert len(m0) == 3 and all(
            [len(r) == 3 for r in m0]
        ), "m0 must be a 3 by 3 matrix"
        assert len(m1) == 3 and all(
            [len(r) == 3 for r in m1]
        ), "m1 must be a 3 by 3 matrix"
        return [
            [
                m0[0][0] * m1[0][0] + m0[0][1] * m1[1][0] + m0[0][2] * m1[2][0],
                m0[0][0] * m1[0][1] + m0[0][1] * m1[1][1] + m0[0][2] * m1[2][1],
                m0[0][0] * m1[0][2] + m0[0][1] * m1[1][2] + m0[0][2] * m1[2][2],
            ],
            [
                m0[1][0] * m1[0][0] + m0[1][1] * m1[1][0] + m0[1][2] * m1[2][0],
                m0[1][0] * m1[0][1] + m0[1][1] * m1[1][1] + m0[1][2] * m1[2][1],
                m0[1][0] * m1[0][2] + m0[1][1] * m1[1][2] + m0[1][2] * m1[2][2],
            ],
            [
                m0[2][0] * m1[0][0] + m0[2][1] * m1[1][0] + m0[2][2] * m1[2][0],
                m0[2][0] * m1[0][1] + m0[2][1] * m1[1][1] + m0[2][2] * m1[2][1],
                m0[2][0] * m1[0][2] + m0[2][1] * m1[1][2] + m0[2][2] * m1[2][2],
            ],
        ]

    @staticmethod
    def __unescape_special_chars_in_ascii_mode(s: str) -> str:
        s2: str = ""
        i: int = 0
        while i < len(s):
            if s[i:].startswith("\\n"):
                s2 += "\n"
                i += 2
                continue
            if s[i:].startswith("\\r"):
                s2 += "\r"
                i += 2
                continue
            if s[i:].startswith("\\t"):
                s2 += "\t"
                i += 2
                continue
            if s[i:].startswith("\\b"):
                s2 += "\b"
                i += 2
                continue
            if s[i:].startswith("\\f"):
                s2 += "\f"
                i += 2
                continue
            if s[i:].startswith("\\("):
                s2 += "("
                i += 2
                continue
            if s[i:].startswith("\\)"):
                s2 += ")"
                i += 2
                continue

            # Handle octal escape sequences (\000 - \377)
            if s[i] == "\\" and i + 1 < len(s) and s[i + 1] in "01234567":
                j = i + 1
                octal_digits = ""
                while j < len(s) and len(octal_digits) < 3 and s[j] in "01234567":
                    octal_digits += s[j]
                    j += 1
                s2 += chr(int(octal_digits, 8))  # Convert octal to character
                i = j  # Move past the octal sequence
                continue

            # default
            s2 += s[i]
            i += 1

        # return
        return s2

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        assert isinstance(operands[0], str)

        # Determine text being rendered
        text_being_rendered: typing.Optional[str] = None
        if isinstance(source.font, SimpleFont):
            unescaped_operand: bytes = b""
            if isinstance(operands[0], hexstr):
                unescaped_operand = operands[0].to_bytes()
            if isinstance(operands[0], str) and not isinstance(operands[0], hexstr):
                # fmt: off
                unescaped_operand = OperatorTj.__unescape_special_chars_in_ascii_mode(operands[0]).encode("latin-1")
                # fmt: on
            text_being_rendered = "".join(
                [source.font.get_character(c) for c in unescaped_operand]
            )

        if isinstance(source.font, CompositeFont):
            if isinstance(operands[0], hexstr):
                i: int = 0
                hexstr_as_bytes: bytes = operands[0].to_bytes()
                while i < len(hexstr_as_bytes):
                    # IF a two byte code is present to map the next two (hex) bytes to a char
                    # THEN use this two byte code
                    if i < len(hexstr_as_bytes) - 1:
                        two_byte_code: int = (
                            hexstr_as_bytes[i] * 256 + hexstr_as_bytes[i + 1]
                        )
                        if source.font.get_character(two_byte_code) not in ["�", None]:  # type: ignore[attr-defined]
                            text_being_rendered = (text_being_rendered or "") + source.font.get_character(  # type: ignore[attr-defined, operator]
                                two_byte_code
                            )
                            i += 2
                            continue

                    # default (single byte code)
                    text_being_rendered = (text_being_rendered or "") + source.font.get_character(hexstr_as_bytes[i])  # type: ignore[attr-defined, operator]
                    i += 1

            if isinstance(operands[0], str) and not isinstance(operands[0], hexstr):
                # fmt: off
                unescaped_operand = OperatorTj.__unescape_special_chars_in_ascii_mode(operands[0]).encode("latin-1")
                text_being_rendered = "".join([source.font.get_character(c) for c in unescaped_operand])
                # fmt: on

        assert text_being_rendered is not None

        # Determine width
        width: float = 0.0
        if isinstance(source.font, SimpleFont):
            assert text_being_rendered is not None
            width = (
                source.font.get_width(
                    font_size=1000,
                    text=text_being_rendered,
                    character_spacing=source.character_spacing,
                    word_spacing=source.word_spacing,
                )
                / 1000
            )

        # Determine x,y
        mtx = OperatorTj.__mul(
            source.text_matrix,
            source.transformation_matrix,
        )
        mtx[0][0] *= source.font_size
        mtx[1][1] *= source.font_size
        p0 = OperatorTj.__cross(mtx, [0, source.text_rise, 1])
        p1 = OperatorTj.__cross(
            mtx,
            [width, source.text_rise, 1],
        )
        p2 = OperatorTj.__cross(mtx, [0, source.text_rise + source.font_size, 1])
        x = round(min([p0[0], p1[0]]))
        y = round(min([p0[1], p1[1]]))
        absolute_width: int = round(abs(p0[0] - p1[0]))
        absolute_height = round(abs(p2[1] - p1[1]))

        # Trigger event
        source.text(
            s=text_being_rendered,
            x=x,
            y=y,
            width=absolute_width,
            height=absolute_height,
            font=source.font,
            font_color=source.stroke_color,
            font_size=source.font_size,
        )

        # Update text rendering location
        # This code only takes into account the text-matrix
        p0 = OperatorTj.__cross(source.text_matrix, [0, 1, 1])
        p1 = OperatorTj.__cross(
            source.text_matrix,
            [width, 1, 1],
        )
        width_in_text_matrix_space: int = round(abs(p0[0] - p1[0]))
        source.text_matrix[2][0] += absolute_width

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Tj"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
