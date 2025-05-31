import math
import typing
import unittest
from io import BytesIO

from borb.pdf import PageLayout, SingleColumnLayout
from borb.pdf.document import Document
from borb.pdf.layout_element.image.emoji import Emoji
from borb.pdf.layout_element.image.image import Image
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestEmoji(unittest.TestCase):

    def test_single_emoji(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        layout: PageLayout = SingleColumnLayout(p)
        layout.append_layout_element(Emoji.BORB_STICKER)

        PDF.write(what=d,
                  where_to='assets/test_single_emoji.pdf')

    def test_emoji(self):

        # create Document
        d: Document = Document()

        # create Page
        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        # create Emoji object(s)
        emojis: typing.List[Image] = [getattr(Emoji, cn) for cn in dir(Emoji)[0:100]]

        N: int = int(math.sqrt(len(emojis)))
        for i in range(0, N):
            for j in range(0, N):
                emojis[i * N + j].paint(
                    available_space=(x + 32 * i, y - 32 * j, w, h), page=p
                )

        PDF.write(what=d, where_to="assets/test_emoji.pdf")
