#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement acts just like Paragraph.
It also adds an outline in the document outline tree.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import DestinationType, Page


class Heading(Paragraph):
    """
    This implementation of LayoutElement acts just like Paragraph.
    It also adds an outline in the document outline tree.
    """

    def __init__(
        self,
        text: str,
        outline_text: typing.Optional[str] = None,
        outline_level: int = 0,
        respect_newlines_in_text: bool = False,
        font: typing.Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        font_color: Color = HexColor("000000"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = HexColor("000000"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,  # type: ignore [name-defined]
    ):
        super().__init__(
            text=text,
            respect_newlines_in_text=respect_newlines_in_text,
            font=font,
            font_size=font_size,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            font_color=font_color,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top
            or {
                1: Decimal(0.335),
                2: Decimal(0.553),
                3: Decimal(0.855),
                4: Decimal(1.333),
                5: Decimal(2.012),
                6: Decimal(3.477),
            }.get(outline_level + 1, Decimal(1))
            * font_size,
            margin_right=margin_right or Decimal(0),
            margin_bottom=margin_bottom
            or {
                1: Decimal(0.335),
                2: Decimal(0.553),
                3: Decimal(0.855),
                4: Decimal(1.333),
                5: Decimal(2.012),
                6: Decimal(3.477),
            }.get(outline_level + 1, Decimal(1))
            * font_size,
            margin_left=margin_left or Decimal(0),
            background_color=background_color,
            parent=parent,
        )
        self._outline_text = outline_text or text
        self._outline_level = outline_level
        self._has_added_outline = False

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        layout_rect = super(Heading, self)._do_layout_without_padding(
            page, bounding_box
        )
        if not self._has_added_outline:
            self._add_outline(page)
        return layout_rect

    def _add_outline(self, page: Page):
        # fetch document
        p = page.get_root()  # type: ignore[attr-defined]
        assert isinstance(p, Document)

        # add outline to document
        page_nr = page.get_page_info().get_page_number()
        assert page_nr is not None
        p.add_outline(
            text=self._outline_text,
            level=self._outline_level,
            destination_type=DestinationType.FIT,
            page_nr=int(page_nr),
        )

        # mark
        self._has_added_outline = True
