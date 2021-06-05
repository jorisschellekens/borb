import json
import unittest
from pathlib import Path

from ptext.pdf.document import Document
from ptext.pdf.pdf import PDF
from ptext.toolkit.export.json_to_pdf import JSONToPDF


class TestExportJSONToPDF(unittest.TestCase):
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

    def test(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        for file_to_convert in [
            "example-json-input-001.json",
            "example-json-input-002.json",
            "example-json-input-003.json",
        ]:

            json_data = None
            path_to_json = Path(__file__).parent / file_to_convert
            with open(path_to_json, "r") as json_file_handle:
                json_data = json.loads(json_file_handle.read())

            # convert
            document: Document = JSONToPDF.convert_json_to_pdf(json_data)

            # store
            output_file = self.output_dir / (file_to_convert + ".pdf")
            with open(output_file, "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, document)

        return True


if __name__ == "__main__":
    unittest.main()
