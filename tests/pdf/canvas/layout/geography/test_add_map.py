from decimal import Decimal

from borb.pdf import Alignment
from borb.pdf import Document
from borb.pdf import FixedColumnWidthTable
from borb.pdf import HexColor
from borb.pdf import MapOfTheWorld
from borb.pdf import OrderedList
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import UnorderedList
from tests.test_case import TestCase


class TestAddMap(TestCase):
    def test_add_map(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(MapOfTheWorld())

        # write
        with open(self.get_first_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_ordered_list_of_maps(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header(
                "This tests creates a PDF with an OrderedList of MapOfTheWorld objects in it."
            )
        )
        layout.add(
            OrderedList()
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="United States of America")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="France")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="Germany")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
        )

        # write
        with open(self.get_second_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_unordered_list_of_maps(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header(
                "This tests creates a PDF with am UnorderedList of MapOfTheWorld objects in it."
            )
        )
        layout.add(
            UnorderedList()
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="United States of America")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="France")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="Germany")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
        )

        # write
        with open(self.get_third_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_table_of_maps(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header(
                "This tests creates a PDF with a Table of MapOfTheWorld objects in it."
            )
        )
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="United States of America")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="France")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="Germany")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
            .add(
                MapOfTheWorld()
                .set_stroke_color(HexColor("#ffffff"))
                .set_fill_color(HexColor("#f0f0f0"))
                .set_fill_color(HexColor("#f1cd2e"), key="Spain")
                .scale_down(max_width=Decimal(200), max_height=Decimal(200))
            )
        )

        # write
        with open(self.get_fourth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_map_using_border(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(
            MapOfTheWorld(
                border_top=True,
                border_right=True,
                border_bottom=True,
                border_left=True,
                border_color=HexColor("#0b3954"),
            )
            .set_stroke_color(HexColor("#ffffff"))
            .set_fill_color(HexColor("#f0f0f0"))
            .set_fill_color(HexColor("#f1cd2e"), key="Spain")
            .scale_down(max_width=Decimal(200), max_height=Decimal(200))
        )

        # write
        with open(self.get_fifth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_image_using_horizontal_alignment_left(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(
            MapOfTheWorld(horizontal_alignment=Alignment.LEFT)
            .set_stroke_color(HexColor("#ffffff"))
            .set_fill_color(HexColor("#f0f0f0"))
            .set_fill_color(HexColor("#f1cd2e"), key="Spain")
            .scale_down(max_width=Decimal(200), max_height=Decimal(200))
        )

        # write
        with open(self.get_sixth_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_image_using_horizontal_alignment_centered(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(
            MapOfTheWorld(horizontal_alignment=Alignment.CENTERED)
            .set_stroke_color(HexColor("#ffffff"))
            .set_fill_color(HexColor("#f0f0f0"))
            .set_fill_color(HexColor("#f1cd2e"), key="Spain")
            .scale_down(max_width=Decimal(200), max_height=Decimal(200))
        )

        # write
        with open(self.get_seventh_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_image_using_horizontal_alignment_right(self):
        pdf: Document = Document()
        page: Page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # add content
        layout.add(
            self.get_test_header("This tests creates a PDF with a MapOfTheWorld in it.")
        )
        layout.add(
            MapOfTheWorld(horizontal_alignment=Alignment.RIGHT)
            .set_stroke_color(HexColor("#ffffff"))
            .set_fill_color(HexColor("#f0f0f0"))
            .set_fill_color(HexColor("#f1cd2e"), key="Spain")
            .scale_down(max_width=Decimal(200), max_height=Decimal(200))
        )

        # write
        with open(self.get_eight_output_file(), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())
