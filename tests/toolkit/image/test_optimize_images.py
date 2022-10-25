import os
import unittest
from pathlib import Path

from borb.io.write.transformer import WriteTransformerState
from borb.pdf.pdf import PDF
from borb.toolkit.image.image_format_optimization import ImageFormatOptimization


class TestOptimizeImages(unittest.TestCase):
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

    def test_optimize_images(self):

        input_file: Path = Path(__file__).parent / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = ImageFormatOptimization()
            doc = PDF.loads(pdf_file_handle, [l])

        output_file: Path = self.output_dir / "output_001.pdf"
        with open(output_file, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, doc)

        # check WriteTransformerState
        assert (
            WriteTransformerState().compression_level == 9
        ), "WriteTransformerState.compression_level should be set at 9 for optimal results!"

        # check whether output_file is smaller than input_file
        file_size_001: int = os.path.getsize(input_file)
        file_size_002: int = os.path.getsize(output_file)
        assert file_size_002 < file_size_001


if __name__ == "__main__":
    unittest.main()
