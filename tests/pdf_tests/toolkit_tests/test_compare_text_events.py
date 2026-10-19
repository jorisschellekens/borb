import json
import pathlib
import typing
import unittest
import dataclasses

from borb.pdf import Source, Pipeline, PDF, Above, Pipe, Event, Sink, Page, GetText
from borb.pdf.primitives import stream
from borb.pdf.toolkit.source.event.text_event import TextEvent
from borb.pdf.visitor.read.compression.decode_stream import decode_stream


@dataclasses.dataclass
class Glyph:
    char: str
    x: int
    y: int


class AllTextEvents(Sink):

    def __init__(self) -> None:
        super().__init__()
        self.__glyphs: typing.List[Glyph] = []

    def process(self, event: Event) -> None:
        if isinstance(event, TextEvent):
            evt: TextEvent = event
            x: int = int(evt.get_x())
            y: int = int(evt.get_y())
            w: int = int(evt.get_width())
            s: str = evt.get_text()
            for i, c in enumerate(s):
                self.__glyphs += [Glyph(char=c, x=int(x + i * (w / len(s))), y=y)]

    def get_output(self) -> typing.Any:
        return {0: self.__glyphs}


class TestCompareTextEvents(unittest.TestCase):

    # Path to the directory containing a collection of PDF documents used for testing.
    #
    # Users must adjust this path to match the location of the PDF corpus on their system
    # to run the tests successfully. A large collection of PDF documents is available
    # on the author's GitHub repository, which can be cloned or downloaded to use as the
    # test corpus.
    #
    # Ensure that the directory specified by this path exists and contains the necessary
    # PDF files before running the tests.
    FIRST_PAGE_PDF_DIR: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus/first-page-pdf"
    )
    FIRST_PAGE_OPS_DIR: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-pdf-corpus/first-page-ops"
    )

    def _compare(
        self, max_x_delta: int, max_y_delta: int, pdf_nr: int
    ) -> typing.Tuple[int, int]:

        # load the text events
        glyphs_01: typing.List[Glyph] = []
        ops_file: pathlib.Path = (
            TestCompareTextEvents.FIRST_PAGE_OPS_DIR / f"{pdf_nr:04d}.json"
        )
        with open(ops_file) as fh:
            for obj in json.loads(fh.read()):
                x: int = obj["x"]
                y: int = obj["y"]
                w: int = obj["width"]
                s: str = obj["text"]
                for i, c in enumerate(s):
                    glyphs_01 += [Glyph(char=c, x=int(x + i * (w / len(s))), y=y)]

        # glyphs according to borb
        pdf_file: pathlib.Path = (
            TestCompareTextEvents.FIRST_PAGE_PDF_DIR / f"{pdf_nr:04d}.pdf"
        )

        glyphs_02: typing.List[Glyph] = []
        
        if ((document := PDF.read(where_from=pdf_file)) is not None):
            glyphs_02 = Pipeline([Source(), AllTextEvents()]).process(
                document
            )[0]

        # compare
        pos: int = 0
        neg: int = 0
        for g01 in glyphs_01:
            g02: typing.Optional[Glyph] = next(
                iter(
                    [
                        g
                        for g in glyphs_02
                        if abs(g.x - g01.x) <= max_x_delta
                        and abs(g.y - g01.y) <= max_y_delta
                    ]
                ),
                None,
            )
            if g02:
                pos += 1
            else:
                neg += 1

        # return
        return pos, neg

    def test_compare_text_events(self):

        xs = []
        ys0 = []
        ys1 = []
        ys2 = []
        for delta in [5, 10, 20, 25, 50]:

            # keep score
            percentages = []

            # measure over 100 pdfs
            for i in range(0, 104):
                if i in [25, 28, 46, 51]:
                    continue
                try:
                    pos, neg = self._compare(
                        max_x_delta=delta, max_y_delta=delta, pdf_nr=i
                    )
                    percentages += [pos / (pos + neg)]
                except:
                    pass

            # avg, min max
            average = sum(percentages) / len(percentages)
            minimum = min(percentages)
            maximum = max(percentages)

            # add to series
            xs += [delta]
            ys0 += [minimum]
            ys1 += [maximum]
            ys2 += [average]

        # plot
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        ax.plot(xs, ys0, label="Min")
        ax.plot(xs, ys1, label="Max")
        ax.plot(xs, ys2, label="Avg")

        ax.set_xlabel("x/y-delta")
        ax.set_ylabel("Matching Percentage")
        ax.legend()

        fig.savefig("test_compare_text_events.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
