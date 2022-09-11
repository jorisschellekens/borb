#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts HTML to PDF.
"""
import copy
import logging
import typing
import xml.etree.ElementTree as ET

from lxml.etree import HTMLParser, _Comment  # type: ignore [import]

from borb.io.read.types import Decimal, Name, String, Dictionary
from borb.pdf import Image
from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.emoji.emoji import Emoji, Emojis
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.horizontal_rule import HorizontalRule
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import LineBreakChunk
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.xref.plaintext_xref import PlainTextXREF
from borb.toolkit.export.html_to_pdf.block_flow import BlockFlow
from borb.toolkit.export.html_to_pdf.inline_flow import InlineFlow

logger = logging.getLogger(__name__)


class HTMLToPDF:
    """
    This class converts HTML to PDF
    """

    class Context:
        """
        This class represents the context in which an (HTML) Element is
        being transformed into its LayoutElement representation. This context
        keeps track of whether an Element should be rendered bold, italic, or both,
        the font_size and the background_color.
        """

        def __init__(self):
            # font properties
            self._fallback_fonts_regular: typing.List[Font] = [
                StandardType1Font("Helvetica")
            ]
            self._fallback_fonts_italic: typing.List[Font] = [
                StandardType1Font("Helvetica-Oblique")
            ]
            self._fallback_fonts_bold: typing.List[Font] = [
                StandardType1Font("Helvetica-Bold")
            ]
            self._fallback_fonts_bold_italic: typing.List[Font] = [
                StandardType1Font("Helvetica-Bold-Oblique")
            ]
            self._fallback_fonts_monospaced: typing.List[Font] = [
                StandardType1Font("Courier")
            ]
            self._is_bold: bool = False
            self._is_italic: bool = False
            self._is_monospaced: bool = False
            self._default_font_size: Decimal = Decimal(12)
            self._font_size: Decimal = self._default_font_size
            self._font_color: typing.Optional[Color] = HexColor("000000")
            # style properties
            self._background_color: typing.Optional[Color] = None
            # linking
            self._document: typing.Optional[Document] = None

    @staticmethod
    def _process_element(e: ET.Element, c: Context) -> LayoutElement:
        ELEMENT_CREATOR_METHODS: typing.Dict[
            str, typing.Callable[[ET.Element, HTMLToPDF.Context], LayoutElement]
        ] = {
            "a": HTMLToPDF._process_a_element,
            "abbr": None,
            "acronym": None,
            "address": None,  # TODO
            "article": HTMLToPDF._process_article_element,
            "aside": None,
            "b": HTMLToPDF._process_b_element,
            "bdo": None,
            "big": None,  # TODO
            "blockquote": HTMLToPDF._process_blockquote_element,
            "body": HTMLToPDF._process_body_element,
            "br": HTMLToPDF._process_br_element,
            "button": None,
            "canvas": None,
            "cite": None,  # TODO
            "code": HTMLToPDF._process_code_element,
            "dd": None,
            "dfn": None,
            "div": HTMLToPDF._process_div_element,
            "dl": None,
            "dt": None,
            "em": HTMLToPDF._process_em_element,
            "fieldset": None,
            "figcaption": None,  # TODO
            "figure": HTMLToPDF._process_figure_element,
            "footer": None,  # TODO
            "form": None,
            "h1": HTMLToPDF._process_hx_element,
            "h2": HTMLToPDF._process_hx_element,
            "h3": HTMLToPDF._process_hx_element,
            "h4": HTMLToPDF._process_hx_element,
            "h5": HTMLToPDF._process_hx_element,
            "h6": HTMLToPDF._process_hx_element,
            "head": HTMLToPDF._process_head_element,
            "header": None,  # TODO
            "hr": HTMLToPDF._process_hr_element,
            "html": HTMLToPDF._process_html_element,
            "i": HTMLToPDF._process_i_element,
            "img": HTMLToPDF._process_img_element,
            "kbd": None,
            "li": HTMLToPDF._process_li_element,
            "main": HTMLToPDF._process_main_element,
            "map": None,  # TODO
            "mark": HTMLToPDF._process_mark_element,
            "meta": HTMLToPDF._process_meta_element,
            "nav": None,
            "noscript": HTMLToPDF._process_noscript_element,
            "ol": HTMLToPDF._process_ol_element,
            "p": HTMLToPDF._process_p_element,
            "pre": None,  # TODO
            "q": HTMLToPDF._process_q_element,
            "samp": HTMLToPDF._process_samp_element,
            "section": HTMLToPDF._process_section_element,
            "span": HTMLToPDF._process_inline_element,
            "strong": HTMLToPDF._process_strong_element,
            "table": HTMLToPDF._process_table_element,
            "title": HTMLToPDF._process_title_element,
            "tfoot": None,
            "ul": HTMLToPDF._process_ul_element,
            "video": None,  # TODO
        }
        if ELEMENT_CREATOR_METHODS.get(e.tag, None) is None:
            logger.warning("<%s> unsupported" % e.tag)
            return None
        return ELEMENT_CREATOR_METHODS[e.tag](e, c)

    @staticmethod
    def _process_a_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "a"
        e.tag = "span"

        prev_tail: str = e.tail
        e.tail = ""
        prev_font_color = c._font_color
        c._font_color = HexColor("#0645ad")
        out_value_001: LayoutElement = HTMLToPDF._process_element(e, c)
        c._font_color = prev_font_color
        e.tag = "a"

        # fake span to hold tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = prev_tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)
        e.tail = prev_tail

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_article_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "article"
        return HTMLToPDF._process_block_element(e, c)

    @staticmethod
    def _process_b_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "b"
        e.tag = "strong"
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "b"
        return out_value

    @staticmethod
    def _process_blockquote_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "blockquote"
        prev_background_color: typing.Optional[Color] = c._background_color
        c._background_color = HexColor("F5F5F5")
        blockquote_element: LayoutElement = HTMLToPDF._process_block_element(e, c)
        blockquote_element._background_color = c._background_color
        blockquote_element._padding_left = c._font_size * 2
        blockquote_element._border_left = True
        blockquote_element._border_width = Decimal(2)
        blockquote_element._border_color = HexColor("DCDCDC")
        c._background_color = prev_background_color
        return blockquote_element

    @staticmethod
    def _process_body_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "body"
        return HTMLToPDF._process_block_element(e, c)

    @staticmethod
    def _process_br_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "br"
        e.tag = "span"
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "br"
        return InlineFlow().extend([LineBreakChunk(), out_value])

    @staticmethod
    def _process_code_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "code"
        e.tag = "span"

        prev_tail: str = e.tail
        e.tail = ""
        prev_background_color = c._background_color
        prev_is_monospaced: bool = c._is_monospaced
        c._background_color = HexColor("#f5f5f5")
        c._is_monospaced = True
        out_value_001: LayoutElement = HTMLToPDF._process_element(e, c)
        c._background_color = prev_background_color
        c._is_monospaced = prev_is_monospaced
        e.tag = "code"

        # fake span to hold tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = prev_tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)
        e.tail = prev_tail

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_div_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "div"
        return HTMLToPDF._process_element(e, c)

    @staticmethod
    def _process_em_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "em"
        e.tag = "span"

        prev_tail: str = e.tail
        e.tail = ""
        prev_is_italic = c._is_italic
        c._is_italic = True
        out_value_001: LayoutElement = HTMLToPDF._process_element(e, c)
        c._is_italic = prev_is_italic
        e.tag = "em"

        # fake span to hold tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = prev_tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)
        e.tail = prev_tail

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_figure_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "figure"
        figcaption: typing.Optional[ET.Element] = next(
            iter([x for x in e if x.tag == "figcaption"]), None
        )
        img: typing.Optional[ET.Element] = next(
            iter([x for x in e if x.tag == "img"]), None
        )
        number_of_rows: int = 0
        if figcaption is not None:
            number_of_rows += 1
        if img is not None:
            number_of_rows += 1
        table: Table = FlexibleColumnWidthTable(
            number_of_columns=1, number_of_rows=number_of_rows
        )
        if img is not None:
            table.add(HTMLToPDF._process_element(img, c))
        if figcaption is not None:
            table.add(HTMLToPDF._process_element(figcaption, c))
        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        table.no_borders()
        return table

    @staticmethod
    def _process_hx_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag in ["h1", "h2", "h3", "h4", "h5", "h6"]
        FONT_SIZE_MODIFIER: typing.Dict[str, Decimal] = {
            "h1": Decimal(2),
            "h2": Decimal(1.5),
            "h3": Decimal(1.17),
            "h4": Decimal(1),
            "h5": Decimal(0.83),
            "h6": Decimal(0.67),
        }
        # modify Context
        prev_font_size: Decimal = c._font_size
        prev_is_bold: bool = c._is_bold
        c._font_size = c._default_font_size * FONT_SIZE_MODIFIER[e.tag]
        c._is_bold = True

        # recursion
        header_layout_element: LayoutElement = BlockFlow().add(
            HTMLToPDF._process_inline_element(e, c)
        )
        header_layout_element._padding_bottom = c._font_size
        header_layout_element._padding_top = c._font_size

        # modify Context
        c._font_size = prev_font_size
        c._is_bold = prev_is_bold

        # return
        return header_layout_element

    @staticmethod
    def _process_head_element(e: ET.Element, c: Context) -> None:
        assert e.tag == "head"
        # title
        if "title" in [x.tag for x in e]:
            HTMLToPDF._process_element([x for x in e if x.tag == "title"][0], c)
        # meta
        for meta_element in [x for x in e if x.tag == "meta"]:
            HTMLToPDF._process_element(meta_element, c)

    @staticmethod
    def _process_hr_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "hr"

        # process tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = e.tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)

        # return
        return BlockFlow().extend([HorizontalRule(), out_value_002])

    @staticmethod
    def _process_html_element(e: ET.Element, c: Context) -> LayoutElement:
        # head
        if "head" in [x.tag for x in e]:
            HTMLToPDF._process_element([x for x in e if x.tag == "head"][0], c)
        # body
        if "body" in [x.tag for x in e]:
            return HTMLToPDF._process_element([x for x in e if x.tag == "body"][0], c)
        # default
        return BlockFlow()

    @staticmethod
    def _process_i_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "i"
        e.tag = "em"
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "i"
        return out_value

    @staticmethod
    def _process_img_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "img"
        src: str = e.attrib["src"]
        w: typing.Optional[Decimal] = (
            Decimal(e.attrib["width"]) if "width" in e.attrib else None
        )
        h: typing.Optional[Decimal] = (
            Decimal(e.attrib["height"]) if "height" in e.attrib else None
        )
        out_value_001: LayoutElement = Image(src, width=w, height=h)

        # process tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = e.tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_li_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "li"
        return HTMLToPDF._process_block_element(e, c)

    @staticmethod
    def _process_main_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "main"
        return HTMLToPDF._process_block_element(e, c)

    @staticmethod
    def _process_mark_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "mark"
        e.tag = "span"

        prev_tail: str = e.tail
        e.tail = ""
        prev_background_color = c._background_color
        c._background_color = HexColor("#ffff00")
        out_value_001: LayoutElement = HTMLToPDF._process_element(e, c)
        c._background_color = prev_background_color
        e.tag = "mark"

        # fake span to hold tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = prev_tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)
        e.tail = prev_tail

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_meta_element(e: ET.Element, c: Context) -> None:
        assert e.tag == "meta"
        document: typing.Optional[Document] = c._document
        if document is None:
            return
        name: str = e.attrib.get("name", "")
        content: str = e.attrib.get("content", "")
        if "XRef" not in document:
            document[Name("XRef")] = PlainTextXREF()
        if "Trailer" not in document["XRef"]:
            document["XRef"][Name("Trailer")] = Dictionary()
        if "Info" not in document["XRef"]["Trailer"]:
            document["XRef"]["Trailer"][Name("Info")] = Dictionary()
        if name == "keywords":
            document["XRef"]["Trailer"]["Info"][Name("Keywords")] = String(content)
        if name == "description":
            document["XRef"]["Trailer"]["Info"][Name("Subject")] = String(content)
        if name == "author":
            document["XRef"]["Trailer"]["Info"][Name("Author")] = String(content)

    @staticmethod
    def _process_noscript_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "noscript"
        e.tag = "p"
        return_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "noscript"
        return return_value

    @staticmethod
    def _process_ol_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "ol"
        ol_layout_element: OrderedList = OrderedList()
        for child_element in e:
            if child_element.tag == ET.Comment:
                continue
            ol_layout_element.add(HTMLToPDF._process_element(child_element, c))
        return BlockFlow().add(ol_layout_element)

    @staticmethod
    def _process_p_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "p"
        return BlockFlow().add(HTMLToPDF._process_inline_element(e, c))

    @staticmethod
    def _process_pre_element(e: ET.Element, c: Context) -> LayoutElement:
        return None

    @staticmethod
    def _process_q_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "q"
        e.tag = "span"
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "q"
        return InlineFlow().extend(
            [
                HTMLToPDF._build_chunk_of_text('"', c),
                out_value,
                HTMLToPDF._build_chunk_of_text('"', c),
            ]
        )

    @staticmethod
    def _process_samp_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "samp"
        e.tag = "span"
        prev_is_monospaced: bool = c._is_monospaced
        c._is_monospaced = True
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        c._is_monospaced = prev_is_monospaced
        e.tag = "samp"
        return out_value

    @staticmethod
    def _process_section_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "section"
        e.tag = "div"
        out_value: LayoutElement = HTMLToPDF._process_element(e, c)
        e.tag = "section"
        return out_value

    @staticmethod
    def _process_strong_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "strong"
        e.tag = "span"

        prev_tail: str = e.tail
        e.tail = ""
        prev_is_bold = c._is_bold
        c._is_bold = True
        out_value_001: LayoutElement = HTMLToPDF._process_element(e, c)
        c._is_bold = prev_is_bold
        e.tag = "strong"

        # fake span to hold tail
        tmp: ET.Element = ET.Element("span")
        tmp.text = prev_tail
        out_value_002: LayoutElement = HTMLToPDF._process_element(tmp, c)
        e.tail = prev_tail

        # return
        return InlineFlow().extend([out_value_001, out_value_002])

    @staticmethod
    def _process_table_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "table"
        if "tbody" in [x.tag for x in e]:
            return HTMLToPDF._process_table_element_001(e, c)
        else:
            return HTMLToPDF._process_table_element_002(e, c)

    @staticmethod
    def _process_table_element_001(e: ET.Element, c: Context) -> LayoutElement:
        # separate thead / tbody
        thead: typing.Optional[ET.Element] = next(
            iter([x for x in e if x.tag == "thead"]), None
        )
        tbody: ET.Element = next(iter([x for x in e if x.tag == "tbody"]))

        # count rows / cols
        nrows_000: int = len([x for x in tbody if x.tag == "tr"]) + (
            1 if thead is not None else 0
        )
        ncols_000: int = len(
            [y for y in [x for x in tbody if x.tag == "tr"][0] if y.tag == "td"]
        )

        # create Table
        table: Table = FlexibleColumnWidthTable(
            number_of_rows=nrows_000, number_of_columns=ncols_000
        )
        if thead is not None:
            for tr in [x for x in thead if x.tag == "tr"]:
                for th in [y for y in tr if y.tag == "th"]:
                    table.add(HTMLToPDF._process_inline_element(th, c))
        for tr in [x for x in tbody if x.tag == "tr"]:
            for td in [y for y in tr if y.tag == "td"]:
                table.add(HTMLToPDF._process_inline_element(td, c))

        # add Table to body
        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        table._margin_top = c._default_font_size
        table._margin_bottom = c._default_font_size
        return table

    @staticmethod
    def _process_table_element_002(e: ET.Element, c: Context) -> LayoutElement:

        # count rows / cols
        nrows_001: int = len([x for x in e if x.tag == "tr"])
        ncols_001: int = len(
            [y for y in [x for x in e if x.tag == "tr"][0] if y.tag == "td"]
        )

        # create Table
        table: Table = FlexibleColumnWidthTable(
            number_of_rows=nrows_001, number_of_columns=ncols_001
        )
        for tr in [x for x in e if x.tag == "tr"]:
            for td in [y for y in tr if y.tag == "td"]:
                table.add(HTMLToPDF._process_inline_element(td, c))

        # add Table to body
        table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        table._margin_top = c._default_font_size
        table._margin_bottom = c._default_font_size
        return table

    @staticmethod
    def _process_title_element(e: ET.Element, c: Context) -> None:
        assert e.tag == "title"
        document: typing.Optional[Document] = c._document
        if document is None:
            return
        if "XRef" not in document:
            document[Name("XRef")] = PlainTextXREF()
        if "Trailer" not in document["XRef"]:
            document["XRef"][Name("Trailer")] = Dictionary()
        if "Info" not in document["XRef"]["Trailer"]:
            document["XRef"]["Trailer"][Name("Info")] = Dictionary()
        document["XRef"]["Trailer"]["Info"][Name("Title")] = String(e.text)

    @staticmethod
    def _process_ul_element(e: ET.Element, c: Context) -> LayoutElement:
        assert e.tag == "ul"
        ul_layout_element: UnorderedList = UnorderedList()
        for child_element in e:
            if child_element.tag == ET.Comment:
                continue
            ul_layout_element.add(HTMLToPDF._process_element(child_element, c))
        return ul_layout_element

    #
    # LOW-LEVEL METHODS
    #

    @staticmethod
    def _process_block_element(e: ET.Element, c: Context) -> LayoutElement:
        block_layout_element: BlockFlow = BlockFlow()

        # add text
        # create artificial <span> element
        # then pass that element through HTMLToPDF._process_element
        if e.text is not None and len(e.text) > 0:
            tmp_span: ET.Element = ET.Element("span")
            tmp_span.text = e.text
            block_layout_element.add(HTMLToPDF._process_element(tmp_span, c))

        # process children
        for child_element in e:
            if isinstance(child_element, _Comment):
                continue
            block_layout_element.add(HTMLToPDF._process_element(child_element, c))

        # add tail
        # create artificial <span> element
        # then pass that element through HTMLToPDF._process_element
        if e.tail is not None and len(e.tail) > 0:
            tmp_span: ET.Element = ET.Element("span")
            tmp_span.text = e.tail
            block_layout_element.add(HTMLToPDF._process_element(tmp_span, c))

        # return
        return block_layout_element

    @staticmethod
    def _process_inline_element(e: ET.Element, c: Context) -> LayoutElement:

        # <span class="emoji"></span>
        chunks: typing.List[LayoutElement] = []
        if e.tag == "span" and (
            "EMOJI" in e.attrib.get("class", "").upper().split(" ")
        ):
            emoji: str = [
                x
                for x in e.attrib.get("class", "").upper().split(" ")
                if x.startswith("EMOJI_")
            ][0][6:]
            chunks.append(Emojis[emoji].value)
            e.text = ""

        # text
        if e.text is not None and len(e.text) > 0:
            ws: typing.List[str] = [x for x in e.text.split(" ")]
            ws = [x + " " for x in ws[0 : len(ws) - 1]] + [ws[-1]]
            chunks.extend([HTMLToPDF._build_chunk_of_text(w, c) for w in ws])

        # children
        for child_element in e:
            if isinstance(child_element, _Comment):
                continue
            chunks.append(HTMLToPDF._process_element(child_element, c))

        # tail
        if e.tail is not None and len(e.tail) > 0:
            ws: typing.List[str] = [x for x in e.tail.split(" ")]
            ws = [x + " " for x in ws[0 : len(ws) - 1]] + [ws[-1]]
            chunks.extend([HTMLToPDF._build_chunk_of_text(w, c) for w in ws])

        # empty
        if len(chunks) == 0:
            chunks.append(HTMLToPDF._build_chunk_of_text(" ", c))

        # return
        return InlineFlow().extend(chunks)

    @staticmethod
    def _build_chunk_of_text(s: str, c: Context) -> LayoutElement:
        fonts_to_try: typing.List[Font] = []
        if c._is_bold and c._is_italic:
            fonts_to_try = c._fallback_fonts_bold_italic
        elif c._is_bold:
            fonts_to_try = c._fallback_fonts_bold
        elif c._is_italic:
            fonts_to_try = c._fallback_fonts_italic
        else:
            fonts_to_try = c._fallback_fonts_regular
        if c._is_monospaced:
            fonts_to_try = c._fallback_fonts_monospaced

        # try
        for font_to_try in fonts_to_try:
            try:
                c: ChunkOfText = ChunkOfText(
                    s,
                    font=font_to_try,
                    font_size=c._font_size,
                    font_color=c._font_color,
                    background_color=c._background_color,
                )
                c._write_text_bytes()
                return c
            except:
                continue

        # default
        return ChunkOfText(
            "□",
            font="Helvetica",
            font_size=c._font_size,
            font_color=c._font_color,
            background_color=c._background_color,
        )

    #
    # public methods
    #

    @staticmethod
    def convert_html_to_layout_element(
        html: typing.Union[str, ET.Element],
        fallback_fonts_regular: typing.List[Font] = [StandardType1Font("Helvetica")],
        fallback_fonts_bold: typing.List[Font] = [StandardType1Font("Helvetica-Bold")],
        fallback_fonts_italic: typing.List[Font] = [StandardType1Font("Helvetica-Oblique")],
        fallback_fonts_bold_italic: typing.List[Font] = [StandardType1Font("Helvetica-Bold-Oblique")],
        fallback_fonts_monospaced: typing.List[Font] = [StandardType1Font("Courier")],
    ) -> LayoutElement:
        """
        This function converts a html str to a LayoutElement
        :param html:                        the html str (or ET.Element) to be converted
        :param fallback_fonts_regular:      fallback (regular) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold:         fallback (bold) fonts to try when the default font is unable to render a character
        :param fallback_fonts_italic:       fallback (italic) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold_italic:  fallback (bold, italic) fonts to try when the default font is unable to render a character
        :return:
        """

        # convert str to ET.Element
        root_element: typing.Optional[ET.Element] = None
        if isinstance(html, str):
            root_element = ET.fromstring(html, HTMLParser())
        else:
            root_element = html
        assert root_element is not None

        # build context
        c: HTMLToPDF.Context = HTMLToPDF.Context()
        c._fallback_fonts_regular = fallback_fonts_regular
        c._fallback_fonts_bold = fallback_fonts_bold
        c._fallback_fonts_italic = fallback_fonts_italic
        c._fallback_fonts_bold_italic = fallback_fonts_bold_italic
        c._fallback_fonts_monospaced = fallback_fonts_monospaced

        # return
        return HTMLToPDF._process_html_element(root_element, c)

    @staticmethod
    def convert_html_to_pdf(
        html: typing.Union[str, ET.Element],
        fallback_fonts_regular: typing.List[Font] = [StandardType1Font("Helvetica")],
        fallback_fonts_bold: typing.List[Font] = [StandardType1Font("Helvetica-Bold")],
        fallback_fonts_italic: typing.List[Font] = [StandardType1Font("Helvetica-Oblique")],
        fallback_fonts_bold_italic: typing.List[Font] = [StandardType1Font("Helvetica-Bold-Oblique")],
        fallback_fonts_monospaced: typing.List[Font] = [StandardType1Font("Courier")],
    ) -> Document:
        """
        This function converts HTML to PDF
        """

        # Document
        doc: Document = Document()

        # Page
        page: Page = Page()
        doc.add_page(page)

        # PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        # parse HTML
        root_element: typing.Optional[ET.Element] = None
        if isinstance(html, str):
            root_element = ET.fromstring(html, HTMLParser())
        else:
            root_element = html
        assert root_element is not None

        # build Context
        c: HTMLToPDF.Context = HTMLToPDF.Context()
        c._document = doc
        c._fallback_fonts_regular = fallback_fonts_regular
        c._fallback_fonts_bold = fallback_fonts_bold
        c._fallback_fonts_italic = fallback_fonts_italic
        c._fallback_fonts_bold_italic = fallback_fonts_bold_italic
        c._fallback_fonts_monospaced = fallback_fonts_monospaced

        # convert HTML to PDF
        layout.add(HTMLToPDF._process_html_element(root_element, c))

        # return
        return doc
