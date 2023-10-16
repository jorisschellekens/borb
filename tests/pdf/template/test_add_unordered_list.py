from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddUnorderedList(TestCase):
    def test_add_unordered_list_001(self):
        A4PortraitTemplate().add_unordered_list(
            ["Lorem", "Ipsum", "Dolor", "Sit"]
        ).save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_unordered_list_002(self):
        A4PortraitTemplate().add_unordered_list(
            ["Lorem", "Ipsum", "Dolor", "Sit"], font_color_as_hex="#56cbf9"
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_unordered_list_003(self):
        A4PortraitTemplate().add_unordered_list(
            ["Lorem", "Ipsum", "Dolor", "Sit"], font_family="Courier"
        ).save(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_add_unordered_list_004(self):
        A4PortraitTemplate().add_unordered_list(
            ["Lorem", "Ipsum", "Dolor", "Sit"], font_size=20
        ).save(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_add_unordered_list_005(self):
        A4PortraitTemplate().add_unordered_list(
            ["Lorem", "Ipsum", "Dolor", "Sit"], font_size=10
        ).save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
