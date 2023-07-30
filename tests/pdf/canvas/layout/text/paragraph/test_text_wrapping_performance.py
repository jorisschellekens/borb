import time
import typing
import unittest
from pathlib import Path

import requests

from borb.pdf import Document
from borb.pdf import Lipsum
from borb.pdf import PDF
from borb.pdf import Page
from borb.pdf import PageLayout
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from tests.test_case import TestCase

unittest.TestLoader.sortTestMethodsUsing = None


class TestTextWrappingPerformance(TestCase):
    @staticmethod
    def get_the_odyssey_by_homer() -> str:
        return requests.get("https://www.gutenberg.org/files/1727/old/1727.txt").text

    def test_layout_odyssey(self):
        text: str = TestTextWrappingPerformance.get_the_odyssey_by_homer()

        # do this for the first 10Kb
        timing_information: typing.Dict[int, typing.List[float]] = {}

        # load the font once
        helvetica: Font = StandardType1Font("Helvetica")

        # iterate
        for i in range(1024, min(len(text), 1024 * 10), 1024):
            for _ in range(0, 5):
                # create Document
                doc: Document = Document()

                # create Page
                page: Page = Page()
                doc.add_page(page)

                # create PageLayout
                layout: PageLayout = SingleColumnLayout(page)

                # start timing the layout information
                t0: float = time.time()
                lines: typing.List[str] = [x.strip() for x in text[0:i].split("\n")]
                for l in lines:
                    if l == "":
                        l = ":"
                    layout.add(Paragraph(l, font=helvetica))
                t0 = time.time() - t0

                # append
                if i not in timing_information:
                    timing_information[i] = []
                timing_information[i].append(t0)

            # take average time
            avg: float = sum(timing_information[i]) / len(timing_information[i])

            # expected linear trend
            expected_avg: float = (i * 0.001046836) + 0.297549662

            # debug
            print("%d\t%f" % (i, avg))

            # check
            # fmt: off
            assert (avg < expected_avg + 2), "Expected Paragraph layout to take max. %f seconds, it took %f" % (expected_avg, avg)
            # fmt: on

            # write
            output_file: Path = self.get_artifacts_directory() / ("output_%d.pdf" % i)
            with open(output_file, "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, doc)
