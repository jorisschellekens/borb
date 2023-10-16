from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddQRCode(TestCase):
    def test_add_qr_code_001(self):
        A4PortraitTemplate().add_qr_code("Lorem Ipsum").save(
            self.get_first_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_qr_code_002(self):
        A4PortraitTemplate().add_qr_code(
            "Lorem Ipsum", fill_color_as_hex="#56cbf9"
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_qr_code_003(self):
        A4PortraitTemplate().add_qr_code("Lorem Ipsum", height=200, width=200).save(
            self.get_third_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_add_qr_code_004(self):
        A4PortraitTemplate().add_qr_code("Lorem Ipsum", height=100, width=100).save(
            self.get_fourth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_add_qr_code_005(self):
        A4PortraitTemplate().add_qr_code(
            "Lorem Ipsum", stroke_color_as_hex="#56cbf9"
        ).save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
