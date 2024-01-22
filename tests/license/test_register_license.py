from pathlib import Path

from borb.io.read.types import Decimal
from borb.license.license import License
from borb.license.async_usage_statistics import AsyncUsageStatistics
from borb.pdf import Document
from borb.pdf import HexColor
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from tests.test_case import TestCase


class TestRegisterLicense(TestCase):
    """
    These tests check the license mechanism
    """

    def test_register_license(self):
        license_file: Path = self.get_artifacts_directory() / "license.json"
        assert License.register(license_file)
        assert AsyncUsageStatistics._get_user_id() == "Joris Schellekens"

    def test_create_document_with_license(self):
        license_file: Path = self.get_artifacts_directory() / "license.json"
        assert License.register(license_file)
        assert AsyncUsageStatistics._get_user_id() == "Joris Schellekens"
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(Paragraph("Hello World"))
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

    def test_create_100_documents_with_license(self):

        license_file: Path = self.get_artifacts_directory() / "license.json"
        assert License.register(license_file)
        assert AsyncUsageStatistics._get_user_id() == "Joris Schellekens"

        # write PDF documents
        for _ in range(0, 100):
            d: Document = Document()
            p: Page = Page()
            d.add_page(p)
            l: SingleColumnLayout = SingleColumnLayout(p)
            l.add(
                Paragraph(
                    "Lorem Ipsum", font_color=HexColor("56cbf9"), font_size=Decimal(20)
                )
            )
            l.add(Paragraph(Lipsum.generate_lipsum_text(5)))
            with open(self.get_second_output_file(), "wb") as fh:
                PDF.dumps(fh, d)
