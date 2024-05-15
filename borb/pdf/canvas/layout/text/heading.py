#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement acts just like Paragraph.
It also adds an outline in the document outline tree.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class Heading(Paragraph):
    """
    This implementation of LayoutElement acts just like Paragraph.
    It also adds an outline in the document outline tree.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        fixed_leading: typing.Optional[Decimal] = None,
        font: typing.Union[Font, str] = "Helvetica",
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        hyphenation: typing.Optional[Hyphenation] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        multiplied_leading: typing.Optional[Decimal] = None,
        outline_level: int = 0,
        outline_text: typing.Optional[str] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        respect_newlines_in_text: bool = False,
        respect_spaces_in_text: bool = False,
        text_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super().__init__(
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            fixed_leading=fixed_leading,
            font=font,
            font_color=font_color,
            font_size=font_size,
            horizontal_alignment=horizontal_alignment,
            hyphenation=hyphenation,
            margin_bottom=margin_bottom
            if margin_bottom is not None
            else Heading._get_margin_for_outline_level(outline_level, font_size),
            margin_left=margin_left or Decimal(0),
            margin_right=margin_right or Decimal(0),
            margin_top=margin_top
            if margin_top is not None
            else Heading._get_margin_for_outline_level(outline_level, font_size),
            multiplied_leading=multiplied_leading,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            respect_newlines_in_text=respect_newlines_in_text,
            respect_spaces_in_text=respect_spaces_in_text,
            text=text,
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
        )
        self._outline_text = outline_text or text
        self._outline_level = outline_level
        self._has_added_outline = False

    #
    # PRIVATE
    #

    @staticmethod
    def _get_margin_for_outline_level(
        outline_level: int = 0, font_size: Decimal = Decimal(12)
    ) -> Decimal:
        return {
            1: Decimal(0.335),
            2: Decimal(0.553),
            3: Decimal(0.855),
            4: Decimal(1.333),
            5: Decimal(2.012),
            6: Decimal(3.477),
        }.get(outline_level + 1, Decimal(1)) * font_size

    #
    # PUBLIC
    #

    def paint(self, page: Page, available_space: Rectangle):
        """
        This method paints this LayoutElement on the given Page, in the available space
        :param page:                the Page on which to paint this LayoutElement
        :param available_space:     the available space (as a Rectangle) on which to paint this LayoutElement
        :return:                    None
        """

        # fetch document
        p = page.get_root()
        assert isinstance(p, Document)

        # add outline to document
        if not self._has_added_outline:
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

        # call super
        super(Heading, self).paint(page, available_space)
