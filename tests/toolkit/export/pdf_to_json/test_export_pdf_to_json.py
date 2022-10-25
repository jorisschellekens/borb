import json
import unittest
from pathlib import Path

from borb.pdf.pdf import PDF


class TestExportPDFToJSON(unittest.TestCase):
    """
    This test attempts to export each PDF in the corpus to JSON
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

    def test_convert_pdf_to_json(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            with open(self.output_dir / "output.json", "w") as json_file_handle:
                json_file_handle.write(json.dumps(doc.to_json_serializable(), indent=4))


if __name__ == "__main__":
    unittest.main()
