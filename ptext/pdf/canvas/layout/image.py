from PIL import Image as PILImage  # type: ignore [import]

from ptext.io.read.image.read_jpeg_image_transformer import image_hash_method
from ptext.io.read.types import Name, Dictionary, add_base_methods
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LayoutElement
from ptext.pdf.page.page import Page


class Image(LayoutElement):
    def __init__(self, image: PILImage):
        super(Image, self).__init__()
        add_base_methods(image.__class__)
        setattr(image.__class__, "__hash__", image_hash_method)
        self.image: PILImage = image

    def get_image_resource_name(self, image: PILImage, page: Page):
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

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:

        # add image to resources
        image_resource_name = self.get_image_resource_name(self.image, page)

        # write Do operator
        content = " q %f 0 0 %f %f %f cm /%s do Q " % (
            bounding_box.width,
            bounding_box.height,
            bounding_box.x,
            bounding_box.y,
            image_resource_name,
        )

        # write content
        self._append_to_content_stream(page, content)

        # return
        return bounding_box  # TODO : image may have been rescaled, this is not the actual bounding box
