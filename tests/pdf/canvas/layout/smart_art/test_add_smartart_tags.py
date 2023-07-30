from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import SmartArt
from tests.test_case import TestCase


class TestAddSmartArtTags(TestCase):
    def test_add_smartart_tags_001(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(SmartArt.tags(["Lorem", "Ipsum", "Dolor", "Sit", "Amet"]))
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_smartart_tags_002(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.tags(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet"],
                background_color=HexColor("56cbf9"),
            )
        )
        with open(self.get_second_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_smartart_tags_003(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.tags(
                ["Lorem", "Ipsum", "Dolor", "Sit", "Amet", "Amet", "AMET", "AMET"]
            )
        )
        with open(self.get_third_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())
