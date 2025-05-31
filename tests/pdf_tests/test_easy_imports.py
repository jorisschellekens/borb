import random
import unittest

from borb.pdf import (
    Document,
    Page,
    SingleColumnLayout,
    Paragraph,
    Lipsum,
    PDF,
    PageLayout,
    GoogleTrueTypeFont,
)
from borb.pdf.conformance import Conformance
from tests.secrets import populate_os_environ


class TestEasyImports(unittest.TestCase):

    def test_easy_imports(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        l: PageLayout = SingleColumnLayout(p)

        random.seed(0)
        l.append_layout_element(
            Paragraph(Lipsum.generate_lorem_ipsum(300), font_size=4)
        )

        PDF.write(what=d, where_to="assets/test_easy_imports.pdf")
