#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts HTML to PDF.
"""
import copy
import typing
import xml.etree.ElementTree as ET

from lxml.etree import HTMLParser  # type: ignore [import]

from borb.io.read.types import Decimal
from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.horizontal_rule import HorizontalRule
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import (
    HeterogeneousParagraph,
    LineBreakChunk,
)
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class HTMLToPDF:
    """
    This class converts HTML to PDF
    """

    class HTMLContext:
        def __init__(self):
            self._font_size: Decimal = Decimal(12)
            self._is_bold: bool = False
            self._is_italic: bool = False
            self._background_color: typing.Optional[Color] = None
            self._padding_left: typing.Optional[Decimal] = None
            self._parent_layout_element: typing.Union[
                LayoutElement, PageLayout, None
            ] = None

    @staticmethod
    def _process_inline(e: ET.Element, c: HTMLContext) -> typing.List[LayoutElement]:

        # determine is_bold, is_italic
        is_bold: bool = c._is_bold
        is_italic: bool = c._is_italic
        if e.tag == "em":
            is_italic = True
        if e.tag == "strong":
            is_bold = True

        # determine font_name
        font_name: str = "Helvetica"
        if is_bold and is_italic:
            font_name = "Helvetica-Bold-Oblique"
        elif is_bold:
            font_name = "Helvetica-Bold"
        elif is_italic:
            font_name = "Helvetica-Oblique"

        background_color: typing.Optional[Color] = None
        if e.tag == "code":
            background_color = HexColor("f5f7f9")

        # linebreak
        chunks: typing.List[ChunkOfText] = []
        if e.tag == "br":
            chunks.append(LineBreakChunk())

        # process text, tail
        if e.text is not None and len(e.text) > 0:
            chunks += [
                ChunkOfText(
                    w + " ",
                    background_color=background_color,
                    font_size=c._font_size,
                    font=font_name,
                )
                for w in e.text.split(" ")
                if w is not None
            ]

        # process children
        c2: HTMLToPDF.HTMLContext = copy.deepcopy(c)
        c2._parent_layout_element = c._parent_layout_element
        c2._is_bold = is_bold
        c2._is_italic = is_italic
        c2._background_color = background_color
        for child_element in e:
            child_layout_elements: typing.List[
                LayoutElement
            ] = HTMLToPDF._process_inline(child_element, c2)
            if len(child_layout_elements) == 1 and isinstance(
                child_layout_elements[0], HeterogeneousParagraph
            ):
                chunks.extend(child_layout_elements[0]._chunks_of_text)
                continue
            if all([isinstance(x, ChunkOfText) for x in child_layout_elements]):
                chunks.extend(child_layout_elements)
                continue

        # process tail
        if e.tail is not None and len(e.tail) > 0:
            chunks += [
                ChunkOfText(
                    w + " ",
                    background_color=background_color,
                    font_size=c._font_size,
                    font=font_name,
                )
                for w in e.tail.split(" ")
                if w is not None
            ]

        # exception: no chunks
        if len(chunks) == 0:
            chunks.append(ChunkOfText(" ", font_size=c._font_size))

        # create
        e: HeterogeneousParagraph = HeterogeneousParagraph(chunks)

        # add
        c._parent_layout_element.add(e)

        # return
        return [e]

    @staticmethod
    def _process_block(e: ET.Element, c: HTMLContext) -> typing.List[LayoutElement]:
        # html
        if e.tag == "html":
            html_out: typing.List[LayoutElement] = []
            for child_element in e:
                html_out.extend(HTMLToPDF._process_element(child_element, c))
            return html_out

        # body
        if e.tag == "body":
            body_out: typing.List[LayoutElement] = []
            for child_element in e:
                body_out.extend(HTMLToPDF._process_element(child_element, c))
            return body_out

        # h1
        if e.tag == "h1":
            h1_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h1_context._parent_layout_element = c._parent_layout_element
            h1_context._font_size = Decimal(12 * 2)
            return HTMLToPDF._process_inline(e, h1_context)

        # h2
        if e.tag == "h2":
            h2_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h2_context._parent_layout_element = c._parent_layout_element
            h2_context._font_size = Decimal(12 * 1.5)
            return HTMLToPDF._process_inline(e, h2_context)

        # h3
        if e.tag == "h3":
            h3_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h3_context._parent_layout_element = c._parent_layout_element
            h3_context._font_size = Decimal(12 * 1.3)
            return HTMLToPDF._process_inline(e, h3_context)

        # h4
        if e.tag == "h4":
            h4_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h4_context._parent_layout_element = c._parent_layout_element
            h4_context._font_size = Decimal(12 * 1)
            return HTMLToPDF._process_inline(e, h4_context)

        # h5
        if e.tag == "h5":
            h5_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h5_context._parent_layout_element = c._parent_layout_element
            h5_context._font_size = Decimal(12 * 0.8)
            return HTMLToPDF._process_inline(e, h5_context)

        # h6
        if e.tag == "h6":
            h6_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            h6_context._parent_layout_element = c._parent_layout_element
            h6_context._font_size = Decimal(12 * 0.7)
            return HTMLToPDF._process_inline(e, h6_context)

        # p
        if e.tag == "p":
            return HTMLToPDF._process_inline(e, c)

        # hr
        if e.tag == "hr":
            hr_layout_element: LayoutElement = HorizontalRule()
            c._parent_layout_element.add(hr_layout_element)
            return [hr_layout_element]

        # ul
        if e.tag == "ul":
            ul: UnorderedList = UnorderedList()
            ul_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            ul_context._parent_layout_element = ul
            for child_element in [x for x in e if x.tag == "li"]:
                HTMLToPDF._process_element(child_element, ul_context)
            c._parent_layout_element.add(ul)
            return [ul]

        # ol
        if e.tag == "ol":
            ol: OrderedList = OrderedList()
            ol_context: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            ol_context._parent_layout_element = ol
            for child_element in [x for x in e if x.tag == "li"]:
                HTMLToPDF._process_element(child_element, ol_context)
            c._parent_layout_element.add(ol)
            return [ol]

        # table (1)
        if e.tag == "table" and not any([True for x in e if x.tag == "tbody"]):
            number_of_rows_001: int = len([x for x in e if x.tag == "tr"])
            number_of_cols_001: int = len(
                [y for y in [x for x in e if x.tag == "tr"][0] if y.tag == "td"]
            )
            table: Table = FlexibleColumnWidthTable(
                number_of_rows=number_of_rows_001, number_of_columns=number_of_cols_001
            )
            c2: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            c2._parent_layout_element = table
            for tr in [x for x in e if x.tag == "tr"]:
                for td in [y for y in tr if y.tag == "td"]:
                    HTMLToPDF._process_element(td, c2)
            table.set_padding_on_all_cells(
                Decimal(5), Decimal(5), Decimal(5), Decimal(5)
            )
            c._parent_layout_element.add(table)
            return [table]

        # table (2)
        if e.tag == "table" and any([True for x in e if x.tag == "tbody"]):
            thead: typing.Optional[ET.Element] = next(iter([x for x in e if x.tag == "thead"]), None)
            tbody: ET.Element = next(iter([x for x in e if x.tag == "tbody"]), None)
            number_of_rows_002: int = len([x for x in tbody if x.tag == "tr"])
            number_of_cols_002: int = len([y for y in [x for x in tbody if x.tag == "tr"][0] if y.tag == "td"])
            if thead is not None:
                number_of_rows_002 += 1
            table: Table = FlexibleColumnWidthTable(
                number_of_rows=number_of_rows_002, number_of_columns=number_of_cols_002
            )
            c2: HTMLToPDF.HTMLContext = copy.deepcopy(c)
            c2._parent_layout_element = table
            # process thead
            if thead is not None:
                c2._is_bold = True
                for tr in [x for x in thead if x.tag == "tr"]:
                    for th in [y for y in tr if y.tag == "th"]:
                        HTMLToPDF._process_element(th, c2)
            # process tbody
            c2._is_bold = False
            for tr in [x for x in tbody if x.tag == "tr"]:
                for td in [y for y in tr if y.tag == "td"]:
                    HTMLToPDF._process_element(td, c2)
            table.set_padding_on_all_cells(
                Decimal(5), Decimal(5), Decimal(5), Decimal(5)
            )
            c._parent_layout_element.add(table)
            return [table]

        # default
        assert False, "Unsupported HTML element %s" % e.tag

    @staticmethod
    def _process_element(e: ET.Element, c: typing.Optional[HTMLContext] = None) -> typing.List[LayoutElement]:
        if c is None:
            c = HTMLToPDF.HTMLContext()

        # inline
        if e.tag in [None, "", "em", "strong", "li", "td", "th", "code", "br"]:
            return HTMLToPDF._process_inline(e, c)

        # blocks
        if e.tag in [
            "html",
            "body",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "ul",
            "ol",
            "table",
            "tr",
            "pre",
        ]:
            return HTMLToPDF._process_block(e, c)

        # default
        return []

    @staticmethod
    def convert_html_to_pdf(html: typing.Union[str, ET.Element]) -> Document:
        """
        This function converts HTML to PDF
        """

        # convert str to ET.Element
        root_element: typing.Optional[ET.Element] = None
        if isinstance(html, str):
            root_element = ET.fromstring(html, HTMLParser())
        else:
            root_element = html
        assert root_element is not None

        # Document
        pdf: Document = Document()

        # Page
        page: Page = Page()
        pdf.add_page(page)

        # PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # parse the stuff
        c: HTMLToPDF.HTMLContext = HTMLToPDF.HTMLContext()
        c._parent_layout_element = layout
        HTMLToPDF._process_element(root_element, c)

        # return
        return pdf
