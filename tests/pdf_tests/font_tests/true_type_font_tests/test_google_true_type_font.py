import unittest

from borb.pdf import Font, Page, Document, Chunk, PDF
from borb.pdf.font.simple_font.true_type.google_true_type_font import GoogleTrueTypeFont
from tests.secrets import populate_os_environ


class TestGoogleTrueTypeFont(unittest.TestCase):

    def test_google_true_type_font_001(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(name="Acme")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            font=font,
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_001.pdf")

    def test_google_true_type_font_002(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(name="Birthstone Bounce")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            font=font,
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_002.pdf")

    def test_google_true_type_font_003(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(name="Climate Crisis")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do", font=font
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_003.pdf")

    def test_google_true_type_font_004(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(
            name="Dawning of a New Day"
        )

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            font=font,
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_004.pdf")

    def test_google_true_type_font_005(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(name="EB Garamond")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            font=font,
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_005.pdf")

    def test_google_true_type_font_006(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # font
        populate_os_environ()
        font: Font = GoogleTrueTypeFont.from_google_font_api(name="Sansation")

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
        line_height: int = int(12 * 1.2)

        # paint Chunk(s)
        Chunk(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
            font=font,
        ).paint(available_space=(x, y, w, h), page=p)
        Chunk(
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim",
            font=font,
        ).paint(available_space=(x, y, w, h - line_height), page=p)
        Chunk(
            "ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
            font=font,
        ).paint(available_space=(x, y, w, h - 2 * line_height), page=p)
        Chunk(
            "aliquip ex ea commodo consequat. Duis aute irure dolor in", font=font
        ).paint(available_space=(x, y, w, h - 3 * line_height), page=p)
        Chunk(
            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
            font=font,
        ).paint(available_space=(x, y, w, h - 4 * line_height), page=p)
        Chunk("pariatur.", font=font).paint(
            available_space=(x, y, w, h - 5 * line_height), page=p
        )

        PDF.write(what=d, where_to="assets/test_google_true_type_font_006.pdf")