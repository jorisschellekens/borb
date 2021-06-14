#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class converts Markdown to PDF.
"""
import re
import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.layout.horizontal_rule import HorizontalRule
from ptext.pdf.canvas.layout.image.image import Image
from ptext.pdf.canvas.layout.layout_element import Alignment
from ptext.pdf.canvas.layout.list.ordered_list import OrderedList
from ptext.pdf.canvas.layout.list.unordered_list import UnorderedList
from ptext.pdf.canvas.layout.page_layout import PageLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.table import Table
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.chunks_of_text import ChunksOfText
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page


class MarkdownToPDF:
    """
    This class converts Markdown to PDF.
    """

    @staticmethod
    def _handle_heading(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        if markdown_input[position].startswith("#"):
            heading_level: int = sum([1 for c in markdown_input[position] if c == "#"])
            heading_level_font_size: Decimal = {
                1: Decimal(18.2),
                2: Decimal(16.1),
                3: Decimal(14.1),
            }.get(heading_level, Decimal(14.1))
            layout.add(
                Paragraph(
                    markdown_input[position].replace("#", "").strip(),
                    font_size=heading_level_font_size,
                )
            )
            position += 1
        return position

    @staticmethod
    def _handle_unordered_list(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
        list_symbol: str = "*",
    ) -> int:
        N: int = len(markdown_input)
        if markdown_input[position].startswith("  " + list_symbol + " "):
            unordered_list_items_001: typing.List[str] = []
            while position < N and markdown_input[position].startswith(
                "  " + list_symbol + " "
            ):
                unordered_list_items_001.append(markdown_input[position][4:])
                position += 1
            ul_001: UnorderedList = UnorderedList()
            for li in unordered_list_items_001:
                ul_001.add(Paragraph(li))
            layout.add(ul_001)
        return position

    @staticmethod
    def _handle_ordered_list(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        p: re.Pattern = re.compile("  [123456789][1234567890]*\\. .*")
        if p.match(markdown_input[position]):
            list_items: typing.List[str] = []
            while position < N and p.match(markdown_input[position]):
                line: str = markdown_input[position]
                list_items.append(line[line.index(".") + 1 :])
                position += 1
            ul: OrderedList = OrderedList()
            for li in list_items:
                ul.add(Paragraph(li))
            layout.add(ul)
        return position

    @staticmethod
    def _handle_blockquote(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        if markdown_input[position].startswith("> "):
            blockquote_items: typing.List[str] = []
            while position < N and markdown_input[position].startswith("> "):
                blockquote_items.append(markdown_input[position][2:])
                position += 1
            layout.add(
                Paragraph(
                    "".join([(x + "\n") for x in blockquote_items]),
                    font="Helvetica",
                    respect_newlines_in_text=True,
                    border_color=HexColor("D3D3D3"),
                    border_left=True,
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    padding_left=Decimal(10),
                    border_width=Decimal(3),
                )
            )
        return position

    @staticmethod
    def _handle_indented_code_snippet(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        if markdown_input[position].startswith("    "):
            code_snippet_items_001: typing.List[str] = []
            while position < N and markdown_input[position].startswith("    "):
                code_snippet_items_001.append(markdown_input[position][4:])
                position += 1
            layout.add(
                Paragraph(
                    "".join([(x + "\n") for x in code_snippet_items_001]),
                    font="Courier",
                    respect_newlines_in_text=True,
                    background_color=HexColor("D3D3D3"),
                    padding_top=Decimal(10),
                    padding_right=Decimal(10),
                    padding_bottom=Decimal(10),
                    padding_left=Decimal(10),
                )
            )
        return position

    @staticmethod
    def _handle_fenced_code_snippet(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        if markdown_input[position].startswith("```"):
            position += 1
            code_snippet_items_002: typing.List[str] = []
            while position < N and not markdown_input[position].startswith("```"):
                code_snippet_items_002.append(markdown_input[position])
                position += 1
            layout.add(
                Paragraph(
                    "".join([(x + "\n") for x in code_snippet_items_002]),
                    font="Courier",
                    respect_newlines_in_text=True,
                    background_color=HexColor("D3D3D3"),
                    padding_top=Decimal(10),
                    padding_right=Decimal(10),
                    padding_bottom=Decimal(10),
                    padding_left=Decimal(10),
                )
            )
            position += 1  # process trailing fences
        return position

    @staticmethod
    def _handle_image_link(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        # fmt: off
        image_pattern: re.Pattern = re.compile('!\\[(?P<alt>[^])]+)]\\((?P<url>[^ ]+) "[^"]+"\\)')
        image_pattern_match: typing.Optional[re.Match] = image_pattern.match(markdown_input[position])
        # fmt: on
        if image_pattern_match:
            layout.add(Image(image_pattern_match["url"]))
            position += 1
        return position

    @staticmethod
    def _handle_horizontal_rule(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        if markdown_input[position] in ["---", " ---", "  ---", "   ---"]:
            layout.add(HorizontalRule())
            position += 1
        return position

    @staticmethod
    def _handle_table(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        if markdown_input[position].startswith("|") and markdown_input[
            position
        ].endswith("|"):
            table_data: typing.List[typing.List[str]] = []
            table_column_alignment: typing.List[Alignment] = []
            j: int = 0
            while (
                position < N
                and markdown_input[position].startswith("|")
                and markdown_input[position].endswith("|")
            ):
                row_data: typing.List[str] = [
                    x.strip() for x in markdown_input[position][1:-1].split("|")
                ]
                assert len(table_data) == 0 or len(table_data[-1]) == len(row_data)

                # alignment information
                if j == 1 and all(
                    [
                        len(x.replace("-", "").replace(":", "").replace(" ", "")) == 0
                        for x in row_data
                    ]
                ):
                    for k in range(0, len(row_data)):
                        if row_data[k].startswith(":") and row_data[k].endswith(":"):
                            table_column_alignment.append(Alignment.CENTERED)
                        elif row_data[k].startswith(":"):
                            table_column_alignment.append(Alignment.LEFT)
                        elif row_data[k].endswith(":"):
                            table_column_alignment.append(Alignment.RIGHT)
                        else:
                            table_column_alignment.append(Alignment.LEFT)
                    position += 1
                    j += 1
                    continue
                # regular data
                table_data.append(row_data)
                position += 1
                j += 1

            # build table from array of str
            table: Table = Table(
                number_of_rows=len(table_data), number_of_columns=len(table_data[0])
            )
            for r in range(0, len(table_data)):
                for c in range(0, len(table_data[r])):
                    if r == 0:
                        table.add(
                            Paragraph(
                                table_data[r][c],
                                font="Helvetica-Bold",
                                text_alignment=table_column_alignment[c],
                            )
                        )
                    else:
                        table.add(
                            Paragraph(
                                table_data[r][c],
                                text_alignment=table_column_alignment[c],
                            )
                        )

            table.set_padding_on_all_cells(
                Decimal(2), Decimal(2), Decimal(2), Decimal(2)
            )
            table.set_border_color_on_all_cells(HexColor("D3D3D3"))
            table.even_odd_row_colors(HexColor("FFFFFF"), HexColor("D3D3D3"))
            layout.add(table)
        return position

    @staticmethod
    def _handle_paragraph(
        markdown_input: typing.List[str],
        position: int,
        document: Document,
        layout: PageLayout,
    ) -> int:
        N: int = len(markdown_input)
        paragraph_items: typing.List[str] = []
        while position < N and markdown_input[position].strip() != "":
            paragraph_items.append(markdown_input[position])
            position += 1
        if len(paragraph_items) == 0:
            return position

        # get paragraph text
        paragraph_text: str = "".join([(x + "\n") for x in paragraph_items])

        # heterogeneous paragraph
        if (
            sum([1 for c in paragraph_text if c == "*"]) >= 2
            or sum([1 for c in paragraph_text if c == "_"]) >= 2
            or sum([1 for c in paragraph_text if c == "`"]) >= 2
        ):
            word_being_built: str = ""
            prev_italic_char: str = ""
            is_italic: bool = False
            prev_bold_char: str = ""
            is_bold: bool = False
            is_code: bool = False
            chunks_of_text: typing.List[ChunkOfText] = []

            def get_font_name():
                if is_italic and is_bold:
                    return "Helvetica-bold-oblique"
                elif is_italic:
                    return "Helvetica-oblique"
                elif is_bold:
                    return "Helvetica-bold"
                elif is_code:
                    return "Courier"
                else:
                    return "Helvetica"

            i: int = 0
            while i < len(paragraph_text):
                if paragraph_text[i] == " ":
                    word_being_built += paragraph_text[i]
                    if is_code:
                        chunks_of_text.append(ChunkOfText(word_being_built, font=get_font_name(), background_color=HexColor("D3D3D3")))
                    else:
                        chunks_of_text.append(ChunkOfText(word_being_built, font=get_font_name()))
                    word_being_built = ""
                    i += 1
                    continue
                # toggle code "`"
                if paragraph_text[i:(i+1)] == "`":
                    if is_code:
                        chunks_of_text.append(ChunkOfText(word_being_built, font=get_font_name(), background_color=HexColor("D3D3D3")))
                        word_being_built = ""
                    else:
                        assert not is_bold, "illegal nesting of operators"
                        assert not is_italic, "illegal nesting of operators"
                    is_code = not is_code
                    i += 1
                    continue
                # toggle bold "**"
                if paragraph_text[i : (i + 2)] == "**":
                    if is_bold:
                        assert (
                            prev_bold_char == "*"
                        ), "mismatched end of BOLD style, expected **"
                        prev_bold_char = ""
                        chunks_of_text.append(
                            ChunkOfText(word_being_built, font=get_font_name())
                        )
                        word_being_built = ""
                    else:
                        prev_bold_char = "*"
                    is_bold = not is_bold
                    i += 2
                    continue
                # toggle bold "__"
                if paragraph_text[i : (i + 2)] == "__":
                    if is_bold:
                        assert (
                            prev_bold_char == "_"
                        ), "mismatched end of BOLD style, expected __"
                        prev_bold_char = ""
                        chunks_of_text.append(
                            ChunkOfText(word_being_built, font=get_font_name())
                        )
                        word_being_built = ""
                    else:
                        prev_bold_char = "_"
                    is_bold = not is_bold
                    i += 2
                    continue
                # toggle italic "*"
                if paragraph_text[i : (i + 1)] == "*":
                    if is_italic:
                        assert (
                            prev_italic_char == "*"
                        ), "mismatched end of ITALIC style, expected *"
                        prev_italic_char = ""
                        chunks_of_text.append(
                            ChunkOfText(word_being_built, font=get_font_name())
                        )
                        word_being_built = ""
                    else:
                        prev_italic_char = "*"
                    is_italic = not is_italic
                    i += 1
                    continue
                # toggle italic "_"
                if paragraph_text[i : (i + 1)] == "_":
                    if is_italic:
                        assert (
                            prev_italic_char == "_"
                        ), "mismatched end of ITALIC style, expected _"
                        prev_italic_char = ""
                        chunks_of_text.append(
                            ChunkOfText(word_being_built, font=get_font_name())
                        )
                        word_being_built = ""
                    else:
                        prev_italic_char = "_"
                    is_italic = not is_italic
                    i += 1
                    continue
                word_being_built += paragraph_text[i]
                i += 1
            assert not is_bold, "missing end of BOLD style"
            assert not is_italic, "missing end of ITALIC style"
            if len(word_being_built) > 0:
                chunks_of_text.append(
                    ChunkOfText(word_being_built, font=get_font_name())
                )
            layout.add(ChunksOfText(chunks_of_text))
        else:
            # homogeneous paragraph
            layout.add(
                Paragraph(
                    paragraph_text,
                    respect_newlines_in_text=True,
                )
            )

        return position

    @staticmethod
    def convert_markdown_to_pdf(markdown_str: str) -> Document:
        """
        This function converts a markdown document to a PDF Document
        """

        # create new Document
        document: Document = Document()

        # create empty Page
        page: Page = Page()
        document.append_page(page)

        # select a layout manager
        layout: PageLayout = SingleColumnLayout(page)

        lines: typing.List[str] = markdown_str.split("\n")
        i: int = 0
        N: int = len(lines)
        while i < N:

            # handle heading
            j: int = i
            j = MarkdownToPDF._handle_heading(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # handle lists
            j = MarkdownToPDF._handle_unordered_list(lines, i, document, layout, "*")
            if j != i:
                i = j
                continue
            j = MarkdownToPDF._handle_unordered_list(lines, i, document, layout, "-")
            if j != i:
                i = j
                continue
            j = MarkdownToPDF._handle_unordered_list(lines, i, document, layout, "+")
            if j != i:
                i = j
                continue
            j = MarkdownToPDF._handle_ordered_list(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # blockquote
            j = MarkdownToPDF._handle_blockquote(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # code
            j = MarkdownToPDF._handle_indented_code_snippet(lines, i, document, layout)
            if j != i:
                i = j
                continue
            j = MarkdownToPDF._handle_fenced_code_snippet(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # image
            j = MarkdownToPDF._handle_image_link(lines, i, document, layout)
            if j != i:
                i = j
                continue
            j = MarkdownToPDF._handle_horizontal_rule(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # table
            j = MarkdownToPDF._handle_table(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # paragraph
            j = MarkdownToPDF._handle_paragraph(lines, i, document, layout)
            if j != i:
                i = j
                continue

            # move to next line (if needed)
            i += 1

        return document
