import typing
from decimal import Decimal
from typing import Optional

import requests
from PIL import Image as PILImage  # type: ignore [import]

from ptext.io.read.image.read_jpeg_image_transformer import image_hash_method
from ptext.io.read.types import Name, Dictionary, add_base_methods
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LayoutElement
from ptext.pdf.page.page import Page


class Image(LayoutElement):
    def __init__(
        self,
        image: typing.Union[str, PILImage.Image],
        width: Optional[Decimal] = None,
        height: Optional[Decimal] = None,
    ):
        if isinstance(image, str):
            image = PILImage.open(
                requests.get(
                    image,
                    stream=True,
                ).raw
            )
        super(Image, self).__init__()
        add_base_methods(image.__class__)
        setattr(image.__class__, "__hash__", image_hash_method)
        self.image: PILImage = image
        self.width = width
        self.height = height

    def _get_image_resource_name(self, image: PILImage, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)  # type: ignore [attr-defined]
        if "XObject" not in page["Resources"]:
            page["Resources"][Name("XObject")] = Dictionary()

        # insert font into resources
        image_resource_name = [
            k for k, v in page["Resources"]["XObject"].items() if v == image
        ]
        if len(image_resource_name) > 0:
            return image_resource_name[0]
        else:
            image_index = len(page["Resources"]["XObject"]) + 1
            page["Resources"]["XObject"][Name("Im%d" % image_index)] = image
            return Name("Im%d" % image_index)

    def _layout_without_padding(self, page: Page, bounding_box: Rectangle) -> Rectangle:

        # add image to resources
        image_resource_name = self._get_image_resource_name(self.image, page)

        # calculate width and height
        if self.width is None and self.height is None:
            self.width = self.image.width
            self.height = self.image.height
        else:
            if self.width is None:
                h_scale: Decimal = self.height / self.image.height
                self.width = self.image.width * h_scale
            if self.height is None:
                w_scale: Decimal = self.width / self.image.width
                self.height = self.image.height * w_scale

        # adjust width to bounding box
        if self.width > bounding_box.width:
            self.height = self.height * (bounding_box.width / self.width)
            self.width = bounding_box.width

        # adjust height to bounding box
        if self.height > bounding_box.height:
            self.width = self.width * (bounding_box.height / self.height)
            self.height = bounding_box.height

        # write Do operator
        content = " q %f 0 0 %f %f %f cm /%s Do Q " % (
            self.width,
            self.height,
            bounding_box.x,
            bounding_box.y + bounding_box.height - self.height,
            image_resource_name,
        )

        # write content
        self._append_to_content_stream(page, content)

        # return
        return Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self.height,
            self.width,
            self.height,
        )
