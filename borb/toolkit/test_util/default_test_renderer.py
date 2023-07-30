#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class represents the default implementation of TestRenderer
"""

import datetime
import math
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.pantone import Pantone
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.link_annotation import DestinationType
from borb.pdf.canvas.layout.annotation.link_annotation import LinkAnnotation
from borb.pdf.canvas.layout.annotation.text_annotation import TextAnnotation
from borb.pdf.canvas.layout.annotation.text_annotation import TextAnnotationIconType
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import (
    FlexibleColumnWidthTable,
)
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.toolkit.test_util.test_info import TestResult
from borb.toolkit.test_util.test_renderer import TestRenderer
from borb.toolkit.test_util.test_status import TestStatus


class DefaultTestRenderer(TestRenderer):
    """
    This class represents the default implementation of TestRenderer
    """

    #
    # BACK COVER PAGE
    #

    BACK_COVER_PAGE_FONT_COLOR_1: Color = HexColor("FFFFFF")
    BACK_COVER_PAGE_FONT_NAME_1: str = "Helvetica"
    BACK_COVER_PAGE_FONT_SIZE_1: Decimal = Decimal(12)

    #
    # FRONT COVER PAGE
    #

    COVER_PAGE_ACCENT_COLOR_1: Color = HexColor("#114B5F")
    COVER_PAGE_ACCENT_COLOR_2: Color = HexColor("#1A936F")
    COVER_PAGE_ACCENT_COLOR_3: Color = HexColor("#88D498")
    COVER_PAGE_ACCENT_COLOR_4: Color = HexColor("#FF9B42")
    COVER_PAGE_FONT_COLOR_1: Color = HexColor("FFFFFF")
    COVER_PAGE_FONT_COLOR_2: Color = HexColor("FFFFFF")
    COVER_PAGE_FONT_COLOR_3: Color = HexColor("FFFFFF")
    COVER_PAGE_FONT_NAME_1: str = "Helvetica"
    COVER_PAGE_FONT_NAME_2: str = "Helvetica-Bold"
    COVER_PAGE_FONT_NAME_3: str = "Helvetica"
    COVER_PAGE_FONT_SIZE_1: Decimal = Decimal(20)
    COVER_PAGE_FONT_SIZE_2: Decimal = Decimal(30)
    COVER_PAGE_FONT_SIZE_3: Decimal = Decimal(12)

    #
    # SUMMARY PAGE
    #

    SUMMARY_PAGE_FONT_COLOR_1: Color = HexColor("114B5F")
    SUMMARY_PAGE_FONT_NAME_1: str = "Helvetica-Bold"
    SUMMARY_PAGE_FONT_SIZE_1: Decimal = Decimal(20)
    SUMMARY_PAGE_TEST_STATUS_TO_COLOR_DICT: typing.Dict[TestStatus, Color] = {
        TestStatus.SKIP: HexColor("A8D5E2"),
        TestStatus.ERROR: HexColor("#FF9B42"),
        TestStatus.FAILURE: HexColor("#FF9B42"),
        TestStatus.SUCCESS: HexColor("#1A936F"),
        TestStatus.EXPECTED_FAILURE: HexColor("#FF9B42"),
        TestStatus.UNEXPECTED_SUCCESS: HexColor("#88D498"),
    }

    #
    # CLASS LEVEL PAGE
    #

    CLASS_LEVEL_PAGE_FONT_COLOR_1: Color = HexColor("114B5F")
    CLASS_LEVEL_PAGE_FONT_COLOR_2: Color = HexColor("114B5F")
    CLASS_LEVEL_PAGE_FONT_COLOR_3: Color = HexColor("000000")
    CLASS_LEVEL_PAGE_FONT_NAME_1: str = "Helvetica-Bold"
    CLASS_LEVEL_PAGE_FONT_NAME_2: str = "Helvetica-Bold"
    CLASS_LEVEL_PAGE_FONT_NAME_3: str = "Helvetica"
    CLASS_LEVEL_PAGE_FONT_SIZE_1: Decimal = Decimal(20)
    CLASS_LEVEL_PAGE_FONT_SIZE_2: Decimal = Decimal(12)
    CLASS_LEVEL_PAGE_FONT_SIZE_3: Decimal = Decimal(8)
    CLASS_LEVEL_TRUNCATION_LIMIT: int = 40

    #
    # DOCUMENT WIDE PROPERTIES
    #

    HORIZONTAL_MARGIN: Decimal = Decimal(0.06)
    TIME_FORMAT: str = "%H:%M:%S"
    VERTICAL_MARGIN: Decimal = Decimal(0.06)

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._current_page: typing.Optional[Page] = None
        self._current_page_layout: typing.Optional[PageLayout] = None
        self._test_results_to_summary_layout_element: typing.Dict[
            TestResult, LayoutElement
        ] = {}

    #
    # PRIVATE
    #

    @staticmethod
    def _duration_to_str(duration: float) -> str:
        # <milliseconds>
        duration_in_ms: int = int(duration * 1000)
        if duration_in_ms < 1000:
            return "%dms" % duration
        # <seconds> <milliseconds>
        if duration_in_ms < 1000 * 60:
            a: int = duration_in_ms // 1000
            b: int = duration_in_ms % 1000
            return "%ds %dms" % (a, b)
        # <minutes> <seconds> <milliseconds>
        a: int = duration_in_ms // (1000 * 60)
        b: int = (duration_in_ms - a * 1000 * 60) // 1000
        c: int = duration_in_ms % 1000
        return "%dm %ds %dms" % (a, b, c)

    @staticmethod
    def _truncate_str(s: str, n: int = 10) -> str:
        if len(s) <= n:
            return s
        return "..." + s[(-n + 3) :]

    #
    # PUBLIC
    #

    def build_pdf_back_cover_page(self, d: Document) -> None:
        """
        This function is called to build the (back) cover Page of the PDF
        :param d:   the PDF to which the cover page can be added
        :return:    None
        """

        page: Page = Page()
        d.add_page(page)

        # draw shape 1
        ZERO: Decimal = Decimal(0)
        W: Decimal = page.get_page_info().get_width()  # width of paper
        H: Decimal = page.get_page_info().get_height()  # height of paper
        W70: Decimal = Decimal(0.70) * W  # width of our large triangle
        H87: Decimal = Decimal(0.87) * H  # height of our large triangle
        ConnectedShape(
            points=[
                (ZERO, H - H87),
                (W70, H),
                (W, H),
                (W, ZERO),
                (ZERO, ZERO),
            ],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_1,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_1,
        ).paint(page, Rectangle(ZERO, ZERO, W, H))

        # first paragraph
        VERTICAL_MARGIN: Decimal = DefaultTestRenderer.VERTICAL_MARGIN * W
        HORIZONTAL_MARGIN: Decimal = DefaultTestRenderer.HORIZONTAL_MARGIN * H
        p0: Paragraph = Paragraph(
            "Test Report built by borb",
            font=DefaultTestRenderer.BACK_COVER_PAGE_FONT_NAME_1,
            font_size=DefaultTestRenderer.BACK_COVER_PAGE_FONT_SIZE_1,
            font_color=DefaultTestRenderer.BACK_COVER_PAGE_FONT_COLOR_1,
            vertical_alignment=Alignment.BOTTOM,
            horizontal_alignment=Alignment.RIGHT,
        )
        p0.paint(
            page,
            Rectangle(
                HORIZONTAL_MARGIN,
                VERTICAL_MARGIN,
                W - HORIZONTAL_MARGIN * Decimal(2),
                H - VERTICAL_MARGIN * Decimal(2),
            ),
        )

    def build_pdf_front_cover_page(self, d: Document) -> None:
        """
        This function is called to build the cover Page of the PDF
        :param d:   the PDF to which the cover page can be added
        :return:    None
        """

        page: Page = Page()
        d.add_page(page)

        # draw shape 1
        ZERO: Decimal = Decimal(0)
        W: Decimal = page.get_page_info().get_width()  # width of paper
        H: Decimal = page.get_page_info().get_height()  # height of paper
        W70: Decimal = Decimal(0.70) * W  # width of our large triangle
        H87: Decimal = Decimal(0.87) * H  # height of our large triangle
        ConnectedShape(
            points=[(ZERO, H - H87), (ZERO, H), (W70, H)],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_1,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_1,
        ).paint(page, Rectangle(ZERO, ZERO, W, H))

        # define a helper function
        # this function returns the y-coordinate for every x-coordinate on the longest side of the triangle
        # this is useful because all our other shapes will have a few coordinates in common with this side
        # being able to easily calculate a point on this side of the triangle is really going to help us out
        y_coordinate: typing.Callable[[Decimal], Decimal] = (
            lambda x: Decimal(109.46) + Decimal(1.7588) * x
        )

        # shape 2
        W20: Decimal = Decimal(0.20) * W70
        W40: Decimal = Decimal(0.40) * W70
        W60: Decimal = Decimal(0.60) * W70
        ConnectedShape(
            points=[
                (W20, y_coordinate(W20)),
                (W40, y_coordinate(W40)),
                (W20, y_coordinate(W60)),
                (ZERO, y_coordinate(W40)),
            ],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_2,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_2,
            vertical_alignment=Alignment.BOTTOM,
        ).paint(page, Rectangle(ZERO, y_coordinate(W20), W, H))

        # shape 3
        ConnectedShape(
            points=[
                (W40, y_coordinate(W40)),
                (W60, y_coordinate(W60)),
                (W20, y_coordinate(W60)),
            ],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_3,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_3,
            vertical_alignment=Alignment.BOTTOM,
        ).paint(page, Rectangle(W20, y_coordinate(W40), W, H))

        # shape 4
        W80: Decimal = Decimal(0.8) * W70
        ConnectedShape(
            points=[
                (W60, y_coordinate(W60)),
                (W60 + W20 * 2, y_coordinate(W60)),
                (W80 + W20 * 2, y_coordinate(W80)),
                (W80, y_coordinate(W80)),
            ],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_2,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_2,
            vertical_alignment=Alignment.BOTTOM,
        ).paint(page, Rectangle(W60, y_coordinate(W60), W, H))

        # shape 5
        ConnectedShape(
            points=[
                (W80, y_coordinate(W80)),
                (W80 + W20 * 2, y_coordinate(W80)),
                (W + W20 * 2, y_coordinate(W)),
                (W, y_coordinate(W)),
            ],
            fill_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_4,
            stroke_color=DefaultTestRenderer.COVER_PAGE_ACCENT_COLOR_4,
            vertical_alignment=Alignment.BOTTOM,
        ).paint(page, Rectangle(W80, y_coordinate(W80), W, H))

        # first paragraph
        p0: Paragraph = Paragraph(
            "Test Report",
            font=DefaultTestRenderer.COVER_PAGE_FONT_NAME_1,
            font_size=DefaultTestRenderer.COVER_PAGE_FONT_SIZE_1,
            font_color=DefaultTestRenderer.COVER_PAGE_FONT_COLOR_1,
        )

        # second paragraph
        p1: Paragraph = Paragraph(
            datetime.datetime.now().strftime(DefaultTestRenderer.TIME_FORMAT),
            font=DefaultTestRenderer.COVER_PAGE_FONT_NAME_2,
            font_size=DefaultTestRenderer.COVER_PAGE_FONT_SIZE_2,
            font_color=DefaultTestRenderer.COVER_PAGE_FONT_COLOR_2,
        )

        # third paragraph
        p2: Paragraph = Paragraph(
            "A test report summary contains all the details of the testing process, what was tested, "
            "when was it tested, how it was tested, and the environments where it was tested.",
            font=DefaultTestRenderer.COVER_PAGE_FONT_NAME_3,
            font_size=DefaultTestRenderer.COVER_PAGE_FONT_SIZE_3,
            font_color=DefaultTestRenderer.COVER_PAGE_FONT_COLOR_3,
        )

        table: Table = (
            FixedColumnWidthTable(number_of_columns=1, number_of_rows=3)
            .add(p0)
            .add(p1)
            .add(p2)
            .no_borders()
        )

        # paint
        HORIZONTAL_MARGIN: Decimal = DefaultTestRenderer.HORIZONTAL_MARGIN * W
        VERTICAL_MARGIN: Decimal = DefaultTestRenderer.VERTICAL_MARGIN * H
        table.paint(
            page,
            Rectangle(
                HORIZONTAL_MARGIN,
                VERTICAL_MARGIN,
                W * Decimal(0.4) - HORIZONTAL_MARGIN * Decimal(2),
                H - VERTICAL_MARGIN * Decimal(2),
            ),
        )

    def build_pdf_module_page(self, d: Document, t: typing.List[TestResult]) -> None:
        """
        This function is called to build content for each typing.List[TestResult] representing a module that was tested
        :param d:   the PDF to which the cover page can be added
        :param t:   the typing.List[TestResult]  representing the module that was tested
        :return:    None
        """

        # add new Page
        if self._current_page is None:
            self._current_page = Page()
            d.add_page(self._current_page)
            self._current_page_layout = SingleColumnLayout(self._current_page)
            self._current_page_layout._margin_top = (
                PageSize.A4_PORTRAIT.value[1] * DefaultTestRenderer.VERTICAL_MARGIN
            )
            self._current_page_layout._margin_right = (
                PageSize.A4_PORTRAIT.value[0] * DefaultTestRenderer.HORIZONTAL_MARGIN
            )
            self._current_page_layout._margin_bottom = (
                PageSize.A4_PORTRAIT.value[1] * DefaultTestRenderer.VERTICAL_MARGIN
            )
            self._current_page_layout._margin_left = (
                PageSize.A4_PORTRAIT.value[0] * DefaultTestRenderer.HORIZONTAL_MARGIN
            )
            self._current_page_layout._column_widths = [
                PageSize.A4_PORTRAIT.value[0]
                * (1 - 2 * DefaultTestRenderer.HORIZONTAL_MARGIN)
            ]

        # shorthand for truncation function
        truncate = lambda x: DefaultTestRenderer._truncate_str(x)

        # check whether we need to include a backlink to this
        for failed_test in [x for x in t if x.get_status() != TestStatus.SUCCESS]:
            doc: Document = self._current_page.get_document()
            summary_page: Page = doc.get_page(1)
            summary_page.add_annotation(
                LinkAnnotation(
                    bounding_box=self._test_results_to_summary_layout_element[
                        failed_test
                    ].get_previous_layout_box(),
                    page=doc.get_document_info().get_number_of_pages() - 1,
                    destination_type=DestinationType.FIT,
                )
            )

        # add Paragraph
        self._current_page_layout.add(
            Paragraph(
                "Class: %s"
                % DefaultTestRenderer._truncate_str(
                    t[0].get_class_name(),
                    DefaultTestRenderer.CLASS_LEVEL_TRUNCATION_LIMIT,
                ),
                font_size=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_SIZE_1,
                font=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_NAME_1,
                font_color=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_COLOR_1,
            )
        )

        # add Table
        for i in range(0, len(t), 20):
            test_result_slice: typing.List[TestResult] = t[i : (i + 20)]

            # add heading
            table: Table = FixedColumnWidthTable(
                number_of_columns=7, number_of_rows=len(test_result_slice) + 1
            )
            for h in ["Class", "File", "Method", "Start", "End", "Duration", "Status"]:
                table.add(
                    Paragraph(
                        h,
                        font_size=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_SIZE_2,
                        font=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_NAME_2,
                        font_color=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_COLOR_2,
                    )
                )

            # add rows
            for tr in test_result_slice:
                for h in [
                    tr.get_class_name(),
                    tr.get_file(),
                    tr.get_method(),
                    datetime.datetime.fromtimestamp(tr.get_started_at()).strftime(
                        DefaultTestRenderer.TIME_FORMAT
                    ),
                    datetime.datetime.fromtimestamp(tr.get_started_at()).strftime(
                        DefaultTestRenderer.TIME_FORMAT
                    ),
                    DefaultTestRenderer._duration_to_str(tr.get_duration()),
                    tr.get_status().name,
                ]:
                    table.add(
                        Paragraph(
                            truncate(h),
                            font_size=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_SIZE_3,
                            font=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_NAME_3,
                            font_color=DefaultTestRenderer.CLASS_LEVEL_PAGE_FONT_COLOR_3,
                        )
                    )

            # zebra striping
            table.no_borders()
            for tc in table.get_cells_at_row(0):
                tc._border_bottom = True
                tc._border_width = Decimal(3)
            table.even_odd_row_colors(
                even_row_color=HexColor("ffffff"), odd_row_color=HexColor("f0f0f0")
            )
            table.set_padding_on_all_cells(
                Decimal(2), Decimal(2), Decimal(2), Decimal(2)
            )

            # add table
            self._current_page_layout.add(table)

    def build_pdf_summary_page(self, d: Document, t: typing.List[TestResult]) -> None:
        """
        This function is called to build content representing a summary of all tests that were run
        :param d:   the PDF to which the cover page can be added
        :param t:   the typing.List[TestResult]  representing all tests that were run
        :return:    None
        """

        # add empty Page
        page: Page = Page()
        d.add_page(page)

        # set PageLayout
        # fmt: off
        layout: PageLayout = SingleColumnLayout(page)
        layout._margin_top = (PageSize.A4_PORTRAIT.value[1] * DefaultTestRenderer.HORIZONTAL_MARGIN)
        layout._margin_right = (PageSize.A4_PORTRAIT.value[0] * DefaultTestRenderer.VERTICAL_MARGIN)
        layout._margin_bottom = (PageSize.A4_PORTRAIT.value[1] * DefaultTestRenderer.HORIZONTAL_MARGIN)
        layout._margin_left = (PageSize.A4_PORTRAIT.value[0] * DefaultTestRenderer.VERTICAL_MARGIN)
        # fmt: on

        # add Paragraph
        layout.add(
            Paragraph(
                "Summary",
                font_size=DefaultTestRenderer.SUMMARY_PAGE_FONT_SIZE_1,
                font=DefaultTestRenderer.SUMMARY_PAGE_FONT_NAME_1,
                font_color=DefaultTestRenderer.SUMMARY_PAGE_FONT_COLOR_1,
            )
        )

        # determine number of rows/cols
        n: int = len(t)
        number_of_rows: int = int(math.sqrt(n))
        number_of_cols: int = n // number_of_rows
        while number_of_cols * number_of_rows < n:
            number_of_cols += 1

        # add Table
        overview_table: Table = FlexibleColumnWidthTable(
            number_of_rows=number_of_rows,
            number_of_columns=number_of_cols,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.MIDDLE,
        )

        ZERO: Decimal = Decimal(0)
        ICON_SIZE: Decimal = Decimal(12)
        for i in range(0, number_of_rows * number_of_cols):
            e: LayoutElement = Paragraph("")
            if i < n:
                e = ConnectedShape(
                    LineArtFactory.droplet(
                        bounding_box=Rectangle(ZERO, ZERO, ICON_SIZE, ICON_SIZE)
                    ),
                    fill_color=DefaultTestRenderer.SUMMARY_PAGE_TEST_STATUS_TO_COLOR_DICT[
                        t[i].get_status()
                    ],
                    stroke_color=DefaultTestRenderer.SUMMARY_PAGE_TEST_STATUS_TO_COLOR_DICT[
                        t[i].get_status()
                    ],
                )
                self._test_results_to_summary_layout_element[t[i]] = e
            overview_table.add(e)
        overview_table.no_borders()
        overview_table.set_padding_on_all_cells(
            Decimal(2), Decimal(2), Decimal(2), Decimal(2)
        )
        layout.add(overview_table)

        # add legend
        page.add_annotation(
            TextAnnotation(
                Rectangle(
                    DefaultTestRenderer.HORIZONTAL_MARGIN
                    * page.get_page_info().get_width(),
                    DefaultTestRenderer.VERTICAL_MARGIN
                    * page.get_page_info().get_height(),
                    ICON_SIZE,
                    ICON_SIZE,
                ),
                contents="Legend:\n"
                + "".join(
                    [
                        "    - %s is represented by %s (%s).\n"
                        % (
                            k.name,
                            v.to_rgb().to_hex_string(),
                            Pantone.find_nearest_pantone_color(v).get_name(),
                        )
                        for k, v in DefaultTestRenderer.SUMMARY_PAGE_TEST_STATUS_TO_COLOR_DICT.items()
                    ]
                ),
                text_annotation_icon=TextAnnotationIconType.HELP,
                color=DefaultTestRenderer.SUMMARY_PAGE_TEST_STATUS_TO_COLOR_DICT[
                    TestStatus.SUCCESS
                ],
            )
        )
