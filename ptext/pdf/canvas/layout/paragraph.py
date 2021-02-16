import typing
import zlib
from enum import Enum
from typing import Union

from ptext.io.read.types import Stream, Name, Dictionary, Decimal, String
from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.font.afm.adobe_font_metrics import AdobeFontMetrics
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.font.font_type_1 import FontType1
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


class LayoutElement:
    def __init__(
        self,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        parent: typing.Optional["LayoutElement"] = None,
    ):
        self.border_top = border_top
        self.border_right = border_right
        self.border_bottom = border_bottom
        self.border_left = border_left
        assert border_width >= 0
        self.border_width = border_width
        self.border_color = border_color
        self.parent = parent
        self.bounding_box = typing.Optional[Rectangle]

    def set_bounding_box(self, bounding_box: Rectangle) -> "LayoutElement":
        self.bounding_box = bounding_box
        return self

    def get_bounding_box(self) -> typing.Optional[Rectangle]:
        return self.bounding_box

    def _initialize_page_content_stream(self, page: Page):
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

    def _append_to_content_stream(self, page: Page, instructions: str):
        self._initialize_page_content_stream(page)
        content_stream = page["Contents"]
        content_stream["DecodedBytes"] += instructions.encode("utf8")
        content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
        content_stream[Name("Length")] = Decimal(len(content_stream["Bytes"]))

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:
        self.set_bounding_box(bounding_box)
        return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))

    def draw_border(self, page: Page, border_box: Rectangle):
        # border is not wanted on any side
        if (
            self.border_top
            == self.border_right
            == self.border_bottom
            == self.border_right
            == False
        ):
            return
        # border width is set to zero
        if self.border_width == 0:
            return
        # draw border(s)
        rgb_color = self.border_color.to_rgb()
        COLOR_MAX = Decimal(255.0)
        content = "q %f %f %f RG %f w" % (
            Decimal(rgb_color.red / COLOR_MAX),
            Decimal(rgb_color.green / COLOR_MAX),
            Decimal(rgb_color.blue / COLOR_MAX),
            self.border_width,
        )
        if self.border_top:
            content += " %f %f m %f %f l s" % (
                border_box.x,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y + border_box.height,
            )
        if self.border_right:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y + border_box.height,
                border_box.x + border_box.width,
                border_box.y,
            )
        if self.border_bottom:
            content += " %d %d m %d %d l s" % (
                border_box.x + border_box.width,
                border_box.y,
                border_box.x,
                border_box.y,
            )
        if self.border_left:
            content += " %d %d m %d %d l s" % (
                border_box.x,
                border_box.y,
                border_box.x,
                border_box.y + border_box.height,
            )
        content += " Q "
        self._append_to_content_stream(page, content)


