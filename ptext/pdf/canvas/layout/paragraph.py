import zlib
from enum import Enum
from typing import Union

from ptext.io.read.types import Stream, Name, Dictionary, Decimal, String
from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.font.afm.adobe_font_metrics import AdobeFontMetrics
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


class LayoutElement:
    def initialize_page_content_stream(self, page: Page):
        if "Contents" in page:
            return

        # build content stream object
        content_stream = Stream()
        content_stream[Name("DecodedBytes")] = b""
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Filter")] = Name("FlateDecode")
        content_stream[Name("Length")] = Decimal(len(content_stream["Bytes"]))

        # set content of page
        page[Name("Contents")] = content_stream

    def append_to_content_stream(self, page: Page, instructions: str):
        self.initialize_page_content_stream(page)
        content_stream = page["Contents"]
        content_stream["DecodedBytes"] += instructions.encode("utf8")
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Length")] = Decimal(len(content_stream["Bytes"]))


class ChunkOfText(LayoutElement):
    def __init__(
        self,
        text: str,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        color: Color = X11Color("Black"),
    ):
        self.text = text
        if isinstance(font, str):
            self.font = AdobeFontMetrics.get(font)
            assert self.font
        else:
            self.font = font
        self.color = color
        self.font_size = font_size

    def get_font_resource_name(self, font: Font, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)  # type: ignore [attr-defined]
        if "Font" not in page["Resources"]:
            page["Resources"][Name("Font")] = Dictionary()

        # insert font into resources
        font_resource_name = [
            k for k, v in page["Resources"]["Font"].items() if v == font
        ]
        if len(font_resource_name) > 0:
            return font_resource_name[0]
        else:
            font_index = len(page["Resources"]["Font"]) + 1
            page["Resources"]["Font"][Name("F%d" % font_index)] = font
            return Name("F%d" % font_index)

    def layout(self, page: Page, bounding_box: Rectangle):
        assert self.font
        rgb_color = self.color.to_rgb()
        COLOR_MAX = Decimal(255.0)
        content = """
            q
            BT
            %f %f %f rg
            /%s %f Tf            
            %f %f Td            
            (%s) Tj
            ET            
            Q
        """ % (
            Decimal(rgb_color.red / COLOR_MAX),
            Decimal(rgb_color.green / COLOR_MAX),
            Decimal(rgb_color.blue / COLOR_MAX),
            self.get_font_resource_name(self.font, page),
            float(self.font_size),
            float(bounding_box.x),
            float(bounding_box.y),
            self.text,
        )
        self.append_to_content_stream(page, content)


class Justification(Enum):
    """
    In typesetting and page layout, alignment or range is the setting of text flow or image placement relative to a page,
    column (measure), table cell, or tab.
    The type alignment setting is sometimes referred to as text alignment,
    text justification, or type justification.
    The edge of a page or column is known as a margin, and a gap between columns is known as a gutter.
    """

    FLUSH_LEFT = (2,)
    FLUSH_RIGHT = (3,)
    JUSTIFIED = (5,)
    CENTERED = 7


class LineOfText(ChunkOfText):
    def __init__(
        self,
        text: str,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        justification: Justification = Justification.FLUSH_LEFT,
        color: Color = X11Color("Black"),
    ):
        super(LineOfText, self).__init__(text, font, font_size, color)
        self.justification = justification

    def layout(self, page: Page, bounding_box: Rectangle):
        assert self.font
        glyph_line: GlyphLine = self.font.build_glyph_line(String(self.text))
        pass


class Paragraph(LineOfText):
    def __init__(
        self,
        text: str,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        justification: Justification = Justification.FLUSH_LEFT,
        color: Color = X11Color("Black"),
    ):
        super(Paragraph, self).__init__(text, font, font_size, justification, color)
