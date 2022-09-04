import cProfile as profile
import pstats

import time
import typing
import unittest
from pathlib import Path

import requests
from borb.pdf import Document, Page, SingleColumnLayout, PageLayout, Paragraph, PDF

unittest.TestLoader.sortTestMethodsUsing = None


class TestTextWrappingPerformance(unittest.TestCase):
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

    def test_layout_odyssey(self):
        text: str = requests.get(
            "https://www.gutenberg.org/files/1727/old/1727.txt"
        ).text

        # do this for the first 10Kb
        timing_information: typing.Dict[int, typing.List[float]] = {}

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
                    layout.add(Paragraph(l))
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
            assert (
                avg < expected_avg + 2
            ), "Expected Paragraph layout to take max. %f seconds, it took %f" % (
                expected_avg,
                avg,
            )

            # write
            output_file: Path = self.output_dir / ("output_%d.pdf" % i)
            with open(output_file, "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, doc)
