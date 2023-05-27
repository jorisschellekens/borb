from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import SmartArt
from tests.test_case import TestCase


class TestAddSmartArtBasicBendingProcess(TestCase):
    def test_add_smartart_basic_bending_process_001(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(SmartArt.basic_bending_process(["Lorem", "Ipsum", "Dolor"]))
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_smartart_basic_bending_process_002(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(SmartArt.basic_bending_process(["Lorem", "Ipsum", "Dolor", "Sit"]))
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_smartart_basic_bending_process_003(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.basic_bending_process(["Lorem", "Ipsum", "Dolor", "Sit", "Amet"])
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_smartart_basic_bending_process_004(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.basic_bending_process(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Consectetur"]
            )
        )
        with open(self.get_fourth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_smartart_basic_bending_process_005(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.basic_bending_process(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Consectetur", "Adipiscing"]
            )
        )
        with open(self.get_fifth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_smartart_basic_bending_process_006(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.basic_bending_process(
                [
                    "Lorem",
                    "Ipsum",
                    "Dolor",
                    "Sit",
                    "Amet",
                    "Consectetur",
                    "Adipiscing",
                    "Elit",
                ]
            )
        )
        with open(self.get_sixth_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())
