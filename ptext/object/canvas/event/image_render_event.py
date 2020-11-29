from decimal import Decimal

from ptext.object.canvas.color.color import RGBColor
from ptext.object.event_listener import Event


class ImageRenderEvent(Event):
    """
    This implementation of Event is triggered when an Image has been processed using a Do instruction
    """

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
        self.scaled_image = self.image.resize((self.width, self.height))

    def get_image(self) -> "PIL.Image":
        """
        Get the (source) Image
        This Image may have different dimensions than
        how it is displayed in the PDF
        """
        return self.image

    def get_scaled_image(self) -> "PIL.Image":
        """
        Get the (scaled) Image
        This Image has the same dimensions as how
        it is displayed in the PDF
        """
        return self.scaled_image

    def get_x(self) -> int:
        """
        Get the x-coordinate at which the Image is drawn
        """
        return self.x

    def get_y(self) -> int:
        """
        Get the y-coordinate at which the Image is drawn
        """
        return self.y

    def get_width(self) -> int:
        """
        Get the width of the (scaled) Image
        """
        return self.width

    def get_height(self) -> int:
        """
        Get the height of the (scaled) Image
        """
        return self.height

    def get_rgb(self, x: int, y: int) -> RGBColor:
        c = self.scaled_image.getpixel((x, y))
        if self.scaled_image.mode == "RGB":
            return RGBColor(r=Decimal(c[0]), g=Decimal(c[1]), b=Decimal(c[2]))
        if self.scaled_image.mode == "RGBA":
            return RGBColor(r=Decimal(c[0]), g=Decimal(c[1]), b=Decimal(c[2]))
        if self.scaled_image.mode == "CMYK":
            r = int((1 - c[0]) * (1 - c[3]) / 255)
            g = int((1 - c[1]) * (1 - c[3]) / 255)
            b = int((1 - c[2]) * (1 - c[0]) / 255)
            return RGBColor(r=Decimal(r), g=Decimal(g), b=Decimal(b))
