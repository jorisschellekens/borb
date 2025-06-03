import pathlib
import unittest

from borb.pdf import Document, PDF, Pipeline, Source
from borb.pdf.toolkit.sink.draw_bounding_boxes import DrawBoundingBoxes


class TestDrawBoundingBoxes(unittest.TestCase):

    # Path to the directory containing a collection of PDF documents used for testing.
    #
    # Users must adjust this path to match the location of the PDF corpus on their system
    # to run the tests successfully. A large collection of PDF documents is available
    # on the author's GitHub repository, which can be cloned or downloaded to use as the
    # test corpus.
    #
    # Ensure that the directory specified by this path exists and contains the necessary
    # PDF files before running the tests.
    CORPUS_DIRECTORY: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus"
    )

    def test_draw_bounding_boxes(self):
        d: Document = PDF.read(
            where_from=TestDrawBoundingBoxes.CORPUS_DIRECTORY / "0004.pdf"
        )

        Pipeline(
            [
                Source(),
                DrawBoundingBoxes(
                    text_event_indices_to_mark=[i for i in range(0, 20) if i % 2 == 0]
                ),
            ]
        ).process(d.get_page(0))

        PDF.write(what=d, where_to="assets/0004_b.pdf")
