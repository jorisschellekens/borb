import random

from borb.pdf import Lipsum
from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddText(TestCase):
    def test_add_text_001(self):
        random.seed(2048)
        A4PortraitTemplate().add_text(Lipsum.generate_lipsum_text(5)).save(
            self.get_first_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_text_002(self):
        random.seed(2048)
        A4PortraitTemplate().add_text(
            Lipsum.generate_lipsum_text(5), font_color_as_hex="#56cbf9"
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_text_003(self):
        random.seed(2048)
        A4PortraitTemplate().add_text(
            Lipsum.generate_lipsum_text(5), font_family="Courier"
        ).save(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_add_text_004(self):
        random.seed(2048)
        A4PortraitTemplate().add_text(
            Lipsum.generate_lipsum_text(5), font_size=20
        ).save(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_add_text_005(self):
        random.seed(2048)
        A4PortraitTemplate().add_text(
            Lipsum.generate_lipsum_text(5), font_size=10
        ).save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
