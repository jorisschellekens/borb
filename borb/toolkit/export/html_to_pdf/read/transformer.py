#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents the base implementation of TagTransformer
    A TagTransformer converts a particular HTML tag (e.g. "<h1>") to its corresponding
    LayoutElement object(s).
"""
import typing
import xml.etree.ElementTree as ET

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.chunks_of_text import LineBreakChunk, Span


class TranformerState:
    """
    This class represents all the meta-information used in the process of converting an HTML document to a  PDF document.
    This includes:
    - the root object (the Document itself)
    - the default compression level
    - etc
    """

    # TODO
    pass


class Transformer:
    """
    This class represents the base implementation of TagTransformer
    A TagTransformer converts a particular HTML tag (e.g. "<h1>") to its corresponding
    LayoutElement object(s).
    """

    def __init__(self):
        self._parent: typing.Optional["Transformer"] = None
        self._children: typing.List["Transformer"] = []

    def can_transform(self, html_element: ET.Element):
        """
        This function returns True if this BaseTagTransformer implementation can convert the given ET.Element
        to LayoutElement object(s)
        """
        return False

    def get_parent(self) -> typing.Optional["Transformer"]:
        """
        This function returns the parent BaseTagTransformer.
        BaseTagTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseTagTransformer may delegate
        some of its work to a bold-BaseTagTransformer).
        """
        return self._parent

    def get_root_tag_transformer(self) -> "Transformer":
        """
        This function returns the root BaseTagTransformer.
        BaseTagTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseTagTransformer may delegate
        some of its work to a bold-BaseTagTransformer).
        """
        tmp: "Transformer" = self
        while tmp._parent is not None:
            tmp = tmp._parent
        return tmp

    def get_children(self) -> typing.List["Transformer"]:
        """
        This function returns the child-BaseTagTransformer(s).
        BaseTagTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseTagTransformer may delegate
        some of its work to a bold-BaseTagTransformer).
        """
        return self._children

    def add_child(self, child_tag_transformer: "Transformer") -> "Transformer":
        """
        This function adds a child-BaseTagTransformer to this BaseTagTransformer.
        BaseTagTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseTagTransformer may delegate
        some of its work to a bold-BaseTagTransformer).
        This function returns self.
        """
        self._children.append(child_tag_transformer)
        child_tag_transformer._parent = self
        return self

    def _get_default_font_for_html_element(
        self, html_element_chain: typing.List[ET.Element]
    ):

        # determine whether the font should be italic or not
        tag_chain: typing.List[str] = [x.tag for x in html_element_chain]
        is_bold: bool = ("b" in tag_chain) or ("strong" in tag_chain)
        is_italic: bool = (
            ("i" in tag_chain) or ("em" in tag_chain) or ("address" in tag_chain)
        )

        # font
        font_name: str = "Helvetica"
        if is_bold and is_italic:
            font_name = "Helvetica-bold-oblique"
        elif is_bold:
            font_name = "Helvetica-bold"
        elif is_italic:
            font_name = "Helvetica-oblique"

        # return
        return font_name

    def _correct_spacing_for_chunks_of_text(self, layout_element: Span) -> None:
        for i, c in enumerate(layout_element._chunks_of_text):
            if isinstance(c, LineBreakChunk):
                continue
            next_text_is_punct: bool = False
            if i != len(layout_element._chunks_of_text) - 1:
                next_chunk: ChunkOfText = layout_element._chunks_of_text[i + 1]
                next_text_is_punct = (
                    len(next_chunk._text) > 0 and next_chunk._text[0] in ".,?!;:"
                )
            if not c._text.endswith(" ") and not next_text_is_punct:
                c._text += " "
            if c._text.endswith(" ") and next_text_is_punct:
                c._text = c._text[:-1]

    def transform(
        self,
        html_element: ET.Element,
        parent_elements: typing.List[ET.Element],
        layout_element: typing.Union[PageLayout, LayoutElement],
    ):
        """
        This method transforms an HTML tag to its corresponding LayoutElement(s)
        """
        for c in self.get_children():
            if c.can_transform(html_element):
                c.transform(html_element, parent_elements, layout_element)
                break

    def _contains_only_text_children(self, html_element: ET.Element) -> bool:
        if html_element.tag in ["p", "em", "i", "b", "strong"]:
            return all(
                [
                    self._contains_only_text_children(e)
                    for e in html_element.getchildren()
                ]
            )
        else:
            return False

    def _contains_only_text_or_single_layout_element(
        self, html_element: ET.Element
    ) -> bool:
        if html_element.text is None or len(html_element.text.strip()) == 0:
            return len(html_element.getchildren()) <= 1
        else:
            return all(
                [
                    self._contains_only_text_children(x)
                    for x in html_element.getchildren()
                ]
            )
