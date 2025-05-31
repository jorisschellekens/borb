import random
import typing
import unittest

from borb.pdf import (
    PDF,
    Document,
    Page,
    PageLayout,
    SingleColumnLayout,
    Paragraph,
    X11Color,
    Lipsum,
)
from borb.pdf.toolkit.pipeline import Pipeline
from borb.pdf.toolkit.sink.get_regular_expression import GetRegularExpression, MatchType
from borb.pdf.toolkit.source.operator.source import Source


class TestGetRegularExpression(unittest.TestCase):

    def test_get_regular_expression(self):

        # step 1: build PDF
        d: Document = Document()
        p: Page = Page()
        d.append_page(p)
        l: PageLayout = SingleColumnLayout(p)

        # generate title
        random.seed(0)
        l.append_layout_element(
            Paragraph(
                Lipsum.generate_lorem_ipsum(32),
                font_size=20,
                font_color=X11Color.PRUSSIAN_BLUE,
            )
        )

        # generate text
        l.append_layout_element(Paragraph(Lipsum.generate_lorem_ipsum(512)))
        PDF.write(what=d, where_to="assets/output.pdf")

        # step 2: read PDF
        d: Document = PDF.read("assets/output.pdf")

        # step 3: process
        matches: typing.List[MatchType] = Pipeline(
            [Source(), GetRegularExpression(pattern="philosophos .* esset")]
        ).process(d)

        # step 4: check some stuff
        assert len(matches) == 1
        assert 0 in matches
        assert len(matches[0]) == 2
        assert matches[0][0].bounding_boxes == [(385, 668, 64, 12), (454, 668, 39, 12)]
