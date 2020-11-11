from typing import Any, Optional

import PIL.Image

from ptext.object.canvas.xobject.image import Image


class JPEGImage(Image):
    def __init__(self):
        super().__init__()
        self.image = None

    def read(self, bytes_in: bytes) -> "JPEGImage":
        self.image = PIL.Image.open(bytes_in)
        return self

    def get_PIL_image(self) -> Optional[PIL.Image.Image]:
        return self.image

    def get_width(self) -> int:
        return self.get("Width").get_int_value()

    def get_height(self) -> int:
        return self.get("Height").get_int_value()

    def get_pixel(self, x: int, y: int) -> Any:
        return self.image.getpixel((x, y))
