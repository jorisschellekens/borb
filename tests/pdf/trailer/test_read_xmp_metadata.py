import unittest
from pathlib import Path

from borb.pdf.pdf import PDF


class TestReadXMPMetaData(unittest.TestCase):
    """
    This test attempts to read the XMPDocumentInfo for each PDF in the corpus
    """

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

    def test_read_xmp_metadata(self):
        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            doc_info = doc.get_xmp_document_info()
            assert (
                doc_info.get_document_id()
                == "xmp.id:54e5adca-494c-4c10-983a-daa03cdae65a"
            )
            assert (
                doc_info.get_original_document_id()
                == "xmp.did:b857e947-9e0d-4cd3-aff9-40a81c991e7a"
            )


if __name__ == "__main__":
    unittest.main()
