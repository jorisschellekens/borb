from typing import List, Optional, Tuple

from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.pdf_high_level_object import Event
from ptext.primitive.pdf_string import PDFString, PDFHexString, PDFLiteralString


class ImageRenderEvent(Event):
    def __init__(self, graphics_state: "CanvasGraphicsState", image: "Image"):
        self.image = image

        # calculate position
        v = graphics_state.ctm.cross(0, 0, 1)
        self.x = int(v[0])
        self.y = int(v[1])

        # calculate display size
        v = graphics_state.ctm.cross(1, 1, 0)
        self.width = max(abs(int(v[0])), 1)
        self.height = max(abs(int(v[1])), 1)

        # scaled image
        self.scaled_image = self.image.image.resize((self.width, self.height))

    def get_image(self) -> int:
        return self.image

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_rgb(self, x: int, y: int) -> Tuple[int, int, int]:
        c = self.scaled_image.getpixel((x, y))
        if self.scaled_image.mode == "RGB":
            return c
        if self.scaled_image.mode == "RGBA":
            return (c[0], c[1], c[2])
        if self.scaled_image.mode == "CMYK":
            return (
                int((1 - c[0]) * (1 - c[3]) / 255),
                int((1 - c[1]) * (1 - c[3]) / 255),
                int((1 - c[2]) * (1 - c[0]) / 255),
            )
