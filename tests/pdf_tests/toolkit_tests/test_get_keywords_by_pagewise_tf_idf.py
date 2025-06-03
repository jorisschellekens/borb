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
from borb.pdf.toolkit.sink.get_keywords_by_pagewise_tf_idf import (
    GetKeywordsByPagewiseTFIDF,
)
from borb.pdf.toolkit.sink.get_regular_expression import MatchType
from borb.pdf.toolkit.source.operator.source import Source


class TestGetKeywordsByPagewiseTFIDF(unittest.TestCase):

    def test_get_keywords_by_pagewise_tf_idf(self):

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
        for _ in range(0, 10):
            l.append_layout_element(Paragraph(Lipsum.generate_arthur_conan_doyle(512)))
        PDF.write(what=d, where_to="assets/output.pdf")

        # step 2: read PDF
        d: Document = PDF.read("assets/output.pdf")

        # step 3: process
        keywords: typing.List[MatchType] = Pipeline(
            [Source(), GetKeywordsByPagewiseTFIDF()]
        ).process(d)

        # step 4: check some stuff
        print(keywords)
