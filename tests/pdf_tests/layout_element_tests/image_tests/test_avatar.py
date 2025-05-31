import unittest

from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.layout_element.image.avatar import Avatar
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class TestAvatar(unittest.TestCase):

    def test_avatar(self):
        d: Document = Document()

        p: Page = Page()
        d.append_page(p)

        # useful constant(s)
        x: int = p.get_size()[0] // 10
        y: int = p.get_size()[1] // 10
        w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
        h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)

        Avatar(
            background_circle_color=X11Color.BLUE,
            clothing_type=Avatar.ClothingType.BLAZER_AND_SHIRT,
            eye_type=Avatar.EyeType.HAPPY,
            facial_hair_type=Avatar.FacialHairType.BEARD_LIGHT,
            hair_color_type=Avatar.HairColorType.BLACK,
            mouth_type=Avatar.MouthType.SERIOUS,
            top_of_head_type=Avatar.TopOfHeadType.SHORT_HAIR_THE_CAESAR,
        ).paint(
            available_space=(x, y, w, h),
            page=p,
        )

        PDF.write(what=d, where_to="assets/test_avatar.pdf")
