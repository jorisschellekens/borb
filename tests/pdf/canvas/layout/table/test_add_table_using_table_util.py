from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import TableUtil
from tests.test_case import TestCase


class TestAddTableUsingTableUtil(TestCase):
    def test_add_fixed_column_width_table_using_table_util_2_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                header_row=False,
                flexible_column_width=False,
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_fixed_column_width_table_using_table_util_3_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Lorem", "Ipsum", "Dolor"],
                    ["Sit", "Amet", "Consectetur"],
                    ["Adipiscing", "Sed", "Do"],
                ],
                flexible_column_width=False,
                header_row=False,
            )
        )
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_fixed_column_width_table_using_table_util_3_by_4(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Lorem", "Ipsum", "Dolor", "Sit"],
                    ["Amet", "Consectetur", "Adipiscing", "Sed"],
                    ["Do", "Eiusmod", "Tempor", "Incididunt"],
                ],
                flexible_column_width=False,
                header_row=False,
            )
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_fixed_column_width_table_using_table_util_with_header_row(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                flexible_column_width=False,
                header_row=True,
            )
        )
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_fixed_column_width_table_using_table_util_with_header_column(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                flexible_column_width=False,
                header_row=False,
                header_col=True,
            )
        )
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_fixed_column_width_table_using_table_util_with_rounding_to_2_digits(
        self,
    ):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], [0.999, 3.1415, 2.7182]],
                flexible_column_width=False,
                header_row=False,
                round_to_n_digits=2,
            )
        )
        with open(self.get_sixth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_fixed_column_width_table_using_table_util_with_rounding_to_3_digits(
        self,
    ):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FixedColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], [0.999, 3.1415, 2.7182]],
                flexible_column_width=False,
                header_row=False,
                round_to_n_digits=3,
            )
        )
        with open(self.get_seventh_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    #
    #
    #

    def test_add_flexible_column_width_table_using_table_util_2_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                header_row=False,
            )
        )
        with open(self.get_eight_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_add_flexible_column_width_table_using_table_util_3_by_3(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Lorem", "Ipsum", "Dolor"],
                    ["Sit", "Amet", "Consectetur"],
                    ["Adipiscing", "Sed", "Do"],
                ],
                header_row=False,
            )
        )
        with open(self.get_nineth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())

    def test_add_flexible_column_width_table_using_table_util_3_by_4(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [
                    ["Lorem", "Ipsum", "Dolor", "Sit"],
                    ["Amet", "Consectetur", "Adipiscing", "Sed"],
                    ["Do", "Eiusmod", "Tempor", "Incididunt"],
                ],
                header_row=False,
            )
        )
        with open(self.get_tenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_tenth_output_file())
        self.check_pdf_using_validator(self.get_tenth_output_file())

    def test_add_flexible_column_width_table_using_table_util_with_header_row(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                header_row=True,
            )
        )
        with open(self.get_eleventh_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_eleventh_output_file())
        self.check_pdf_using_validator(self.get_eleventh_output_file())

    def test_add_flexible_column_width_table_using_table_util_with_header_column(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
                header_row=False,
                header_col=True,
            )
        )
        with open(self.get_twelfth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_twelfth_output_file())
        self.check_pdf_using_validator(self.get_twelfth_output_file())

    def test_add_flexible_column_width_table_using_table_util_with_rounding_to_2_digits(
        self,
    ):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], [0.999, 3.1415, 2.7182]],
                header_row=False,
                round_to_n_digits=2,
            )
        )
        with open(self.get_thirteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_thirteenth_output_file())
        self.check_pdf_using_validator(self.get_thirteenth_output_file())

    def test_add_flexible_column_width_table_using_table_util_with_rounding_to_3_digits(
        self,
    ):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(
            TableUtil.from_2d_array(
                [["Lorem", "Ipsum", "Dolor"], [0.999, 3.1415, 2.7182]],
                header_row=False,
                round_to_n_digits=3,
            )
        )
        with open(self.get_fourteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourteenth_output_file())
        self.check_pdf_using_validator(self.get_fourteenth_output_file())

    def test_add_table_from_pandas_dataframe_using_table_util(self):

        # Import pandas package
        import pandas as pd

        data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")
        data = data[0:10]

        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(
                test_description="This test adds a FlexibleColumnWidthTable to a PDF using the TableUtil."
            )
        )
        layout.add(TableUtil.from_pandas_dataframe(data))
        with open(self.get_fifteenth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifteenth_output_file())
        self.check_pdf_using_validator(self.get_fifteenth_output_file())
