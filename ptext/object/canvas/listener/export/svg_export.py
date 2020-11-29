import xml.etree.ElementTree as ET
from typing import Optional, Tuple

from ptext.object.canvas.event.begin_page_event import BeginPageEvent
from ptext.object.canvas.event.end_page_event import EndPageEvent
from ptext.object.canvas.event.image_render_event import ImageRenderEvent
from ptext.object.canvas.event.text_render_event import TextRenderEvent
from ptext.object.canvas.listener.structure.line.line_render_event import (
    LineRenderEvent,
)
from ptext.object.canvas.listener.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)
from ptext.object.page.page_size import PageSize
from ptext.object.event_listener import EventListener, Event


class SVGExport(EventListener):
    """
    This implementation of EventListener exports a Page as an SVG
    """

    def __init__(
        self,
        include_document_information: bool = False,
        default_page_size: Optional[Tuple[float, float]] = PageSize.A4_PORTRAIT.value,
    ):
        self.svg_element_per_page = {}

        # global settings
        self.include_document_information = include_document_information
        self.default_page_size = default_page_size

        # page being rendered
        self.current_page_width = None
        self.current_page_height = None
        self.current_page_svg_element = None
        self.current_page = -1

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, ParagraphRenderEvent):
            self.render_paragraph(event)
            return
        if isinstance(event, LineRenderEvent):
            self.render_text_line(event)
            return

        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())
        if isinstance(event, TextRenderEvent):
            self._render_text(event)
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def _begin_page(self, page: "Page"):

        # get page nr
        self.current_page += 1

        # get page size
        page_size = page.get_page_info().get_size()
        if page_size is None and self.default_page_size is None:
            return
        if page_size == (None, None):
            page_size = self.default_page_size

        self.current_page_width = page_size[0]
        self.current_page_height = page_size[1]

        # init svg image
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        svg_element = ET.Element("svg")
        svg_element.set(
            "viewbox", "0 0 %d %d" % (self.current_page_width, self.current_page_height)
        )

        # meta properties
        if self.include_document_information:
            document_info = page.get_document().get_document_info()
            for method, name in [
                (document_info.get_title, "dc:title"),
                (document_info.get_author, "dc:author"),
                (document_info.get_creator, "dc:creator"),
                (document_info.get_producer, "dc:producer"),
            ]:
                if method() is not None:
                    e = ET.Element("desc")
                    e.set("property", name)
                    e.text = method().get_text()
                    svg_element.append(e)

        # white background
        rct_element = ET.Element("rect")
        rct_element.set("width", str(self.current_page_width))
        rct_element.set("height", str(self.current_page_height))
        rct_element.set("style", "fill:rgb(255, 255, 255);")
        svg_element.append(rct_element)
        self.current_page_svg_element = svg_element

    def _end_page(self, page: "Page"):

        # store
        self.svg_element_per_page[self.current_page] = self.current_page_svg_element

        # reset
        self.current_page_width = None
        self.current_page_height = None
        self.current_page_svg_element = None

    def get_svg(self, page_number: int) -> ET.Element:
        return self.svg_element_per_page[page_number]

    def _render_text(self, text_render_info: "TextRenderInfo"):

        if text_render_info.get_text() is None:
            return

        if len(text_render_info.get_text().replace(" ", "")) == 0:
            return

        # color
        r = int(text_render_info.font_color.to_rgb().red * 255)
        g = int(text_render_info.font_color.to_rgb().green * 255)
        b = int(text_render_info.font_color.to_rgb().blue * 255)

        # font size
        fs = text_render_info.get_font_size()

        # COORDINATE TRANSFORM:
        # In PDF coordinate space the origin is at the bottom left of the page,
        # for SVG images, the origin is the top left.
        bl = text_render_info.get_baseline()
        x = int(bl.x0)
        y = int(self.current_page_height - bl.y0)

        # build text element
        text_element = ET.Element("text")
        if text_render_info.get_font_family() is not None:
            font_family_name = text_render_info.get_font_family()

            # check whether the font is bold
            is_bold = False
            bold_name_part = [
                "Bold",
                "bold",
                ",Bold,",
                ",bold,",
                ",Bold",
                ",bold",
                "Bold,",
                "bold,",
            ]
            for bn in bold_name_part:
                if bn in font_family_name:
                    font_family_name = font_family_name.replace(bn, "")
                    is_bold = True
            if is_bold:
                text_element.set("font-weight", "bold")

            # check whether the font is italic
            is_italic = False
            italic_name_part = [
                "Italic",
                "italic",
                ",Italic,",
                ",italic,",
                ",Italic",
                ",italic",
                "Italic,",
                "italic,",
            ]
            for bn in italic_name_part:
                if bn in font_family_name:
                    font_family_name = font_family_name.replace(bn, "")
                    is_italic = True
            if is_italic:
                text_element.set("font-style", "italic")

            # font family trimming
            if font_family_name.endswith(","):
                font_family_name = font_family_name[:-1]

            # set font-family
            text_element.set("font-family", font_family_name)
        text_element.set("x", str(x))
        text_element.set("y", str(y))
        text_element.set(
            "style", "fill:rgb(%d, %d, %d); font-size:%d px;" % (r, g, b, fs)
        )
        if (
            text_render_info.get_text().startswith(" ")
            or "  " in text_render_info.get_text()
        ):
            text_element.set("xml:space", "preserve")
            text_element.set(
                "style",
                "fill:rgb(%d, %d, %d); font-size:%d px; white-space: pre;"
                % (r, g, b, fs),
            )
        text_element.text = text_render_info.get_text()

        # append to page
        self.current_page_svg_element.append(text_element)

    def _render_image(self, event: ImageRenderEvent):

        # build img element
        img_element = ET.Element("g")

        w = int(event.get_width())
        h = int(event.get_height())

        # COORDINATE TRANSFORM:
        # In PDF coordinate space the origin is at the bottom left of the page,
        # for SVG images, the origin is the top left.
        x = int(event.get_x())
        y = int(self.current_page_height - event.get_y() - event.get_height())

        # set pixels
        for i in range(0, w):
            for j in range(0, h):
                c = event.get_rgb(i, j)
                pixel_element = ET.Element("rect")
                pixel_element.set(
                    "style", "fill:rgb(%d, %d, %d);" % (c.red, c.green, c.blue)
                )
                pixel_element.set("x", str(x + i))
                pixel_element.set("y", str(y + j))
                pixel_element.set("width", "1")
                pixel_element.set("height", "1")
                img_element.append(pixel_element)

        self.current_page_svg_element.append(img_element)

    def render_text_line(self, event: LineRenderEvent):
        bb = event.get_bounding_box()
        y = int(self.current_page_height - bb.y - bb.height)
        line_element = ET.Element("rect")
        line_element.set("x", str(bb.x))
        line_element.set("y", str(y))
        line_element.set("width", str(bb.width))
        line_element.set("height", str(bb.height))
        line_element.set(
            "style", "stroke: rgb(255, 0, 0); stroke-width: 1; fill: none;"
        )
        self.current_page_svg_element.append(line_element)

    def render_paragraph(self, event: ParagraphRenderEvent):
        bb = event.get_bounding_box()
        y = int(self.current_page_height - bb.y - bb.height)
        line_element = ET.Element("rect")
        line_element.set("x", str(bb.x))
        line_element.set("y", str(y))
        line_element.set("width", str(int(bb.width)))
        line_element.set("height", str(bb.height))
        line_element.set(
            "style", "stroke: rgb(0, 255, 255); stroke-width: 1; fill: none;"
        )
        self.current_page_svg_element.append(line_element)
