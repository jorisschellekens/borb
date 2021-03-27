import logging
import re
import unittest
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.pdf import PDF
from ptext.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test import Test
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-add-square-annotation-around-word.log"),
    level=logging.DEBUG,
)


class TestAddSquareAnnotationAroundWord(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(
            get_output_dir(), "test-add-square-annotation-around-word"
        )

    def test_exact_document(self):
        self._test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    @unittest.skip
    def test_corpus(self):
        super(TestAddSquareAnnotationAroundWord, self).test_corpus()

    def _test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # get text
        txt_ground_truth_file = self.input_dir / (file.stem + ".txt")
        txt_ground_truth = ""
        with open(txt_ground_truth_file, "r") as txt_ground_truth_file_handle:
            txt_ground_truth = txt_ground_truth_file_handle.read()

        words = [x for x in re.split("[^a-zA-Z]+", txt_ground_truth) if len(x) > 5]
        w = words[5] if len(words) > 5 else None

        if w is None:
            return True

        # determine output location
        out_file = self.output_dir / (file.stem + "_" + w + "_out.pdf")

        # attempt to read PDF
        doc = None
        l = RegularExpressionTextExtraction(w)
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle, [l])

        # add annotation
        print(
            "\tAdding %d annotations"
            % len(l.get_matched_chunk_of_text_render_events_per_page(0))
        )
        for e in l.get_matched_chunk_of_text_render_events_per_page(0):
            doc.get_page(0).append_square_annotation(
                e.get_bounding_box(),
                stroke_color=X11Color("Firebrick"),
            )

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)

        return True
