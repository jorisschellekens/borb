from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddImage(TestCase):
    def test_add_image_001(self):
        A4PortraitTemplate().add_image(
            "https://images.unsplash.com/photo-1654110464626-e855725b4467",
            width=528 // 2,
            height=300 // 2,
        ).save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_image_002(self):
        A4PortraitTemplate().add_image(
            "https://images.unsplash.com/photo-1654110464626-e855725b4467",
            width=528 // 3,
            height=300 // 3,
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())
