#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a PDF document
"""
import io
import typing
from decimal import Decimal
import pathlib

# fmt: off
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
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import TwoColumnLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.codeblock_with_syntax_highlighting import CodeBlockWithSyntaxHighlighting
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF


# fmt: on


class A4PortraitTemplate:
    """
    This class represents an A4 portrait PDF document
    """

    ACCENT_COLOR: Color = HexColor("#0b3954")
    LIGHT_GRAY_COLOR: Color = HexColor("#eeeeee")
    DARK_GRAY_COLOR: Color = HexColor("#595959")

    BODY_FONT_SIZE: Decimal = Decimal(12)
    BODY_FONT_COLOR: Color = HexColor("#000000")
    BODY_FONT: str = "Helvetica"

    H1_FONT_SIZE: Decimal = Decimal(18)
    H1_FONT_COLOR: Color = HexColor("0b3954")
    H1_FONT: str = "Helvetica-Bold"

    H2_FONT_SIZE: Decimal = Decimal(16)
    H2_FONT_COLOR: Color = HexColor("0b3954")
    H2_FONT: str = "Helvetica-Bold"

    H3_FONT_SIZE: Decimal = Decimal(14)
    H3_FONT_COLOR: Color = HexColor("0b3954")
    H3_FONT: str = "Helvetica-Bold"

    H4_FONT_SIZE: Decimal = Decimal(13)
    H4_FONT_COLOR: Color = HexColor("0b3954")
    H4_FONT: str = "Helvetica-Bold-Oblique"

    H5_FONT_SIZE: Decimal = Decimal(12)
    H5_FONT_COLOR: Color = HexColor("0b3954")
    H5_FONT: str = "Helvetica-Bold"

    H6_FONT_SIZE: Decimal = Decimal(12)
    H6_FONT_COLOR: Color = HexColor("0b3954")
    H6_FONT: str = "Helvetica-Bold-Oblique"

    QUOTE_AUTHOR_FONT_SIZE: Decimal = Decimal(12)
    QUOTE_AUTHOR_FONT_COLOR: Color = ACCENT_COLOR
    QUOTE_AUTHOR_FONT: str = "Helvetica-Oblique"

    QUOTE_TEXT_FONT_SIZE: Decimal = Decimal(20)
    QUOTE_TEXT_FONT_COLOR: Color = ACCENT_COLOR
    QUOTE_TEXT_FONT: str = "Helvetica-Bold"

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._document: Document = Document()
        self._page: Page = Page()
        self._document.add_page(self._page)
        self._layout: SingleColumnLayout = SingleColumnLayout(self._page)

    #
    # PRIVATE
    #

    def _add_page_numbers(self) -> None:
        N: int = int(
            self._document.get_document_info().get_number_of_pages() or Decimal(0)
        )
        for i in range(0, N):
            s: Page = self._document.get_page(i)
            # add blue square
            ConnectedShape(
                LineArtFactory.rectangle(
                    Rectangle(Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47))
                ),
                stroke_color=A4PortraitTemplate.ACCENT_COLOR,
                fill_color=A4PortraitTemplate.ACCENT_COLOR,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )
            # add Paragraph
            Paragraph(
                f"{i+1}",
                font_size=Decimal(10),
                font_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
                horizontal_alignment=Alignment.CENTERED,
                vertical_alignment=Alignment.MIDDLE,
            ).paint(
                page=s,
                available_space=Rectangle(
                    Decimal(595 - 47), Decimal(0), Decimal(47), Decimal(47)
                ),
            )

    #
    # PUBLIC
    #

    def add_barchart(
        self,
        xs: typing.List[float],
        labels: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "A4PortraitTemplate":
        """
        This function adds a barchart to this A4PortraitTemplate
        :param xs:          the xs-series
        :param labels:      the labels
        :param y_label:     the label for the y-axis
        :return:            self
        """
        available_width: typing.Optional[Decimal] = Decimal(200)
        available_height: typing.Optional[Decimal] = Decimal(200)

        # create matplotlib plot
        import matplotlib.pyplot  # type: ignore[import]

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(labels, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)
        # fig.legend(loc="outside lower center")

        # add Chart
        self._layout.add(
            Chart(
                matplotlib.pyplot,
                width=available_width,
                height=available_height,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        return self

    def add_blank_page(
        self, disclaimer_text: str = "This page intentionally left blank."
    ) -> "A4PortraitTemplate":
        """
        This function adds a blank Page to this A4PortraitTemplate,
        and then switches to a new Page
        :return:    self
        """
        self._layout.switch_to_next_page()
        self._page = self._layout.get_page()
        Paragraph(
            disclaimer_text,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            font_size=Decimal(A4PortraitTemplate.BODY_FONT_SIZE // 2),
            font_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
        ).paint(
            page=self._page,
            available_space=Rectangle(
                Decimal(0), Decimal(0), Decimal(595), Decimal(842)
            ),
        )
        self._layout.switch_to_next_page()
        self._page = self._layout.get_page()
        return self

    def add_code(self, code: str) -> "A4PortraitTemplate":
        """
        This function adds a CodeBlockWithSyntaxHighlighting to this A4PortraitTemplate
        :param code:    the code to be added
        :return:        self
        """
        self._layout.add(
            CodeBlockWithSyntaxHighlighting(
                code,
                font_size=Decimal(8),
                padding_top=Decimal(8),
                padding_right=Decimal(8),
                padding_bottom=Decimal(8),
                padding_left=Decimal(8),
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        return self

    def add_h1(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 1 heading to this A4PortraitTemplate
        :param text:    the text of the (level 1) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H1_FONT_COLOR,
                font=A4PortraitTemplate.H1_FONT,
                font_size=A4PortraitTemplate.H1_FONT_SIZE,
                outline_level=0,
            )
        )
        return self

    def add_h2(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 2 heading to this A4PortraitTemplate
        :param text:    the text of the (level 2) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H2_FONT_COLOR,
                font=A4PortraitTemplate.H2_FONT,
                font_size=A4PortraitTemplate.H2_FONT_SIZE,
                outline_level=1,
            )
        )
        return self

    def add_h3(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 3 heading to this A4PortraitTemplate
        :param text:    the text of the (level 3) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H3_FONT_COLOR,
                font=A4PortraitTemplate.H3_FONT,
                font_size=A4PortraitTemplate.H3_FONT_SIZE,
                outline_level=2,
            )
        )
        return self

    def add_h4(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 4 heading to this A4PortraitTemplate
        :param text:    the text of the (level 4) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H4_FONT_COLOR,
                font=A4PortraitTemplate.H4_FONT,
                font_size=A4PortraitTemplate.H4_FONT_SIZE,
                outline_level=3,
            )
        )
        return self

    def add_h5(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 5 heading to this A4PortraitTemplate
        :param text:    the text of the (level 5) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H5_FONT_COLOR,
                font=A4PortraitTemplate.H5_FONT,
                font_size=A4PortraitTemplate.H5_FONT_SIZE,
                outline_level=4,
            )
        )
        return self

    def add_h6(self, text: str) -> "A4PortraitTemplate":
        """
        This function adds a level 6 heading to this A4PortraitTemplate
        :param text:    the text of the (level 6) heading
        :return:        self
        """
        self._layout.add(
            Heading(
                text=text,
                font_color=A4PortraitTemplate.H6_FONT_COLOR,
                font=A4PortraitTemplate.H6_FONT,
                font_size=A4PortraitTemplate.H6_FONT_SIZE,
                outline_level=5,
            )
        )
        return self

    def add_image(
        self,
        url_or_path: typing.Union[str, pathlib.Path],
    ) -> "A4PortraitTemplate":
        """
        This function adds an image to this A4PortraitTemplate
        :param url_or_path:     the url (str) or path (Path) of the Image
        :return:                self
        """
        assert isinstance(url_or_path, str) or isinstance(url_or_path, pathlib.Path)
        available_width: typing.Optional[Decimal] = None
        available_height: typing.Optional[Decimal] = None
        if isinstance(self._layout, TwoColumnLayout):
            available_width, available_height = Decimal(212), Decimal(673)
        if isinstance(self._layout, SingleColumnLayout):
            available_width, available_height = Decimal(465), Decimal(673)
        assert available_width is not None
        assert available_height is not None
        if isinstance(url_or_path, str):
            image_to_add: Image = Image(
                url_or_path,
                horizontal_alignment=Alignment.CENTERED,
                height=available_height,
                width=available_width,
            )
        if isinstance(url_or_path, pathlib.Path):
            assert url_or_path.exists()
            image_to_add = Image(
                url_or_path,
                horizontal_alignment=Alignment.CENTERED,
                height=available_height,
                width=available_width,
            )
        w: Decimal = Decimal(image_to_add.get_PIL_image().width)
        h: Decimal = Decimal(image_to_add.get_PIL_image().height)
        if w > available_width or h > available_height:
            scale: Decimal = max(w / available_width, h / available_height)
            image_to_add._width = Decimal(round(w / scale))
            image_to_add._height = Decimal(round(h / scale))
        self._layout.add(image_to_add)
        return self

    def add_linechart(
        self,
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        labels: typing.List[str],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "A4PortraitTemplate":
        """
        This function adds a linechart to this A4PortraitTemplate
        :param xs:          the xs-series
        :param ys:          the ys-series
        :param labels:      the labels
        :param x_label:     the label for the x-axis
        :param y_label:     the label for the y-axis
        :return:            self
        """

        available_width: typing.Optional[Decimal] = Decimal(200)
        available_height: typing.Optional[Decimal] = Decimal(200)

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add Chart
        self._layout.add(
            Chart(
                matplotlib.pyplot,
                width=available_width,
                height=available_height,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        return self

    def add_map_of_europe(
        self, marked_countries: typing.List[str] = []
    ) -> "A4PortraitTemplate":
        """
        This function adds a map of Europe to this A4PortraitTemplate
        :param marked_countries:    the countries that ought to be marked
        :return:                    self
        """
        available_width: Decimal = Decimal(200)
        available_height: Decimal = Decimal(200)
        m: MapOfEurope = MapOfEurope(
            horizontal_alignment=Alignment.CENTERED,
            fill_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        for c in marked_countries:
            m.set_fill_color(A4PortraitTemplate.ACCENT_COLOR, key=c)
        m.scale_up(max_width=available_width, max_height=available_height)
        m.scale_down(max_width=available_width, max_height=available_height)
        self._layout.add(m)
        return self

    def add_map_of_the_contiguous_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "A4PortraitTemplate":
        """
        This function adds a map of the (contiguous) United States to this A4PortraitTemplate
        :param marked_countries:    the states that ought to be marked
        :return:                    self
        """
        available_width: Decimal = Decimal(200)
        available_height: Decimal = Decimal(200)
        m: MapOfTheUnitedStates = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            fill_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
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
        for c in marked_states:
            m.set_fill_color(A4PortraitTemplate.ACCENT_COLOR, key=c)
        m.scale_up(max_width=available_width, max_height=available_height)
        m.scale_down(max_width=available_width, max_height=available_height)
        self._layout.add(m)
        return self

    def add_map_of_the_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "A4PortraitTemplate":
        """
        This function adds a map of the United States to this A4PortraitTemplate
        :param marked_countries:    the states that ought to be marked
        :return:                    self
        """
        available_width: Decimal = Decimal(200)
        available_height: Decimal = Decimal(200)
        m: MapOfTheUnitedStates = MapOfTheUnitedStates(
            horizontal_alignment=Alignment.CENTERED,
            fill_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        for c in marked_states:
            m.set_fill_color(A4PortraitTemplate.ACCENT_COLOR, key=c)
        m.scale_up(max_width=available_width, max_height=available_height)
        m.scale_down(max_width=available_width, max_height=available_height)
        self._layout.add(m)
        return self

    def add_map_of_the_world(
        self, marked_countries: typing.List[str] = []
    ) -> "A4PortraitTemplate":
        """
        This function adds a map of the world to this A4PortraitTemplate
        :param marked_countries:    the countries that ought to be marked
        :return:                    self
        """
        available_width: Decimal = Decimal(200)
        available_height: Decimal = Decimal(200)
        m: MapOfTheWorld = MapOfTheWorld(
            horizontal_alignment=Alignment.CENTERED,
            fill_color=A4PortraitTemplate.LIGHT_GRAY_COLOR,
            stroke_color=HexColor("#ffffff"),
            line_width=Decimal(0.1),
        )
        for c in marked_countries:
            m.set_fill_color(A4PortraitTemplate.ACCENT_COLOR, key=c)
        m.scale_up(max_width=available_width, max_height=available_height)
        m.scale_down(max_width=available_width, max_height=available_height)
        self._layout.add(m)
        return self

    def add_ordered_list(
        self,
        text: typing.List[str],
    ) -> "A4PortraitTemplate":
        """
        This function adds an ordered list to this A4PortraitTemplate
        :param text:                    the text (typing.List[str]) to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, typing.List),           "text must be typing.List[str]"
        assert len(text) > 0,                           "text must have 1 or more element(s)"
        assert all([isinstance(x, str) for x in text]), "text must be typing.List[str]"

        # fmt: on
        l: OrderedList = OrderedList()
        for x in text:
            l.add(
                Paragraph(
                    x,
                    font=A4PortraitTemplate.BODY_FONT,
                    font_size=A4PortraitTemplate.BODY_FONT_SIZE,
                    font_color=A4PortraitTemplate.BODY_FONT_COLOR,
                )
            )
        self._layout.add(l)
        return self

    def add_page(self) -> "A4PortraitTemplate":
        """
        This function switches to a new Page
        :return:    self
        """
        self._layout.switch_to_next_page()
        return self

    def add_piechart(
        self,
        xs: typing.List[float],
        labels: typing.List[str],
    ) -> "A4PortraitTemplate":
        """
        This function adds a piechart to this A4PortraitTemplate
        :param xs:      the xs-series
        :param labels:  the labels
        :return:        self
        """
        available_width: typing.Optional[Decimal] = Decimal(200)
        available_height: typing.Optional[Decimal] = Decimal(200)

        # create matplotlib plot
        import matplotlib.pyplot

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        should_explode = tuple(
            [1 if xs[i] == max(xs) else 0 for i in range(0, len(xs))]
        )
        ax.pie(xs, labels=labels, explode=should_explode)
        fig.legend(loc="outside lower center")

        # add Chart
        self._layout.add(
            Chart(
                matplotlib.pyplot,
                width=available_width,
                height=available_height,
                horizontal_alignment=Alignment.CENTERED,
            )
        )
        return self

    def add_qr_code(
        self,
        data: str,
    ) -> "A4PortraitTemplate":
        """
        This function adds a QR code to this A4PortraitTemplate
        :param data:                    the data to be encoded in the QR code (e.g. a URL)
        :return:                        self
        """
        available_width: typing.Optional[Decimal] = Decimal(200)
        available_height: typing.Optional[Decimal] = Decimal(200)
        self._layout.add(
            Barcode(
                data=data,
                stroke_color=A4PortraitTemplate.BODY_FONT_COLOR,
                horizontal_alignment=Alignment.CENTERED,
                fill_color=HexColor("#ffffff"),
                width=available_width,
                height=available_height,
                type=BarcodeType.QR,
            )
        )
        return self

    def add_quote(self, quote_author: str, quote_text: str) -> "A4PortraitTemplate":
        """
        This function adds a quote and its author to this A4PortraitTemplate
        :param quote_author:    the author of the quote
        :param quote_text:      the text of the quote
        :return:                self
        """
        self._layout.add(
            FlexibleColumnWidthTable(
                number_of_columns=1,
                number_of_rows=2,
                border_left=True,
                border_width=Decimal(3),
                border_color=A4PortraitTemplate.ACCENT_COLOR,
            )
            .add(
                Paragraph(
                    quote_text,
                    text_alignment=(
                        Alignment.JUSTIFIED
                        if isinstance(self._layout, TwoColumnLayout)
                        else Alignment.LEFT
                    ),
                    font=A4PortraitTemplate.QUOTE_TEXT_FONT,
                    font_color=A4PortraitTemplate.QUOTE_TEXT_FONT_COLOR,
                    font_size=A4PortraitTemplate.QUOTE_TEXT_FONT_SIZE,
                )
            )
            .add(
                Paragraph(
                    quote_author,
                    font=A4PortraitTemplate.QUOTE_AUTHOR_FONT,
                    font_color=A4PortraitTemplate.QUOTE_AUTHOR_FONT_COLOR,
                    font_size=A4PortraitTemplate.QUOTE_AUTHOR_FONT_SIZE,
                )
            )
            .set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            .no_borders()
        )
        return self

    def add_table(
        self,
        tabular_data: typing.List[typing.List[str]],
        use_header_row: bool = True,
        use_header_column: bool = False,
    ) -> "A4PortraitTemplate":
        """
        This function adds a Table to this A4PortraitTemplate
        :param tabular_data:        the text (typing.List[typing.List[str]]) in the Table
        :param use_header_row:      whether to use a header row or not (default True)
        :param use_header_column:   whether to use a header column or not (default False)
        :return:                    self
        """
        # fmt: off

        assert isinstance(tabular_data, typing.List), "text must be typing.List[typing.List[str]]"
        assert len(tabular_data) > 0, "text must have 1 or more element(s)"
        assert all([isinstance(x, typing.List) for x in tabular_data]), "text must be typing.List[typing.List[str]]"
        # fmt: on

        t: Table = TableUtil.from_2d_array(
            tabular_data,
            font_color=A4PortraitTemplate.BODY_FONT_COLOR,
            font_size=A4PortraitTemplate.BODY_FONT_SIZE,
            header_row=use_header_row,
            header_col=use_header_column,
            round_to_n_digits=2,
            flexible_column_width=False,
        )

        # add Table to SingleColumnLayout
        self._layout.add(t)

        # return
        return self

    def add_text(
        self,
        text: str,
    ) -> "A4PortraitTemplate":
        """
        This function adds a Paragraph of text to this A4PortraitTemplate
        :param text:                    the text (str) to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, str),               "text must be str"

        # fmt: on
        self._layout.add(
            Paragraph(
                text,
                font=A4PortraitTemplate.BODY_FONT,
                font_size=A4PortraitTemplate.BODY_FONT_SIZE,
                font_color=A4PortraitTemplate.BODY_FONT_COLOR,
            )
        )
        return self

    def add_unordered_list(
        self,
        text: typing.List[str],
    ) -> "A4PortraitTemplate":
        """
        This function adds an unordered list to this A4PortraitTemplate
        :param text:                    the text (typing.List[str]) to be added
        :return:                        self
        """
        # fmt: off

        assert isinstance(text, typing.List),           "text must be typing.List[str]"
        assert len(text) > 0,                           "text must have 1 or more element(s)"
        assert all([isinstance(x, str) for x in text]), "text must be typing.List[str]"

        # fmt: on
        l: UnorderedList = UnorderedList()
        for x in text:
            l.add(
                Paragraph(
                    x,
                    font=A4PortraitTemplate.BODY_FONT,
                    font_size=A4PortraitTemplate.BODY_FONT_SIZE,
                    font_color=A4PortraitTemplate.BODY_FONT_COLOR,
                )
            )
        self._layout.add(l)
        return self

    def bytes(self) -> bytes:
        """
        This function returns the bytes representing this A4PortraitTemplate.
        It does so by saving this A4PortraitTemplate to an io.BytesIO buffer,
        and returning its bytes.
        :return:    the bytes representing this A4PortraitTemplate
        """
        self._add_page_numbers()
        buffer = io.BytesIO()
        PDF.dumps(buffer, self._document)
        buffer.seek(0)
        return buffer.getvalue()

    def save(
        self, path_or_str: typing.Union[str, pathlib.Path]
    ) -> "A4PortraitTemplate":
        """
        This function stores this A4PortraitTemplate at the given path
        :param path_or_str:     the path or str representing the location at which to store this A4PortraitTemplate
        :return:                self
        """
        self._add_page_numbers()
        with open(path_or_str, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self._document)
        return self
