#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class converts Markdown to PDF
"""
import typing
import xml.etree.ElementTree
from decimal import Decimal

from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.emoji.emoji import Emojis
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.document.document import Document
from borb.pdf.page.page_size import PageSize
from borb.toolkit.export.html_to_pdf.html_to_pdf import HTMLToPDF


class MarkdownToPDF:
    """
    This class converts Markdown to PDF
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _replace_github_flavored_emoji(e: "Element", parents: typing.List["Element"] = []) -> "Element":  # type: ignore[name-defined]
        # do not modify emoji elements themselves
        if e.tag == "span" and "emoji" in e.get("class", "").split(" "):
            return e

        import lxml.etree  # type: ignore[import]

        TAGS_TO_IGNORE: typing.List[str] = ["code", "pre"]
        element_can_be_changed: bool = (
            len([True for x in parents if x.tag in TAGS_TO_IGNORE]) == 0
            and e.tag not in TAGS_TO_IGNORE
        )

        # change text
        text_exists: bool = e.text is not None and len(e.text) > 0
        if text_exists and element_can_be_changed:
            for k, v in [(":" + x.lower() + ":", x) for x in dir(Emojis)]:
                if k in e.text:
                    n: int = e.text.find(k)
                    before: str = e.text[0:n]
                    after: str = e.text[n + len(k) :]
                    e.text = before

                    # create <span> element
                    span: lxml.etree.Element = lxml.etree.Element("span")
                    span.set("class", "emoji emoji_%s" % v)
                    span.text = k
                    span.tail = after

                    # insert new element
                    e.insert(0, span)

        # recurse for children
        for x in e:
            MarkdownToPDF._replace_github_flavored_emoji(x, parents + [e])

        # change tail
        tail_exists: bool = e.tail is not None and len(e.tail) > 0
        if tail_exists and element_can_be_changed:
            for k, v in [(":" + x.lower() + ":", x) for x in dir(Emojis)]:
                if k in e.tail:
                    n = e.tail.find(k)
                    before = e.tail[0:n]
                    after = e.tail[n + len(k) :]
                    e.tail = after

                    # create <span> element
                    span = lxml.etree.Element("span")
                    span.set("class", "emoji emoji_%s" % v)
                    span.text = k
                    span.tail = before

                    # insert new element
                    parent: lxml.etree.Element = parents[-1]
                    index_of_e_in_parent: int = [
                        i for i, x in enumerate(parent) if x == e
                    ][0]
                    parent.insert(index_of_e_in_parent, span)

        # return
        return e

    @staticmethod
    def _set_img_width_and_height(e: "lxml.etree.Element") -> "lxml.etree.Element":  # type: ignore[name-defined]
        if e.tag == "img":
            w: typing.Optional[int] = e.attrib["width"] if "width" in e.attrib else None
            h: typing.Optional[int] = (
                e.attrib["height"] if "height" in e.attrib else None
            )
            if (
                w is None
                or h is None
                or w > PageSize.A4_PORTRAIT.value[0]
                or h > PageSize.A4_PORTRAIT.value[1]
            ):
                w = int(PageSize.A4_PORTRAIT.value[0] * Decimal(0.8))
                h = int(w * 0.618)
                e.attrib["width"] = str(w)
                e.attrib["height"] = str(h)
        for x in e:
            MarkdownToPDF._set_img_width_and_height(x)
        return e

    #
    # PUBLIC
    #

    @staticmethod
    def convert_markdown_to_layout_element(
        # fmt: off
        markdown: str,
        fallback_fonts_regular: typing.List[Font] = [StandardType1Font("Helvetica")],
        fallback_fonts_bold: typing.List[Font] = [StandardType1Font("Helvetica-Bold")],
        fallback_fonts_italic: typing.List[Font] = [StandardType1Font("Helvetica-Oblique")],
        fallback_fonts_bold_italic: typing.List[Font] = [StandardType1Font("Helvetica-Bold-Oblique")],
        # fmt: on
    ) -> LayoutElement:
        """
        This function converts a markdown str to a LayoutElement
        :param markdown:                    the markdown str to be converted
        :param fallback_fonts_regular:      fallback (regular) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold:         fallback (bold) fonts to try when the default font is unable to render a character
        :param fallback_fonts_italic:       fallback (italic) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold_italic:  fallback (bold, italic) fonts to try when the default font is unable to render a character
        :return:
        """

        # markdown to HTML
        import markdown_it  # type: ignore[import]
        import lxml.etree  # type: ignore[import]

        html: str = markdown_it.MarkdownIt().enable("table").render(markdown)
        html_root: xml.etree.ElementTree.Element = xml.etree.ElementTree.fromstring(
            html, lxml.etree.HTMLParser()
        )

        # handle emoji
        html_root = MarkdownToPDF._replace_github_flavored_emoji(html_root)

        # handle img
        html_root = MarkdownToPDF._set_img_width_and_height(html_root)

        # convert HTML
        return HTMLToPDF.convert_html_to_layout_element(
            html_root,
            fallback_fonts_regular,
            fallback_fonts_bold,
            fallback_fonts_italic,
            fallback_fonts_bold_italic,
        )

    @staticmethod
    def convert_markdown_to_pdf(
        # fmt: off
        markdown: str,
        fallback_fonts_regular: typing.List[Font] = [StandardType1Font("Helvetica")],
        fallback_fonts_bold: typing.List[Font] = [StandardType1Font("Helvetica-Bold")],
        fallback_fonts_italic: typing.List[Font] = [StandardType1Font("Helvetica-Oblique")],
        fallback_fonts_bold_italic: typing.List[Font] = [StandardType1Font("Helvetica-Bold-Oblique")],
        # fmt: on
    ) -> Document:
        """
        This function converts a markdown str to a Document
        :param markdown:                    the markdown str to be converted
        :param fallback_fonts_regular:      fallback (regular) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold:         fallback (bold) fonts to try when the default font is unable to render a character
        :param fallback_fonts_italic:       fallback (italic) fonts to try when the default font is unable to render a character
        :param fallback_fonts_bold_italic:  fallback (bold, italic) fonts to try when the default font is unable to render a character
        :return:
        """

        # markdown to HTML
        import markdown_it  # type: ignore[import]
        import lxml.etree  # type: ignore[import]

        html: str = markdown_it.MarkdownIt().enable("table").render(markdown)
        html_root: xml.etree.ElementTree.Element = xml.etree.ElementTree.fromstring(
            html, lxml.etree.HTMLParser()
        )

        # handle emoji
        html_root = MarkdownToPDF._replace_github_flavored_emoji(html_root)

        # handle img
        html_root = MarkdownToPDF._set_img_width_and_height(html_root)

        # convert HTML
        return HTMLToPDF.convert_html_to_pdf(
            html_root,
            fallback_fonts_regular,
            fallback_fonts_bold,
            fallback_fonts_italic,
            fallback_fonts_bold_italic,
        )
