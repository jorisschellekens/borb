from typing import Any

from ptext.object.pdf_high_level_object import PDFHighLevelObject


class Image(PDFHighLevelObject):
    def get_width(self) -> int:
        return 0

    def get_height(self) -> int:
        return 0

    def get_pixel(self, x: int, y: int) -> Any:
        return (0, 0, 0)
