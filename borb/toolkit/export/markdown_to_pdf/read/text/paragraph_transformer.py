#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles paragraphs
"""
import typing

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.emoji.emoji import Emoji, Emojis
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import (
    HeterogeneousParagraph,
    LineBreakChunk,
)
from borb.toolkit.export.markdown_to_pdf.read.transformer import (
    Transformer,
    TransformerState,
)


class ParagraphTransformer(Transformer):
    """
    This implementation of BaseMarkdownTransformer handles paragraphs
    """

    def _can_transform(self, context: TransformerState) -> bool:
        """
        This function always returns True, anything can be a Paragraph
        """
        return context.get_markdown_string()[
            context.tell()
        ].isalpha() or context.get_markdown_string()[context.tell()] in [
            "*",
            "_",
            ":",
            "\\",
            "`",
        ]

    def _get_font(self, is_bold: bool, is_italic: bool, is_monospaced: bool) -> Font:
        if is_monospaced:
            return StandardType1Font("Courier")
        if is_bold and is_italic:
            return StandardType1Font("Helvetica-bold-oblique")
        elif is_bold:
            return StandardType1Font("Helvetica-bold")
        elif is_italic:
            return StandardType1Font("Helvetica-oblique")
        else:
            return StandardType1Font("Helvetica")

    def _build_chunks(
        self, text: str, is_bold: bool, is_italic: bool, is_monospaced: bool
    ) -> typing.List[ChunkOfText]:
        out: typing.List[ChunkOfText] = []
        for w in text.split(" "):
            background_color: Color = HexColor("ffffff")
            if is_monospaced:
                background_color = HexColor("c3c3c3")
            out.append(
                ChunkOfText(
                    w + " ",
                    font=self._get_font(is_bold, is_italic, is_monospaced),
                    background_color=background_color,
                )
            )
        return out

    def _transform(self, context: TransformerState) -> None:

        # continue processing lines until we hit <newline><newline>
        end_pos: int = self._until_double_newline(context)
        if end_pos == -1:
            end_pos = len(context.get_markdown_string()) + 1
        paragraph_lines_raw: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_pos - 1
        ].split("\n")

        # process each line
        chunks_of_text: typing.List[typing.Union[ChunkOfText, Emoji]] = []
        is_bold: bool = False
        is_italic: bool = False
        is_monospaced: bool = False
        chunk_text: str = ""
        for paragraph_line in paragraph_lines_raw:
            i: int = 0
            while i < len(paragraph_line):
                # process \<
                c: str = paragraph_line[i]
                if (
                    c == "\\"
                    and i + 1 < len(paragraph_line)
                    and paragraph_line[i + 1] in [">", "<", "*", "+", "-", "_", "`"]
                ):
                    chunk_text += paragraph_line[i + 1]
                    i += 2
                    continue
                # process :<emoji_name>:
                if (
                    not is_monospaced
                    and c == ":"
                    and paragraph_line.find(":", i + 1) >= 0
                    and paragraph_line[i + 1 : paragraph_line.find(":", i + 1)].upper()
                    in [x.name for x in Emojis]
                ):
                    emoji_name: str = paragraph_line[
                        i + 1 : paragraph_line.find(":", i + 1)
                    ]
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunks_of_text.append(Emojis[emoji_name.upper()].value)
                    chunk_text = ""
                    i = paragraph_line.find(":", i + 1) + 1
                    continue
                # process ***
                if (
                    c == "*"
                    and i + 1 < len(paragraph_line)
                    and paragraph_line[i + 1] == "*"
                    and i + 2 < len(paragraph_line)
                    and paragraph_line[i + 2] == "*"
                ):
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_bold = not is_bold
                    is_italic = not is_italic
                    i += 3
                    continue
                # process ___
                if (
                    c == "_"
                    and i + 1 < len(paragraph_line)
                    and paragraph_line[i + 1] == "_"
                    and i + 2 < len(paragraph_line)
                    and paragraph_line[i + 2] == "_"
                ):
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_bold = not is_bold
                    is_italic = not is_italic
                    i += 3
                    continue
                # process **
                if (
                    c == "*"
                    and i + 1 < len(paragraph_line)
                    and paragraph_line[i + 1] == "*"
                ):
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_bold = not is_bold
                    i += 2
                    continue
                # process __
                if (
                    c == "_"
                    and i + 1 < len(paragraph_line)
                    and paragraph_line[i + 1] == "_"
                ):
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_bold = not is_bold
                    i += 2
                    continue
                # process *
                if c == "*":
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_italic = not is_italic
                    i += 1
                    continue
                # process _
                if c == "_":
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_italic = not is_italic
                    i += 1
                    continue
                # process `
                if c == "`":
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunk_text = ""
                    is_monospaced = not is_monospaced
                    i += 1
                    continue
                # process <whitespace><whitespace>
                if (
                    i == len(paragraph_line) - 2
                    and c == " "
                    and paragraph_line[i + 1] == " "
                ):
                    chunks_of_text.extend(
                        self._build_chunks(
                            chunk_text, is_bold, is_italic, is_monospaced
                        )
                    )
                    chunks_of_text.append(LineBreakChunk())
                    chunk_text = ""
                    i += 2
                    continue
                # process any character
                chunk_text += c
                i += 1

        # append any remaining chunks
        if len(chunk_text) > 0:
            chunks_of_text.extend(
                self._build_chunks(chunk_text, is_bold, is_italic, is_monospaced)
            )

        # append HeterogeneousParagraph
        context.get_parent_layout_element().add(HeterogeneousParagraph(chunks_of_text))  # type: ignore [union-attr]

        # seek
        context.seek(end_pos)