class ChunkOfText(LayoutElement):
    def __init__(
        self,
        text: str,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        font_color: Color = X11Color("Black"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        parent: typing.Optional["LayoutElement"] = None,
    ):
        super(ChunkOfText, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            parent=parent,
        )
        self.text = text
        if isinstance(font, str):
            self.font: Font = FontType1()
            font_to_copy: typing.Optional[Font] = AdobeFontMetrics.get(font)
            assert font_to_copy
            for k, v in font_to_copy.items():
                self.font[k] = v
            assert self.font
        else:
            self.font = font
        self.font_color = font_color
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
        rgb_color = self.font_color.to_rgb()
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
            float(bounding_box.y + bounding_box.height - self.font_size),
            self.text,
        )
        self._append_to_content_stream(page, content)
        layout_rect = Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self.font_size,
            self.font.build_glyph_line(String(self.text)).get_width_in_text_space(
                self.font_size
            ),
            self.font_size,
        )

        # draw border
        self.draw_border(page, layout_rect)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect


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
        font_color: Color = X11Color("Black"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        parent: typing.Optional["LayoutElement"] = None,
    ):
        super(LineOfText, self).__init__(
            text=text,
            font=font,
            font_size=font_size,
            font_color=font_color,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            parent=parent,
        )
        self.justification = justification

    def layout(self, page: Page, bounding_box: Rectangle):
        assert self.font
        if self.justification == Justification.FLUSH_LEFT:
            return super(LineOfText, self).layout(page, bounding_box)

        # calculate width of glyph line
        glyph_line: GlyphLine = self.font.build_glyph_line(String(self.text))
        glyph_line_width = glyph_line.get_width_in_text_space(self.font_size)
        remaining_space = max(bounding_box.get_width() - glyph_line_width, Decimal(0))

        if self.justification == Justification.FLUSH_RIGHT:
            layout_rect = super(LineOfText, self).layout(
                page,
                Rectangle(
                    bounding_box.x + remaining_space,
                    bounding_box.y,
                    glyph_line_width,
                    bounding_box.height,
                ),
            )

        elif self.justification == Justification.CENTERED:
            half_of_remaining_space = remaining_space / Decimal(2)
            bounds = Rectangle(
                bounding_box.x + half_of_remaining_space,
                bounding_box.y,
                glyph_line_width,
                bounding_box.height,
            )
            layout_rect = super(LineOfText, self).layout(
                page,
                bounds,
            )

        elif self.justification == Justification.JUSTIFIED:
            number_of_spaces: Decimal = Decimal(sum([1 for x in self.text if x == " "]))
            if number_of_spaces > 0:
                space_per_space: Decimal = remaining_space / number_of_spaces
            else:
                space_per_space = Decimal(0)
            words: typing.List[str] = self.text.split(" ")
            x: Decimal = bounding_box.x
            for w in words:
                s = w + " "
                ChunkOfText(
                    s,
                    font=self.font,
                    font_size=self.font_size,
                    font_color=self.font_color,
                    parent=self,
                ).layout(
                    page,
                    bounding_box=Rectangle(
                        x, bounding_box.y, bounding_box.width, bounding_box.height
                    ),
                )
                word_size = self.font.build_glyph_line(
                    String(s)
                ).get_width_in_text_space(self.font_size)
                x += word_size
                x += space_per_space
            layout_rect = Rectangle(
                bounding_box.x, bounding_box.y, bounding_box.width, self.font_size
            )

        # draw border
        self.draw_border(page, layout_rect)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect


class Paragraph(LineOfText):
    """
    A paragraph (from the Ancient Greek παράγραφος, parágraphos, "to write beside")
    is a self-contained unit of discourse in writing dealing with a particular point or idea.
    A paragraph consists of one or more sentences. Though not required by the syntax of any language,
    paragraphs are usually an expected part of formal writing, used to organize longer prose.
    """

    def __init__(
        self,
        text: str,
        font: Union[Font, str] = "Helvetica",
        font_size: Decimal = Decimal(12),
        justification: Justification = Justification.FLUSH_LEFT,
        font_color: Color = X11Color("Black"),
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        parent: typing.Optional["LayoutElement"] = None,
    ):
        super(Paragraph, self).__init__(
            text=text,
            font=font,
            font_size=font_size,
            justification=justification,
            font_color=font_color,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            parent=parent,
        )

    def layout(self, page: Page, bounding_box: Rectangle):
        # easy case
        if len(self.text) == 0:
            return Rectangle(bounding_box.x, bounding_box.y, Decimal(0), Decimal(0))
        # determine how to break text to fit
        lines_of_text = []
        last_line_of_text = ""
        words = self.text.split(" ")
        for i, w in enumerate(words):
            potential_text = last_line_of_text
            if i != 0:
                potential_text += " "
            potential_text += w
            potential_width = self.font.build_glyph_line(
                String(potential_text)
            ).get_width_in_text_space(self.font_size)
            if potential_width > bounding_box.width:
                lines_of_text.append(last_line_of_text)
                last_line_of_text = w
            else:
                if i != 0:
                    last_line_of_text += " "
                last_line_of_text += w

        # append last line
        if len(last_line_of_text) > 0:
            lines_of_text.append(last_line_of_text)

        # delegate
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)
        leading: Decimal = self.font_size * Decimal(1.3)
        for i, l in enumerate(lines_of_text):
            r = LineOfText(
                l,
                font=self.font,
                font_size=self.font_size,
                justification=self.justification,
                font_color=self.font_color,
                parent=self,
            ).layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y + bounding_box.height - leading * i - self.font_size,
                    bounding_box.width,
                    self.font_size,
                ),
            )
            min_x = min(r.x, min_x)
            min_y = min(r.y, min_y)
            max_x = max(r.x + r.width, max_x)
            max_y = max(r.y + r.height, max_y)
        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

        # draw border
        self.draw_border(page, layout_rect)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
