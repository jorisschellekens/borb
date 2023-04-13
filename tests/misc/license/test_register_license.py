import unittest
from pathlib import Path

from borb.license.license import License
from borb.license.usage_statistics import UsageStatistics
from borb.pdf import Document, Page, SingleColumnLayout, PageLayout, Paragraph, PDF


class TestRegisterLicense(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_register_license(self):
        assert License.register(Path(__file__).parent / "license.json")
        assert UsageStatistics._get_user_id() == "Joris Schellekens"

    def test_create_document_with_license(self):
        assert License.register(Path(__file__).parent / "license.json")
        assert UsageStatistics._get_user_id() == "Joris Schellekens"

        doc: Document = Document()

        page: Page = Page()
        doc.add_page(page)

        layout: PageLayout = SingleColumnLayout(page)
        layout.add(Paragraph("Hello World"))

        # determine output location
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)
