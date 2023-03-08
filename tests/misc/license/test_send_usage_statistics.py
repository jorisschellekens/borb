import unittest
from pathlib import Path

from borb.license.anonymous_user_id import AnonymousUserID
from borb.pdf import Document, Page, SingleColumnLayout, PageLayout, Paragraph, PDF


class TestSendUsageStatistics(unittest.TestCase):
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

    def test_send_usage_statistics(self):
        def _get_user_id() -> str:
            return "developer-user-id-jsc"

        # monkey patching
        prev_user_id_function = AnonymousUserID.get
        AnonymousUserID.get = _get_user_id

        # build tiny little Document
        d: Document = Document()

        p: Page = Page()
        d.add_page(p)

        l: PageLayout = SingleColumnLayout(p)
        for _ in range(0, 32):
            l.add(Paragraph("Hello World"))

        # determine output location
        out_file = self.output_dir / "output.pdf"
        with open(out_file, "wb") as out_file_handle:
            PDF.dumps(out_file_handle, d)

        # restore
        AnonymousUserID.get = prev_user_id_function
