#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class provides the base for converting a snippet of Markdown
    to PDF syntax.
"""
import re
import typing

from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.browser_layout import BrowserLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.document import Document
from borb.pdf.page.page import Page


class MarkdownTransformerState:
    """
    This class represents all the meta-information used in the process of converting markdown to PDF
    This includes:
    - the root object (the Document itself)
    - the current position in the markdown str
    - etc
    """

    def __init__(self, markdown: str):
        self._markdown_string: str = markdown
        self._start_index: int = 0
        self._document: Document = Document()
        page: Page = Page()
        self._document.append_page(page)
        layout: PageLayout = BrowserLayout(page)
        self._parent_layout_element: typing.Union[
            Document, Page, LayoutElement, PageLayout
        ] = layout

    def tell(self) -> int:
        """
        This function returns the current str position
        """
        return self._start_index

    def seek(self, p: int) -> "MarkdownTransformerState":
        """
        This function changes the str position to the given byte offset.
        This function returns self.
        """
        self._start_index = p
        return self

    def get_markdown_string(self) -> str:
        """
        This function returns the markdown str being transformed
        """
        return self._markdown_string

    def get_document(self) -> Document:
        """
        This function returns the Document being built
        """
        return self._document

    def get_parent_layout_element(
        self,
    ) -> typing.Union[Document, Page, LayoutElement, PageLayout]:
        return self._parent_layout_element


class BaseMarkdownTransformer:
    """
    This class provides the base for converting a snippet of Markdown
    to PDF syntax.
    """

    def __init__(self):
        self._children: typing.List["BaseMarkdownTransformer"] = []
        self._parent: typing.Optional["BaseMarkdownTransformer"] = None

    def add_child_transformer(
        self, transformer: "BaseMarkdownTransformer"
    ) -> "BaseMarkdownTransformer":
        """
        Add a child BaseMarkdownTransformer to this BaseMarkdownTransformer.
        Child transformers can be used to encapsulate specific object-creation/transformation logic.
        e.g. converting bold text, lists, tables, etc
        :param transformer: the BaseMarkdownTransformer implementation to be added
        :type transformer:  BaseMarkdownTransformer
        """
        self._children.append(transformer)
        transformer._parent = self
        return self

    def get_parent(self) -> typing.Optional["BaseMarkdownTransformer"]:
        """
        This function returns the parent BaseMarkdownTransformer.
        BaseMarkdownTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseMarkdownTransformer may delegate
        some of its work to a bold-BaseMarkdownTransformer).
        """
        return self._parent

    def get_root(self) -> "BaseMarkdownTransformer":
        """
        This function returns the root BaseMarkdownTransformer.
        BaseMarkdownTransformer implementations can delegate the transformation
        process to their children (e.g. a paragraph-BaseMarkdownTransformer may delegate
        some of its work to a bold-BaseMarkdownTransformer).
        """
        p = self
        while p._parent is not None:
            p = p._parent
        return p

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        return False

    def _transform(self, context: MarkdownTransformerState) -> None:
        return None

    def _until_double_newline(self, context: MarkdownTransformerState) -> int:
        i: int = context.tell()
        while i < len(context.get_markdown_string()):
            if (
                context.get_markdown_string()[i] == "\n"
                and i + 1 < len(context.get_markdown_string())
                and context.get_markdown_string()[i + 1] == "\n"
            ):
                return i + 1
            i += 1
        return -1

    def _as_long_as_input_lines_match(
        self, line_regex: str, context: MarkdownTransformerState
    ) -> int:
        prev_newline_pos: int = context.tell() - 1
        while prev_newline_pos < len(context.get_markdown_string()):
            # find next newline
            next_newline_pos: int = context.get_markdown_string().find(
                "\n", prev_newline_pos + 1
            )

            # handle end of input
            if next_newline_pos == -1:
                next_newline_pos = len(context.get_markdown_string())

            # determine input line
            line: str = context.get_markdown_string()[
                prev_newline_pos + 1 : next_newline_pos
            ]
            if re.match(line_regex, line) is None:
                return prev_newline_pos

            # set everything up for the next round
            prev_newline_pos = next_newline_pos

        # return
        return prev_newline_pos
