#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a block of preformatted code.

The `CodeSnippet` class is used to display a section of code within a document
or layout. It preserves the original formatting, including indentation, line
breaks, and spacing, making it suitable for presenting code snippets or other
preformatted text.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hex_color import HexColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.line_art import LineArt
from borb.pdf.layout_element.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.page import Page


class CodeSnippet(LayoutElement):
    """
    Represents a block of preformatted code.

    The `CodeSnippet` class is used to display a section of code within a document
    or layout. It preserves the original formatting, including indentation, line
    breaks, and spacing, making it suitable for presenting code snippets or other
    preformatted text.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        code: str,
        background_color: typing.Optional[Color] = X11Color.BLACK,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_size: int = 12,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        remove_common_indent: bool = True,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a CodeSnippet object representing a block of code in the document.

        This constructor allows users to create a styled code snippet, including
        customization options for appearance such as background color, border, and alignment.

        :param code: The code to be displayed in the snippet.
        :param background_color: The background color of the code snippet (default is black).
        :param border_color: The color of the border around the snippet (default is None).
        :param border_dash_pattern: The pattern for dashed borders (default is an empty list).
        :param border_dash_phase: The phase for dashed borders (default is 0).
        :param border_width_bottom: The width of the bottom border (default is 0).
        :param border_width_left: The width of the left border (default is 0).
        :param border_width_right: The width of the right border (default is 0).
        :param border_width_top: The width of the top border (default is 0).
        :param font_size: The font size for the code (default is 12).
        :param horizontal_alignment: The horizontal alignment of the snippet (default is left).
        :param margin_bottom: The bottom margin of the snippet (default is 0).
        :param margin_left: The left margin of the snippet (default is 0).
        :param margin_right: The right margin of the snippet (default is 0).
        :param margin_top: The top margin of the snippet (default is 0).
        :param padding_bottom: The bottom padding of the snippet (default is 0).
        :param padding_left: The left padding of the snippet (default is 0).
        :param padding_right: The right padding of the snippet (default is 0).
        :param padding_top: The top padding of the snippet (default is 0).
        :param remove_common_indent: Whether or not to remove the common indent (prefix) from all lines of code (default is True).
        :param vertical_alignment: The vertical alignment of the snippet (default is top).
        """
        super().__init__(
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_top=border_width_top,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        """
        Initialize a new `CodeBlock` object for rendering a block of code in a PDF document.

        This constructor allows customization of various layout and style properties
        for the code block, including background color, border styles, margins,
        and padding. These properties help define the visual appearance and spacing
        of the code block, making it distinct and readable within the PDF.

        :param code:                    The actual code content to be rendered in the block.
        :param background_color:        Optional background color for the code block.
        :param border_color:            Optional border color for the code block.
        :param border_dash_pattern:     Dash pattern used for the border lines of the code block.
        :param border_dash_phase:       Phase offset for the dash pattern in the code block borders.
        :param border_width_bottom:     Width of the bottom border of the code block.
        :param border_width_left:       Width of the left border of the code block.
        :param border_width_right:      Width of the right border of the code block.
        :param font_size:               Font size of the code block.
        :param border_width_top:        Width of the top border of the code block.
        :param horizontal_alignment:    Horizontal alignment of the code block (default is LEFT).
        :param margin_bottom:           Space between the code block and the element below it.
        :param margin_left:             Space between the code block and the left page margin.
        :param margin_right:            Space between the code block and the right page margin.
        :param margin_top:              Space between the code block and the element above it.
        :param padding_bottom:          Padding inside the code block at the bottom.
        :param padding_left:            Padding inside the code block on the left side.
        :param padding_right:           Padding inside the code block on the right side.
        :param padding_top:             Padding inside the code block at the top.
        :param vertical_alignment:      Vertical alignment of the code block (default is TOP).
        """
        lines_of_code: typing.List[typing.List[Chunk]] = CodeSnippet.__code_to_chunks(
            code=code,
            font_size=font_size,
            remove_common_indent=remove_common_indent,
            theme={
                "Token": "#e6edf3",
                "Token.Error": "#f85149",
                "Token.Keyword": "#ff7b72",
                "Token.Keyword.Constant": "#79c0ff",
                "Token.Keyword.Pseudo": "#79c0ff",
                "Token.Name": "#e6edf3",
                "Token.Name.Class": "#f0883e",
                "Token.Name.Constant": "#79c0ff",
                "Token.Name.Decorator": "#d2a8ff",
                "Token.Name.Entity": "#ffa657",
                "Token.Name.Exception": "#f0883e",
                "Token.Name.Function": "#d2a8ff",
                "Token.Name.Label": "#79c0ff",
                "Token.Name.Namespace": "#ff7b72",
                "Token.Name.Property": "#79c0ff",
                "Token.Name.Tag": "#7ee787",
                "Token.Name.Variable": "#79c0ff",
                "Token.Literal": "#a5d6ff",
                "Token.Literal.Date": "#79c0ff",
                "Token.Literal.String": "#a5d6ff",
                "Token.Literal.String.Affix": "#79c0ff",
                "Token.Literal.String.Delimiter": "#79c0ff",
                "Token.Literal.String.Escape": "#79c0ff",
                "Token.Literal.String.Heredoc": "#79c0ff",
                "Token.Literal.String.Regex": "#79c0ff",
                "Token.Literal.Number": "#a5d6ff",
                "Token.Comment": "#8b949e",
                "Token.Comment.Preproc": "#8b949e",
                "Token.Comment.Special": "#8b949e",
                "Token.Operator": "#ff7b72",
                "Token.Generic": "#e6edf3",
                "Token.Generic.Deleted": "#ffa198",
                "Token.Generic.Emph": "#e6edf3",
                "Token.Generic.Error": "#ffa198",
                "Token.Generic.Heading": "#79c0ff",
                "Token.Generic.Inserted": "#56d364",
                "Token.Generic.Output": "#8b949e",
                "Token.Generic.Prompt": "#8b949e",
                "Token.Generic.Strong": "#e6edf3",
                "Token.Generic.EmphStrong": "#e6edf3",
                "Token.Generic.Subheading": "#79c0ff",
                "Token.Generic.Traceback": "#ff7b72",
                "Token.Generic.Underline": "#e6edf3",
                "Token.Text.Whitespace": "#6e7681",
                "Token.Text": "#e6edf3",
                "Token.Escape": "#e6edf3",
                "Token.Other": "#e6edf3",
                "Token.Keyword.Declaration": "#ff7b72",
                "Token.Keyword.Namespace": "#ff7b72",
                "Token.Keyword.Reserved": "#ff7b72",
                "Token.Keyword.Type": "#ff7b72",
                "Token.Name.Attribute": "#e6edf3",
                "Token.Name.Builtin": "#e6edf3",
                "Token.Name.Builtin.Pseudo": "#e6edf3",
                "Token.Name.Function.Magic": "#d2a8ff",
                "Token.Name.Other": "#e6edf3",
                "Token.Name.Variable.Class": "#79c0ff",
                "Token.Name.Variable.Global": "#79c0ff",
                "Token.Name.Variable.Instance": "#79c0ff",
                "Token.Name.Variable.Magic": "#79c0ff",
                "Token.Literal.String.Backtick": "#a5d6ff",
                "Token.Literal.String.Char": "#a5d6ff",
                "Token.Literal.String.Doc": "#a5d6ff",
                "Token.Literal.String.Double": "#a5d6ff",
                "Token.Literal.String.Interpol": "#a5d6ff",
                "Token.Literal.String.Other": "#a5d6ff",
                "Token.Literal.String.Single": "#a5d6ff",
                "Token.Literal.String.Symbol": "#a5d6ff",
                "Token.Literal.Number.Bin": "#a5d6ff",
                "Token.Literal.Number.Float": "#a5d6ff",
                "Token.Literal.Number.Hex": "#a5d6ff",
                "Token.Literal.Number.Integer": "#a5d6ff",
                "Token.Literal.Number.Integer.Long": "#a5d6ff",
                "Token.Literal.Number.Oct": "#a5d6ff",
                "Token.Operator.Word": "#ff7b72",
                "Token.Punctuation": "#e6edf3",
                "Token.Punctuation.Marker": "#e6edf3",
                "Token.Comment.Hashbang": "#8b949e",
                "Token.Comment.Multiline": "#8b949e",
                "Token.Comment.PreprocFile": "#8b949e",
                "Token.Comment.Single": "#8b949e",
            },
        )
        # add empty line
        lines_of_code += [[Chunk(" ", font_size=font_size)]]

        # build __inner_table
        self.__inner_table: Table = FlexibleColumnWidthTable(
            number_of_rows=len(lines_of_code) + 1,
            number_of_columns=1,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            background_color=None,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

        # add shape
        t2: Table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=1)
        t2.append_layout_element(
            Table.TableCell(
                LineArt.circle(
                    fill_color=X11Color.RED, stroke_color=X11Color.RED.darker()
                ).scale_to_fit(size=(8, 8)),
                padding_right=5,
                padding_left=5,
            )
        )
        t2.append_layout_element(
            Table.TableCell(
                LineArt.circle(
                    fill_color=X11Color.ORANGE, stroke_color=X11Color.ORANGE.darker()
                ).scale_to_fit(size=(8, 8)),
                padding_right=5,
                padding_left=5,
            )
        )
        t2.append_layout_element(
            Table.TableCell(
                LineArt.circle(
                    fill_color=X11Color.GREEN_YELLOW,
                    stroke_color=X11Color.GREEN_YELLOW.darker(),
                ).scale_to_fit(size=(8, 8)),
                padding_right=5,
                padding_left=5,
            )
        )
        t2.no_borders()
        self.__inner_table.append_layout_element(
            Table.TableCell(
                t2,
                background_color=HexColor("2f2f2f"),
                padding_top=5,
                padding_right=5,
                padding_bottom=5,
                padding_left=5,
            )
        )

        # add code
        for line_nr, line_of_code in enumerate(lines_of_code):
            self.__inner_table.append_layout_element(
                Table.TableCell(
                    e=HeterogeneousParagraph(
                        chunks=line_of_code, preserve_whitespaces=True
                    ),
                    background_color=background_color,
                    padding_left=font_size,
                    padding_right=font_size,
                )
            )

        # no borders
        self.__inner_table.no_borders()

    #
    # PRIVATE
    #

    @staticmethod
    def __code_to_chunks(
        code: str,
        font_size: int = 12,
        remove_common_indent: bool = True,
        theme: typing.Dict[str, str] = {},
    ) -> typing.List[typing.List[Chunk]]:

        # try to format the code using black
        try:
            import black  # type: ignore[import-untyped, import-not-found]

            code = black.format_str(code, mode=black.Mode())
        except:
            pass

        # remove common indent (prefix)
        if remove_common_indent:
            lines: typing.List[str] = code.split("\n")
            common_indent: str = ""
            while (
                len(lines) > 0
                and len(common_indent) < len(lines[0])
                and all([line.startswith(common_indent) for line in lines])
            ):
                common_indent = lines[0][: len(common_indent) + 1]
            if len(common_indent) > 0:
                common_indent = common_indent[:-1]
            lines = [line[len(common_indent) :] for line in lines]
            code = "\n".join([line for line in lines])
            if len(code) > 0 and code.endswith("\n"):
                code = code[:-1]

        # try to apply a syntax highlighter
        output: typing.List[typing.List[Chunk]] = [[]]
        try:
            from pygments import lexers  # type: ignore[import]

            for ttype, value in lexers.get_lexer_by_name("python").get_tokens(code):
                # IF the value is a newline,
                # THEN start a new line
                if value == "\n":
                    output += [[]]
                    continue
                # default
                output[-1] += [
                    Chunk(
                        text=value,
                        font_color=HexColor(theme.get(str(ttype), "#000000")),
                        font_size=font_size,
                        font=Standard14Fonts.get("Courier"),
                    )
                ]
        # IF that fails
        # THEN process the text as is
        except:
            output = [
                [
                    Chunk(
                        text=l,
                        font_color=X11Color.WHITE,
                        font_size=font_size,
                        font=Standard14Fonts.get("Courier"),
                    )
                ]
                for l in code.split("\n")
            ]

        # remove leading/trailing empty lines
        while len(output) > 0 and output[0] == []:
            output = output[1:]
        while len(output) > 0 and output[-1] == []:
            output = output[:-1]

        # return
        return output

    #
    # PUBLIC
    #

    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        return self.__inner_table.get_size(available_space=available_space)

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        self.__inner_table.paint(available_space=available_space, page=page)
        self._LayoutElement__previous_paint_box = (
            self.__inner_table.get_previous_paint_box()
        )
