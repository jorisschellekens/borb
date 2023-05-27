from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import SingleColumnLayout
from borb.pdf import SmartArt
from tests.test_case import TestCase


class TestAddSmartArtPictureList(TestCase):
    def test_add_smartart_picture_list(self):
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(
            self.get_test_header(test_description="This test adds SmartArt to a PDF.")
        )
        layout.add(
            SmartArt.picture_list(
                ["Lorem", "Ipsum", "Dolor"],
                [
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/512/Matryoshka-Leisure-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Music-icon.png",
                    "https://icons.iconarchive.com/icons/benschlitter/matryoshka/128/Matryoshka-Pictures-icon.png",
                ],
            )
        )
        with open(self.get_first_output_file(), "wb") as fh:
            PDF.dumps(fh, doc)
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())
