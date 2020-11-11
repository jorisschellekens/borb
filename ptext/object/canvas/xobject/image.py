from typing import Any, Optional

import PIL.Image

from ptext.object.pdf_high_level_object import PDFHighLevelObject


class Image(PDFHighLevelObject):
    def get_PIL_image(self) -> Optional[PIL.Image.Image]:
        return None

    def get_width(self) -> int:
        return 0

    def get_height(self) -> int:
        return 0

    def get_pixel(self, x: int, y: int) -> Any:
        return (0, 0, 0)
