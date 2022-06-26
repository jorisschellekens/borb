import typing
import unittest
from pathlib import Path

from borb.pdf import Document, PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestDocumentHasSignatures(unittest.TestCase):
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

    def test_document_has_signatures_001(self):

        # read Document
        doc: typing.Optional[Document] = None
        with open("hello_world_signed_initials_001.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # check whether we have read the Document
        assert doc is not None

        # check whether the Document has signatures
        assert doc.get_document_info().has_signatures() == False

    def test_document_has_signatures_002(self):

        # read Document
        doc: typing.Optional[Document] = None
        with open("hello_world_signed_initials_002.pdf", "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)

        # check whether we have read the Document
        assert doc is not None

        # check whether the Document has signatures
        assert doc.get_document_info().has_signatures()
