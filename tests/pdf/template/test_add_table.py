from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddTable(TestCase):
    def test_add_table_001(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]]
        ).save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_table_002(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], [0.333, 0.666, 0.999]]
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_table_003(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
            font_color_as_hex="#56cbf9",
        ).save(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_add_table_004(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
            font_family="Courier",
        ).save(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_add_table_005(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]], font_size=20
        ).save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())

    def test_add_table_006(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]], font_size=10
        ).save(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())

    def test_add_table_007(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
            use_header_column=True,
            use_header_row=False,
        ).save(self.get_seventh_output_file())
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())

    def test_add_table_008(self):
        A4PortraitTemplate().add_table(
            [["Lorem", "Ipsum", "Dolor"], ["Sit", "Amet", "Consectetur"]],
            use_header_column=True,
            use_header_row=True,
        ).save(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
