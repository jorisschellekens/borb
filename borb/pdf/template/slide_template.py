#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents an easy way to manipulate a PDF document
that looks like a slideshow
"""
import io
import random
import typing
from decimal import Decimal
import pathlib

# fmt: off
from borb.pdf.canvas.layout.shape.shapes import Shapes
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.geography.map_of_europe import MapOfEurope
from borb.pdf.canvas.layout.geography.map_of_the_united_states import MapOfTheUnitedStates
from borb.pdf.canvas.layout.geography.map_of_the_world import MapOfTheWorld
from borb.pdf.canvas.layout.image.barcode import Barcode
from borb.pdf.canvas.layout.image.barcode import BarcodeType
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.codeblock_with_syntax_highlighting import CodeBlockWithSyntaxHighlighting
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


# fmt: on


class SlideTemplate:
    """
    This class represents an easy way to manipulate a PDF document
    that looks like a slideshow
    """

    ACCENT_COLOR: Color = HexColor("#0b3954")
    LIGHT_GRAY_COLOR: Color = HexColor("#eeeeee")
    DARK_GRAY_COLOR: Color = HexColor("#595959")

    BIG_NUMBER_TEXT_FONTSIZE_MAX: int = 300
    BIG_NUMBER_TEXT_FONTSIZE_MIN: int = 20
    BIG_NUMBER_TEXT_FONTSIZE_STEP: int = 10

    QUOTE_TEXT_FONTSIZE_MAX: int = 300
    QUOTE_TEXT_FONTSIZE_MIN: int = 20
    QUOTE_TEXT_FONTSIZE_STEP: int = 10

    TABLE_TEXT_FONTSIZE_MAX: int = 100
    TABLE_TEXT_FONTSIZE_MIN: int = 12
    TABLE_TEXT_FONTSIZE_STEP: int = 2

    SUBTITLE_FONTSIZE: int = 18
    TEXT_FONTSIZE: int = 12
    TITLE_FONTSIZE: int = 20

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._document: Document = Document()
        self._slides_to_be_numbered: typing.List[int] = []

    #
    # PRIVATE
    #

    def _add_page_numbers(self) -> None:
        for i in self._slides_to_be_numbered:
            s: Page = self._document.get_page(i)
            Paragraph(
                f"{i+1}",
                font_size=Decimal(10),
                font_color=SlideTemplate.LIGHT_GRAY_COLOR,
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )

    def _blank_slide(self) -> Page:
        p: Page = Page(width=Decimal(950), height=Decimal(540))
        self._document.add_page(p)
        return p

    def _split_in_half_slide(
        self,
        subtitle: typing.Optional[str],
        text: typing.Optional[str],
        title: typing.Optional[str],
    ) -> Page:
        # create blank slide
        s: Page = self._blank_slide()

        # add gray rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(
                    Decimal(950 // 2), Decimal(0), Decimal(950 // 2), Decimal(540)
                )
            ),
            stroke_color=SlideTemplate.LIGHT_GRAY_COLOR,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(950 // 2), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # add blue rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47)
            ),
        )

        # mark slide as "has to be numbered"
        page_nr: typing.Optional[int] = None
        number_of_pages: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, number_of_pages):
            if self._document.get_page(i) == s:
                page_nr = i
                break
        assert page_nr is not None
        self._slides_to_be_numbered.append(page_nr)

        # add title
        prev_bottom_y: Decimal = Decimal(540)
        must_have_top_padding: bool = True
        if title is not None:
            p0 = Paragraph(
                title,
                font_size=Decimal(SlideTemplate.TITLE_FONTSIZE),
                padding_top=Decimal(540 // 10),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(950 // 2), Decimal(0), Decimal(950 // 2), Decimal(540)
                ),
            )
            p0_prev_paint_box: typing.Optional[Rectangle] = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # add subtitle
        if subtitle is not None:
            p0 = Paragraph(
                subtitle,
                font_color=SlideTemplate.DARK_GRAY_COLOR,
                font_size=Decimal(SlideTemplate.SUBTITLE_FONTSIZE),
                padding_top=Decimal(540 // 10) if must_have_top_padding else Decimal(0),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(950 // 2), Decimal(0), Decimal(950 // 2), prev_bottom_y
                ),
            )
            p0_prev_paint_box = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # text
        if text is not None:
            Paragraph(
                text,
                font_size=Decimal(SlideTemplate.TEXT_FONTSIZE),
                padding_top=Decimal(540 // 10) if must_have_top_padding else Decimal(0),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(950 // 2), Decimal(0), Decimal(950 // 2), prev_bottom_y
                ),
            )

        # return
        return s

    #
    # PUBLIC
    #

    def add_barchart_and_text_slide(
        self,
        xs: typing.List[float],
        labels: typing.List[str],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a barchart (on the left side)
        and a title, subtitle and text (on the right side)
        :param xs           the x-data series
        :param labels       the labels of the series
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :param y_label      the label on the y-axis
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # create matplotlib plot
        import matplotlib.pyplot  # type: ignore[import]

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(labels, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)
        # fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_barchart_slide(
        self,
        xs: typing.List[float],
        labels: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a barchart
        as big as it can be, centered horizontally and vertically on the page
        :param xs           the x-data series
        :param labels       the labels of the series
        :param y_label      the label on the y-axis
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(labels, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)
        # fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_big_number_and_text_slide(
        self,
        big_number: str,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a large number (on the left side)
        and a title, subtitle and text (on the right side)
        :param big_number:  the big number to be added (e.g. "84%")
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add big number
        for font_size in range(
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MAX,
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MIN,
            -SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
        ):
            try:
                Paragraph(
                    big_number,
                    horizontal_alignment=Alignment.CENTERED,
                    vertical_alignment=Alignment.MIDDLE,
                    font="Helvetica-Bold",
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                    font_size=Decimal(font_size),
                    font_color=SlideTemplate.ACCENT_COLOR,
                ).paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_big_number_slide(self, big_number: str) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a large number
        as big as it can be, centered horizontally and vertically on the page
        :param big_number:  the big number to be added (e.g. "84%")
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # add big number
        for font_size in range(
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MAX,
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MIN,
            -SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
        ):
            try:
                Paragraph(
                    big_number,
                    horizontal_alignment=Alignment.CENTERED,
                    vertical_alignment=Alignment.MIDDLE,
                    font="Helvetica-Bold",
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                    font_size=Decimal(font_size),
                    font_color=SlideTemplate.ACCENT_COLOR,
                ).paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_blank_slide(
        self, disclaimer_text: str = "This slide intentionally left blank."
    ) -> "SlideTemplate":
        """
        This function adds a blank slide to this SlideTemplate, possibly containing a disclaimer as to why this slide is blank.
        Such as "Slide intentionally left blank"
        :param disclaimer_text  the disclaimer text
        :return:                self
        """
        s: Page = self._blank_slide()
        Paragraph(
            disclaimer_text,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            font_size=Decimal(SlideTemplate.TEXT_FONTSIZE // 2),
            font_color=SlideTemplate.LIGHT_GRAY_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )
        return self

    def add_code_and_text_slide(
        self,
        code: str,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ):
        """
        This function adds a slide to this SlideTemplate containing a block of code (on the left side)
        and a title, subtitle and text (on the right side)
        :param code         the code to be displayed
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add CodeBlockWithSyntaxHighlighting
        for font_size in range(
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MAX,
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
            -SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
        ):
            try:
                CodeBlockWithSyntaxHighlighting(
                    code,
                    horizontal_alignment=Alignment.CENTERED,
                    vertical_alignment=Alignment.MIDDLE,
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                    font_size=Decimal(font_size),
                    font_color=SlideTemplate.ACCENT_COLOR,
                ).paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_code_slide(self, code: str) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a block of code
        as big as it can be, centered horizontally and vertically on the page
        :param big_number:  the code to be added
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # add CodeBlockWithSyntaxHighlighting
        for font_size in range(
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_MAX,
            SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
            -SlideTemplate.BIG_NUMBER_TEXT_FONTSIZE_STEP,
        ):
            try:
                CodeBlockWithSyntaxHighlighting(
                    code,
                    horizontal_alignment=Alignment.CENTERED,
                    vertical_alignment=Alignment.MIDDLE,
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                    font_size=Decimal(font_size),
                    font_color=SlideTemplate.ACCENT_COLOR,
                ).paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_image_and_text_slide(
        self,
        image_url: str,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an image (on the left side)
        and a title, subtitle and text (on the right side)
        :param image_url    the URL for the image being displayed
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # image
        Image(
            image_url,
            width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_image_slide(self, image_url: str) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an image
        as big as it can be, centered horizontally and vertically on the page
        :param image_url    the URL of the image to be added
        :return:            self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # image
        Image(image_url, width=Decimal(950), height=Decimal(540)).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_linechart_and_text_slide(
        self,
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        labels: typing.List[str],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a linechart (on the left side)
        and a title, subtitle and text (on the right side)
        :param xs           the x-data series
        :param ys           the y-data series
        :param labels       the labels of the series
        :param x_label      the label for the x-axis
        :param y_label      the label for the y-axis
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_linechart_slide(
        self,
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        labels: typing.List[str],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a linechart
        as big as it can be, centered horizontally and vertically on the page
        :param xs           the x-data series
        :param ys           the y-data series
        :param labels       the labels of the series
        :param x_label      the label for the x-axis
        :param y_label      the label for the y-axis
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_map_of_europe_and_text_slide(
        self,
        marked_countries: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of Europe (on the left side)
        and a title, subtitle and text (on the right side)
        :param marked_countries:    the countries to be marked
        :param subtitle:            the subtitle
        :param text:                the text
        :param title:               the title
        :return:                    self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add map
        m = MapOfEurope(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        m.scale_up(
            max_width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_countries:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_map_of_europe_slide(
        self, marked_countries: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of Europe
        as big as it can be, centered horizontally and vertically on the page
        :param marked_countries:    the countries that ought to be marked
        :return:                    self
        """
        s: Page = self._blank_slide()
        # add map
        m = MapOfEurope(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        )
        m.scale_up(
            max_width=Decimal(950 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_countries:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )
        return self

    def add_map_of_the_contiguous_united_states_and_text_slide(
        self,
        marked_states: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the (contiguous) United States (on the left side)
        and a title, subtitle and text (on the right side)
        :param marked_states    the states that ought to be marked
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add map
        m = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        m.pop("Alaska")
        m.pop("American Samoa")
        m.pop("Commonwealth of the Northern Mariana Islands")
        m.pop("District of Columbia")
        m.pop("Guam")
        m.pop("Hawaii")
        m.pop("Puerto Rico")
        m.pop("United States Virgin Islands")
        m.scale_up(
            max_width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_states:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_map_of_the_contiguous_united_states_slide(
        self, marked_states: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the (contiguous) United States
        as big as it can be, centered horizontally and vertically on the page
        :param marked_states    the states that ought to be marked
        :return:                self
        """
        s: Page = self._blank_slide()
        # add map
        m = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        )
        m.pop("Alaska")
        m.pop("American Samoa")
        m.pop("Commonwealth of the Northern Mariana Islands")
        m.pop("District of Columbia")
        m.pop("Guam")
        m.pop("Hawaii")
        m.pop("Puerto Rico")
        m.pop("United States Virgin Islands")
        m.scale_up(
            max_width=Decimal(950 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_states:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )
        return self

    def add_map_of_the_united_states_and_text_slide(
        self,
        marked_states: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the United States (on the left side)
        and a title, subtitle and text (on the right side)
        :param marked_states    the states that ought to be marked
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add map
        m = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        for c in marked_states:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_map_of_the_united_states_slide(
        self, marked_states: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the United States
        as big as it can be, centered horizontally and vertically on the page
        :param marked_states    the states that ought to be marked
        :return:                self
        """
        s: Page = self._blank_slide()
        # add map
        m = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        )
        m.scale_up(
            max_width=Decimal(950 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_states:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )
        return self

    def add_map_of_the_world_and_text_slide(
        self,
        marked_countries: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the world (on the left side)
        and a title, subtitle and text (on the right side)
        :param marked_countries the countries that ought to be marked
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add map
        m = MapOfTheWorld(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        for c in marked_countries:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_map_of_the_world_slide(
        self, marked_countries: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a map of the world
        as big as it can be, centered horizontally and vertically on the page
        :param marked_countries     the countries that ought to be marked
        :return:                    self
        """
        s: Page = self._blank_slide()
        # add map
        m: Shapes = MapOfTheWorld(
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            fill_color=SlideTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        )
        m = m.scale_up(
            max_width=Decimal(950 - 540 // 10 - 540 // 10),
            max_height=Decimal(540 - 540 // 10 - 540 // 10),
        )
        for c in marked_countries:
            m.set_fill_color(fill_color=SlideTemplate.ACCENT_COLOR, key=c)  # type: ignore[attr-defined]
        m.paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )
        return self

    def add_ordered_list_and_text_slide(
        self,
        list_items: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an ordered list (on the left side)
        and a title, subtitle and text (on the right side)
        :param list_items:      the items in the list
        :param subtitle:        the subtitle
        :param text:            the text
        :param title:           the title
        :return:                self
        """
        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                ol: OrderedList = OrderedList(
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                )
                for li in list_items:
                    ol.add(
                        Paragraph(
                            li,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                ol.paint(
                    s,
                    Rectangle(Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)),
                )
                break
            except:
                pass

        # return
        return self

    def add_ordered_list_slide(
        self, list_items: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an ordered list
        as big as it can be, centered horizontally and vertically on the page
        :param list_items:  the items in the list
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                ol: OrderedList = OrderedList(
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                )
                for li in list_items:
                    ol.add(
                        Paragraph(
                            li,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                ol.paint(
                    s,
                    Rectangle(Decimal(0), Decimal(0), Decimal(950), Decimal(540)),
                )
                break
            except:
                pass

        # return
        return self

    def add_piechart_and_text_slide(
        self,
        xs: typing.List[float],
        labels: typing.Optional[typing.List[str]],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a piechart (on the left side)
        and a title, subtitle and text (on the right side)
        :param xs           the x-data series
        :param labels       the labels of the series
        :param subtitle:    the subtitle
        :param text:        the title
        :param title:       the text
        :return:            self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        should_explode = tuple(
            [1 if xs[i] == max(xs) else 0 for i in range(0, len(xs))]
        )
        ax.pie(xs, labels=labels, explode=should_explode)
        fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 // 2 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_piechart_slide(
        self,
        xs: typing.List[float],
        labels: typing.Optional[typing.List[str]],
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a piechart
        as big as it can be, centered horizontally and vertically on the page
        :param xs           the x-data series
        :param labels       the labels of the series
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        should_explode = tuple(
            [1 if xs[i] == max(xs) else 0 for i in range(0, len(xs))]
        )
        ax.pie(xs, labels=labels, explode=should_explode)
        fig.legend(loc="outside lower center")

        # add chart
        Chart(
            matplotlib.pyplot,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
            width=Decimal(950 - 540 // 10 - 540 // 10),
            height=Decimal(540 - 540 // 10 - 540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_qr_code_and_text_slide(
        self,
        data: str,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a QR code (on the left side)
        and a title, subtitle and text (on the right side)
        :param data:        the data to be encoded in the QR code (e.g. a URL)
        :param subtitle:    the subtitle
        :param text:        the text
        :param title:       the title
        :return:            self
        """
        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # image
        Barcode(
            data,
            type=BarcodeType.QR,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            stroke_color=SlideTemplate.ACCENT_COLOR,
            width=Decimal(366),
            height=Decimal(366),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
            ),
        )

        # return
        return self

    def add_qr_code_slide(
        self,
        data: str,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a QR code
        as big as it can be, centered horizontally and vertically on the page
        :param data:    the data to be encoded in the QR code (e.g. a URL)
        :return:        self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # image
        Barcode(
            data,
            type=BarcodeType.QR,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
            stroke_color=SlideTemplate.ACCENT_COLOR,
            width=Decimal(431),
            height=Decimal(431),
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        # return
        return self

    def add_quote_and_text_slide(
        self,
        quote_author: str,
        quote_text: str,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a quote and its author (on the left side)
        and a title, subtitle and text (on the right side)
        :param quote_author     the author of the quote
        :param quote_text       the text of the quote
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """
        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                (
                    FixedColumnWidthTable(
                        number_of_columns=1,
                        number_of_rows=2,
                        padding_top=Decimal(540 // 10),
                        padding_right=Decimal(540 // 10),
                        padding_bottom=Decimal(540 // 10),
                        padding_left=Decimal(540 // 10),
                    )
                    .add(
                        Paragraph(
                            quote_text,
                            text_alignment=Alignment.JUSTIFIED,
                            horizontal_alignment=Alignment.CENTERED,
                            vertical_alignment=Alignment.MIDDLE,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                    .add(
                        Paragraph(
                            quote_author,
                            horizontal_alignment=Alignment.RIGHT,
                            vertical_alignment=Alignment.MIDDLE,
                            font="Helvetica-Oblique",
                            font_size=Decimal(20),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                    .no_borders()
                    .paint(
                        s,
                        Rectangle(
                            Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
                        ),
                    )
                )
                break
            except:
                pass

        # return
        return self

    def add_quote_slide(self, quote_author: str, quote_text: str) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a quote and its author
        as big as it can be, centered horizontally and vertically on the page
        :param quote_author     the author of the quote
        :param quote_text       the text of the quote
        :return:                self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                (
                    FixedColumnWidthTable(
                        number_of_columns=1,
                        number_of_rows=2,
                        padding_top=Decimal(540 // 10),
                        padding_right=Decimal(540 // 10),
                        padding_bottom=Decimal(540 // 10),
                        padding_left=Decimal(540 // 10),
                        horizontal_alignment=Alignment.CENTERED,
                        vertical_alignment=Alignment.MIDDLE,
                    )
                    .add(
                        Paragraph(
                            quote_text,
                            text_alignment=Alignment.JUSTIFIED,
                            horizontal_alignment=Alignment.CENTERED,
                            vertical_alignment=Alignment.MIDDLE,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                    .add(
                        Paragraph(
                            quote_author,
                            horizontal_alignment=Alignment.RIGHT,
                            vertical_alignment=Alignment.MIDDLE,
                            font="Helvetica-Oblique",
                            font_size=Decimal(20),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                    .no_borders()
                    .paint(
                        s,
                        Rectangle(Decimal(0), Decimal(0), Decimal(950), Decimal(540)),
                    )
                )
                break
            except:
                pass

        # return
        return self

    def add_section_title_slide(
        self,
        nr: str,
        subtitle: str,
        title: str,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a section title.
        The slide is styled with an image, and a color accent
        :param nr           the nr (e.g. '2b')
        :param subtitle     the subtitle
        :param title        the title
        :return:            self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add Image
        image_url: str = random.choice(
            [
                "https://images.unsplash.com/photo-1551041181-cacd7047d18d",
                "https://images.unsplash.com/photo-1555859623-1caf19ff9bbb",
                "https://images.unsplash.com/photo-1560174038-da43ac74f01b",
                "https://images.unsplash.com/photo-1561700398-b25aeb4454fc",
                "https://images.unsplash.com/photo-1439337153520-7082a56a81f4",
                "https://images.unsplash.com/photo-1476891626313-2cecb3820a69",
                "https://images.unsplash.com/photo-1490004531003-9bda21d243db",
                "https://images.unsplash.com/photo-1495745713439-7efd16a9555c",
                "https://images.unsplash.com/photo-1504019853082-9a4cb128c1ef",
                "https://images.unsplash.com/photo-1521035227181-90af4feddc6c",
                "https://images.unsplash.com/photo-1524230572899-a752b3835840",
                "https://images.unsplash.com/photo-1527576539890-dfa815648363",
                "https://images.unsplash.com/photo-1527698334848-f475f9d99449",
                "https://images.unsplash.com/photo-1532374281774-97f9514fcfea",
                "https://images.unsplash.com/photo-1574492956703-638af28b0065",
                "https://images.unsplash.com/photo-1582140161604-0b909c97653c",
                "https://images.unsplash.com/photo-1605986740387-0ea0d9168f19",
                "https://plus.unsplash.com/premium_photo-1661880452033-a41bd5e32eae",
            ]
        )
        Image(image_url, width=Decimal(950 // 2.32), height=Decimal(540),).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 2.32), Decimal(540)
            ),
        )

        # add ACCENT_COLOR rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(0), Decimal(0), Decimal(950 // 50), Decimal(540))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 50), Decimal(540)
            ),
        )

        # add nr, title, subtitle
        FixedColumnWidthTable(
            number_of_columns=1,
            number_of_rows=3,
            vertical_alignment=Alignment.MIDDLE,
            horizontal_alignment=Alignment.CENTERED,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        ).add(
            Paragraph(
                nr,
                font="Helvetica-Bold",
                font_color=SlideTemplate.ACCENT_COLOR,
                padding_bottom=Decimal(10),
                font_size=Decimal(20),
            )
        ).add(
            Paragraph(title, font_size=Decimal(30))
        ).add(
            Paragraph(subtitle, font_color=SlideTemplate.DARK_GRAY_COLOR)
        ).no_borders().paint(
            page=s,
            available_space=Rectangle(
                Decimal(950 // 2.32), Decimal(0), Decimal(950 // 2.32), Decimal(540)
            ),
        )

        # return
        return self

    def add_single_column_text_slide(
        self,
        text: str,
        subtitle: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a single column of text
        as big as it can be
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add title
        prev_bottom_y: Decimal = Decimal(540)
        must_have_top_padding: bool = True
        if title is not None:
            p0 = Paragraph(
                title,
                font_size=Decimal(SlideTemplate.TITLE_FONTSIZE),
                padding_top=Decimal(540 // 10),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(0), Decimal(0), Decimal(950), Decimal(540)
                ),
            )
            p0_prev_paint_box: typing.Optional[Rectangle] = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # add subtitle
        if subtitle is not None:
            p0 = Paragraph(
                subtitle,
                font_color=SlideTemplate.DARK_GRAY_COLOR,
                font_size=Decimal(SlideTemplate.SUBTITLE_FONTSIZE),
                padding_top=Decimal(540 // 10) if must_have_top_padding else Decimal(0),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(0), Decimal(0), Decimal(950), prev_bottom_y
                ),
            )
            p0_prev_paint_box = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # add blue rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47)
            ),
        )

        # mark slide as "has to be numbered"
        page_nr: typing.Optional[int] = None
        number_of_pages: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, number_of_pages):
            if self._document.get_page(i) == s:
                page_nr = i
                break
        assert page_nr is not None
        self._slides_to_be_numbered.append(page_nr)

        # add text
        for font_size in range(
            SlideTemplate.TABLE_TEXT_FONTSIZE_MAX,
            SlideTemplate.TABLE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.TABLE_TEXT_FONTSIZE_STEP,
        ):
            try:
                Paragraph(
                    text=text,
                    padding_top=Decimal(540 // 10)
                    if must_have_top_padding
                    else Decimal(font_size),
                    padding_left=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    font_size=Decimal(font_size),
                    text_alignment=Alignment.JUSTIFIED,
                ).paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950), prev_bottom_y
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_table_and_text_slide(
        self,
        tabular_data: typing.List[typing.List[typing.Any]],
        header_col: bool = False,
        header_row: bool = True,
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a table (on the left side)
        and a title, subtitle and text (on the right side)
        :param tabular_data     the tabular data
        :param header_col       whether the first column ought to be marked as a header
        :param header_row       whether the first row ought to be marked as a header
        :param subtitle:        the subtitle
        :param text:            the title
        :param title:           the text
        :return:                self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add tabular data
        for font_size in range(
            SlideTemplate.TABLE_TEXT_FONTSIZE_MAX,
            SlideTemplate.TABLE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.TABLE_TEXT_FONTSIZE_STEP,
        ):
            try:
                t: Table = TableUtil.from_2d_array(
                    tabular_data,
                    header_row=header_row,
                    header_col=header_col,
                    header_background_color=SlideTemplate.ACCENT_COLOR,
                    header_font_color=HexColor("#ffffff"),
                    font_size=Decimal(font_size),
                )
                t._padding_top = Decimal(540 // 10)
                t._padding_right = Decimal(540 // 10)
                t._padding_bottom = Decimal(540 // 10)
                t._padding_left = Decimal(540 // 10)
                t._horizontal_alignment = Alignment.CENTERED
                t._vertical_alignment = Alignment.MIDDLE
                t.set_padding_on_all_cells(
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                )
                t.paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_table_slide(
        self,
        tabular_data: typing.List[typing.List[typing.Any]],
        header_col: bool = False,
        header_row: bool = True,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing a table
        as big as it can be, centered horizontally and vertically on the page
        :param tabular_data     the tabular data
        :param header_col       whether the first column ought to be marked as a header
        :param header_row:      whether the first row ought to be marked as a header
        :return:                self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add tabular data
        for font_size in range(
            SlideTemplate.TABLE_TEXT_FONTSIZE_MAX,
            SlideTemplate.TABLE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.TABLE_TEXT_FONTSIZE_STEP,
        ):
            try:
                t: Table = TableUtil.from_2d_array(
                    tabular_data,
                    header_row=header_row,
                    header_col=header_col,
                    header_background_color=SlideTemplate.ACCENT_COLOR,
                    header_font_color=HexColor("#ffffff"),
                    font_size=Decimal(font_size),
                )
                t.set_padding_on_all_cells(
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                    Decimal(font_size // 3),
                )
                t._padding_top = Decimal(540 // 10)
                t._padding_right = Decimal(540 // 10)
                t._padding_bottom = Decimal(540 // 10)
                t._padding_left = Decimal(540 // 10)
                t._horizontal_alignment = Alignment.CENTERED
                t._vertical_alignment = Alignment.MIDDLE
                t.paint(
                    page=s,
                    available_space=Rectangle(
                        Decimal(0), Decimal(0), Decimal(950), Decimal(540)
                    ),
                )
                break
            except:
                pass

        # return
        return self

    def add_title_slide(
        self, author: str, date: str, subtitle: str, title: str, version: str
    ) -> "SlideTemplate":
        """
        This function adds a title slide to this SlideTemplate. The title slide contains
        a title, subtitle, author, version and date
        :param author:      the author
        :param date:        the date
        :param subtitle:    the subtitle
        :param title:       the title
        :param version:     the version
        :return:            self
        """

        # create blank slide
        s: Page = self._blank_slide()

        # add ACCENT_COLOR rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(0), Decimal(0), Decimal(950 // 50), Decimal(540))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950 // 50), Decimal(540)
            ),
        )

        # add ACCENT_COLOR rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(0), Decimal(0), Decimal(950), Decimal(950 // 50))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(950 // 50)
            ),
        )

        # add title, subtitle, date - version
        FixedColumnWidthTable(
            number_of_columns=1,
            number_of_rows=3,
            vertical_alignment=Alignment.MIDDLE,
            horizontal_alignment=Alignment.CENTERED,
            padding_top=Decimal(540 // 10),
            padding_right=Decimal(540 // 10),
            padding_bottom=Decimal(540 // 10),
            padding_left=Decimal(540 // 10),
        ).add(
            Paragraph(
                title,
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.CENTERED,
                font_color=SlideTemplate.ACCENT_COLOR,
                font_size=Decimal(40),
            )
        ).add(
            Paragraph(
                subtitle,
                horizontal_alignment=Alignment.CENTERED,
                font_color=SlideTemplate.DARK_GRAY_COLOR,
                font_size=Decimal(20),
            )
        ).add(
            Paragraph(
                f"{date}, {version}",
                font_size=Decimal(10),
                horizontal_alignment=Alignment.CENTERED,
                font_color=SlideTemplate.LIGHT_GRAY_COLOR,
            )
        ).no_borders().paint(
            page=s,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(950), Decimal(540)
            ),
        )

        return self

    def add_two_column_text_slide(
        self,
        text_left: str,
        text_right: str,
        subtitle: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing two columns of text
        :param text_left        the text on the left side
        :param text_right       the text on the right side
        :param subtitle:        the subtitle
        :param text:            the title
        :return:                self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add title
        prev_bottom_y: Decimal = Decimal(540)
        must_have_top_padding: bool = True
        if title is not None:
            p0 = Paragraph(
                title,
                font_size=Decimal(SlideTemplate.TITLE_FONTSIZE),
                padding_top=Decimal(540 // 10),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(0), Decimal(0), Decimal(950), Decimal(540)
                ),
            )
            p0_prev_paint_box: typing.Optional[Rectangle] = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # add subtitle
        if subtitle is not None:
            p0 = Paragraph(
                subtitle,
                font_color=SlideTemplate.DARK_GRAY_COLOR,
                font_size=Decimal(SlideTemplate.SUBTITLE_FONTSIZE),
                padding_top=Decimal(540 // 10) if must_have_top_padding else Decimal(0),
                padding_right=Decimal(540 // 10),
                padding_left=Decimal(540 // 10),
            )
            p0.paint(
                page=s,
                available_space=Rectangle(
                    Decimal(0), Decimal(0), Decimal(950), prev_bottom_y
                ),
            )
            p0_prev_paint_box = p0.get_previous_paint_box()
            assert p0_prev_paint_box is not None
            prev_bottom_y = p0_prev_paint_box.get_y()
            must_have_top_padding = False

        # add blue rectangle
        ConnectedShape(
            LineArtFactory.rectangle(
                Rectangle(Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47))
            ),
            stroke_color=SlideTemplate.ACCENT_COLOR,
            fill_color=SlideTemplate.ACCENT_COLOR,
        ).paint(
            page=s,
            available_space=Rectangle(
                Decimal(950 - 47), Decimal(0), Decimal(47), Decimal(47)
            ),
        )

        # mark slide as "has to be numbered"
        page_nr: typing.Optional[int] = None
        number_of_pages: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, number_of_pages):
            if self._document.get_page(i) == s:
                page_nr = i
                break
        assert page_nr is not None
        self._slides_to_be_numbered.append(page_nr)

        # add text_left, text_right
        for font_size in range(
            SlideTemplate.TABLE_TEXT_FONTSIZE_MAX,
            SlideTemplate.TABLE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.TABLE_TEXT_FONTSIZE_STEP,
        ):
            try:
                (
                    FixedColumnWidthTable(
                        number_of_columns=2,
                        number_of_rows=1,
                        padding_left=Decimal(540 // 10),
                        padding_top=Decimal(540 // 10)
                        if must_have_top_padding
                        else Decimal(font_size),
                        padding_bottom=Decimal(540 // 10),
                        padding_right=Decimal(540 // 10),
                    )
                    .add(
                        TableCell(
                            Paragraph(
                                text_left,
                                font_size=Decimal(font_size),
                                text_alignment=Alignment.JUSTIFIED,
                            ),
                            padding_right=Decimal(540 // 20),
                        )
                    )
                    .add(
                        TableCell(
                            Paragraph(
                                text_right,
                                font_size=Decimal(font_size),
                                text_alignment=Alignment.JUSTIFIED,
                            ),
                            padding_left=Decimal(540 // 20),
                        )
                    )
                    .no_borders()
                    .paint(
                        page=s,
                        available_space=Rectangle(
                            Decimal(0), Decimal(0), Decimal(950), prev_bottom_y
                        ),
                    )
                )
                break
            except:
                pass

        #
        return self

    def add_unordered_list_and_text_slide(
        self,
        list_items: typing.List[str] = [],
        subtitle: typing.Optional[str] = None,
        text: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an unordered list (on the left side)
        and a title, subtitle and text (on the right side)
        :param list_items:      the items in the list
        :param subtitle:        the subtitle
        :param text:            the text
        :param title:           the title
        :return:                self
        """

        # create blank slide
        s: Page = self._split_in_half_slide(subtitle=subtitle, text=text, title=title)

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                ol: UnorderedList = UnorderedList(
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                )
                for li in list_items:
                    ol.add(
                        Paragraph(
                            li,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                ol.paint(
                    s,
                    Rectangle(Decimal(0), Decimal(0), Decimal(950 // 2), Decimal(540)),
                )
                break
            except:
                pass

        # return
        return self

    def add_unordered_list_slide(
        self, list_items: typing.List[str] = []
    ) -> "SlideTemplate":
        """
        This function adds a slide to this SlideTemplate containing an unordered list
        as big as it can be, centered horizontally and vertically on the page
        :param list_items:  the items in the list
        :return:            self
        """
        # create blank slide
        s: Page = self._blank_slide()

        # add quote
        for font_size in range(
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MAX,
            SlideTemplate.QUOTE_TEXT_FONTSIZE_MIN,
            -SlideTemplate.QUOTE_TEXT_FONTSIZE_STEP,
        ):
            try:
                ol: UnorderedList = UnorderedList(
                    padding_top=Decimal(540 // 10),
                    padding_right=Decimal(540 // 10),
                    padding_bottom=Decimal(540 // 10),
                    padding_left=Decimal(540 // 10),
                )
                for li in list_items:
                    ol.add(
                        Paragraph(
                            li,
                            font="Helvetica-Bold",
                            font_size=Decimal(font_size),
                            font_color=SlideTemplate.ACCENT_COLOR,
                        )
                    )
                ol.paint(
                    s,
                    Rectangle(Decimal(0), Decimal(0), Decimal(950), Decimal(540)),
                )
                break
            except:
                pass

        # return
        return self

    def bytes(self) -> bytes:
        """
        This function returns the bytes representing this SlideTemplate.
        It does so by saving this SlideTemplate to an io.BytesIO buffer,
        and returning its bytes.
        :return:    the bytes representing this SlideTemplate
        """
        self._add_page_numbers()
        buffer = io.BytesIO()
        PDF.dumps(buffer, self._document)
        buffer.seek(0)
        return buffer.getvalue()

    def save(self, path_or_str: typing.Union[str, pathlib.Path]) -> "SlideTemplate":
        """
        This function stores this SlideTemplate at the given path
        :param path_or_str:     the path or str representing the location at which to store this SlideTemplate
        :return:                self
        """
        self._add_page_numbers()
        with open(path_or_str, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self._document)
        return self
