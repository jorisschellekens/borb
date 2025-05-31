#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `MarkdownParagraph` class: A paragraph layout element with Markdown-like formatting.

This class extends the functionality of `HeterogeneousParagraph` to allow users to create
richly formatted paragraphs using a simple Markdown-inspired syntax. It interprets
special characters to apply styles such as bold, italic, colored text, and highlighted
backgrounds to different parts of the text. Each segment of text, represented by a `Chunk`,
can have its own unique style properties.

Markdown-like formatting rules:
- `*italic*`: Italicized text.
- `**bold**`: Bold text.
- `~highlight~`: Highlighted text with a yellow background.
"""
import collections
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph

MarkdownChunkType = collections.namedtuple(
    "MarkdownChunkType", ["text", "bold", "highlight", "italic"]
)


class MarkdownParagraph(HeterogeneousParagraph):
    """
    The `MarkdownParagraph` class: A paragraph layout element with Markdown-like formatting.

    This class extends the functionality of `HeterogeneousParagraph` to allow users to create
    richly formatted paragraphs using a simple Markdown-inspired syntax. It interprets
    special characters to apply styles such as bold, italic, colored text, and highlighted
    backgrounds to different parts of the text. Each segment of text, represented by a `Chunk`,
    can have its own unique style properties.

    Markdown-like formatting rules:
    - `*italic*`: Italicized text.
    - `**bold**`: Bold text.
    - `~highlight~`: Highlighted text with a yellow background.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        fixed_leading: typing.Optional[int] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        multiplied_leading: typing.Optional[float] = 1.2,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        preserve_whitespaces: bool = False,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a `MarkdownParagraph` with markdown-like formatting and optional layout properties.

        This constructor creates a `MarkdownParagraph`, a subclass of `HeterogeneousParagraph`, designed
        to simplify the creation of richly formatted text blocks using markdown-like syntax.
        Each text segment is styled based on markdown-like markers such as `*`, `_`, `~`, and `~~`.

        :arg text: The text content to display, formatted using markdown-like syntax.
        :arg background_color: (Optional[Color]) Background color of the paragraph. Defaults to None.
        :arg border_color: (Optional[Color]) Border color of the paragraph. Defaults to None.
        :arg border_dash_pattern: (List[int]) Dash pattern for the border. Defaults to [].
        :arg border_dash_phase: (int) Starting phase for the border dash pattern. Defaults to 0.
        :arg border_width_bottom: (int) Width of the bottom border. Defaults to 0.
        :arg border_width_left: (int) Width of the left border. Defaults to 0.
        :arg border_width_right: (int) Width of the right border. Defaults to 0.
        :arg border_width_top: (int) Width of the top border. Defaults to 0.
        :arg default_chunk_background_color: (Optional[Color]) Default background color for text chunks. Defaults to None.
        :arg default_font: (Union[str, Font]) Default font for text chunks. Defaults to "Helvetica".
        :arg default_font_color: (Color) Default font color for text chunks. Defaults to `X11Color.BLACK`.
        :arg default_font_size: (int) Default font size for text chunks. Defaults to 12.
        :arg fixed_leading: (Optional[int]) Fixed line spacing in user space units. Defaults to None.
        :arg horizontal_alignment: (LayoutElement.HorizontalAlignment) Horizontal alignment of the paragraph. Defaults to `HorizontalAlignment.LEFT`.
        :arg margin_bottom: (int) Bottom margin of the paragraph. Defaults to 0.
        :arg margin_left: (int) Left margin of the paragraph. Defaults to 0.
        :arg margin_right: (int) Right margin of the paragraph. Defaults to 0.
        :arg margin_top: (int) Top margin of the paragraph. Defaults to 0.
        :arg multiplied_leading: (Optional[float]) Line spacing multiplier. Defaults to 1.2.
        :arg padding_bottom: (int) Bottom padding of the paragraph. Defaults to 0.
        :arg padding_left: (int) Left padding of the paragraph. Defaults to 0.
        :arg padding_right: (int) Right padding of the paragraph. Defaults to 0.
        :arg padding_top: (int) Top padding of the paragraph. Defaults to 0.
        :arg preserve_whitespaces: (bool) Whether to preserve whitespaces in the text. Defaults to False.
        :arg text_alignment: (LayoutElement.TextAlignment) Text alignment within the paragraph. Defaults to `TextAlignment.LEFT`.
        :arg vertical_alignment: (LayoutElement.VerticalAlignment) Vertical alignment of the paragraph. Defaults to `VerticalAlignment.TOP`.
        """
        super().__init__(
            MarkdownParagraph.__split_text_and_apply_formatting(text=text),
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            fixed_leading=fixed_leading,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            multiplied_leading=multiplied_leading,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            preserve_whitespaces=preserve_whitespaces,
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __split_text_and_apply_formatting(text: str) -> typing.List[Chunk]:

        i: int = 0
        is_escaped: bool = False
        bold: bool = False
        italic: bool = False
        yellow_highlight: bool = False
        blue_highlight: bool = False
        chunks: typing.List[MarkdownChunkType] = []
        while i < len(text):

            # escape sequence
            if text[i] == "\\":
                is_escaped = True
                i += 1
                continue

            # bold
            if not is_escaped and text[i : i + 2] == "**":
                bold = not bold
                i += 2
                continue
            if not is_escaped and text[i : i + 2] == "__":
                bold = not bold
                i += 2
                continue

            # italic
            if not is_escaped and text[i] == "*":
                italic = not italic
                i += 1
                continue
            if not is_escaped and text[i] == "_":
                italic = not italic
                i += 1
                continue

            # highlight
            if not is_escaped and text[i : i + 2] == "~~":
                blue_highlight = not blue_highlight
                i += 2
                continue
            if not is_escaped and text[i] == "~":
                yellow_highlight = not yellow_highlight
                i += 1
                continue

            # text
            if len(chunks) == 0:
                # IF the text is a space
                # THEN we either need to create a new chunk (assuming the space is escaped) OR not
                if text[i].isspace():
                    if is_escaped:
                        chunks += [
                            MarkdownChunkType(
                                text=text[i],
                                bold=bold,
                                highlight=yellow_highlight,
                                italic=italic,
                            )
                        ]
                    else:
                        chunks += [
                            MarkdownChunkType(
                                text="",
                                bold=bold,
                                highlight=yellow_highlight,
                                italic=italic,
                            )
                        ]
                # IF the text is not a space
                # THEN we create a new (initial) chunk
                else:
                    chunks += [
                        MarkdownChunkType(
                            text=text[i],
                            bold=bold,
                            highlight=yellow_highlight,
                            italic=italic,
                        )
                    ]
                i += 1
                is_escaped = False
                continue
            else:
                # IF the previous chunk has the same markup as the current one
                # THEN we append
                if (
                    chunks[-1].bold == bold
                    and chunks[-1].highlight == yellow_highlight
                    and chunks[-1].italic == italic
                ):
                    if text[i].isspace():
                        if is_escaped:
                            chunks[-1] = MarkdownChunkType(
                                text=chunks[-1].text + text[i],
                                bold=chunks[-1].bold,
                                highlight=chunks[-1].highlight,
                                italic=chunks[-1].italic,
                            )
                        else:
                            if (
                                len(chunks[-1].text) == 0
                                or chunks[-1].text[-1].isspace()
                            ):
                                pass
                            else:
                                chunks[-1] = MarkdownChunkType(
                                    text=chunks[-1].text + text[i],
                                    bold=chunks[-1].bold,
                                    highlight=chunks[-1].highlight,
                                    italic=chunks[-1].italic,
                                )
                    else:
                        chunks[-1] = MarkdownChunkType(
                            text=chunks[-1].text + text[i],
                            bold=chunks[-1].bold,
                            highlight=chunks[-1].highlight,
                            italic=chunks[-1].italic,
                        )
                    i += 1
                    is_escaped = False
                    continue
                # IF NOT
                # THEN we create a new chunk
                else:
                    if text[i].isspace():
                        if is_escaped:
                            chunks += [
                                MarkdownChunkType(
                                    text=text[i],
                                    bold=bold,
                                    highlight=yellow_highlight,
                                    italic=italic,
                                )
                            ]
                        else:
                            if chunks[-1].text[-1].isspace():
                                chunks += [
                                    MarkdownChunkType(
                                        text="",
                                        bold=bold,
                                        highlight=yellow_highlight,
                                        italic=italic,
                                    )
                                ]
                            else:
                                chunks += [
                                    MarkdownChunkType(
                                        text=text[i],
                                        bold=bold,
                                        highlight=yellow_highlight,
                                        italic=italic,
                                    )
                                ]
                    else:
                        chunks += [
                            MarkdownChunkType(
                                text=text[i],
                                bold=bold,
                                highlight=yellow_highlight,
                                italic=italic,
                            )
                        ]
                    i += 1
                    is_escaped = False
                    continue

        chunk_objects: typing.List[Chunk] = []
        for c in chunks:
            if c.bold and c.italic:
                chunk_objects += [
                    Chunk(
                        text=c.text,
                        font="Helvetica-Bold-Oblique",
                        background_color=(
                            X11Color.YELLOW_MUNSELL if c.highlight else None
                        ),
                    )
                ]
            elif c.bold:
                chunk_objects += [
                    Chunk(
                        text=c.text,
                        font="Helvetica-Bold",
                        background_color=(
                            X11Color.YELLOW_MUNSELL if c.highlight else None
                        ),
                    )
                ]
            elif c.italic:
                chunk_objects += [
                    Chunk(
                        text=c.text,
                        font="Helvetica-Oblique",
                        background_color=(
                            X11Color.YELLOW_MUNSELL if c.highlight else None
                        ),
                    )
                ]
            else:
                chunk_objects += [
                    Chunk(
                        text=c.text,
                        font="Helvetica",
                        background_color=(
                            X11Color.YELLOW_MUNSELL if c.highlight else None
                        ),
                    )
                ]

        # return
        return chunk_objects

    #
    # PUBLIC
    #
