import os
import unittest
from pathlib import Path

from borb.io.write.transformer import WriteTransformerState
from borb.pdf.pdf import PDF
from borb.toolkit.image.image_format_optimization import ImageFormatOptimization
from tests.test_case import TestCase


class TestOptimizeImages(TestCase):
    def test_optimize_images(self):

        input_file: Path = self.get_artifacts_directory() / "input_001.pdf"
        with open(input_file, "rb") as pdf_file_handle:
            l = ImageFormatOptimization()
            doc = PDF.loads(pdf_file_handle, [l])

        output_file: Path = self.get_artifacts_directory() / "output_001.pdf"
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
