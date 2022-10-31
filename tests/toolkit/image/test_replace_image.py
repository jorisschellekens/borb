import unittest
from pathlib import Path
from PIL import Image

from borb.pdf.pdf import PDF


class TestReplaceImage(unittest.TestCase):
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

    def test_replace_image(self):

        input_file: Path = Path(__file__).parent / "input_002.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
        replacement_image = Image.open(Path(__file__).parent / "input_replacement_002.png")

        image = list(doc.get_page(0)["Resources"]["XObject"].values())[0]
        image.paste(replacement_image)

        output_file: Path = self.output_dir / "output_001.pdf"
        with open(output_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)


if __name__ == "__main__":
    unittest.main()
