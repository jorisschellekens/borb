from pathlib import Path

from borb.license.license import License
from borb.license.usage_statistics import UsageStatistics
from borb.pdf import Document
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
        assert UsageStatistics._get_user_id() == "Joris Schellekens"

    def test_create_document_with_license(self):
        license_file: Path = self.get_artifacts_directory() / "license.json"
        assert License.register(license_file)
        assert UsageStatistics._get_user_id() == "Joris Schellekens"
        doc: Document = Document()
        page: Page = Page()
        doc.add_page(page)
        layout: PageLayout = SingleColumnLayout(page)
        layout.add(Paragraph("Hello World"))
        with open(self.get_first_output_file(), "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
