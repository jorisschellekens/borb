from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import SmartArt
from tests.test_case import TestCase


class TestAddSmartArtOpposingIdeas(TestCase):
    def test_add_smartart_opposing_ideas(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.opposing_ideas(
                [
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip",
                    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
                ]
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
