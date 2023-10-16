from borb.pdf.template.a4_portrait_template import A4PortraitTemplate
from tests.test_case import TestCase


class TestAddH1H6(TestCase):
    def test_add_h1(self):
        A4PortraitTemplate().add_h1("Lorem Ipsum").save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())

    def test_add_h2(self):
        A4PortraitTemplate().add_h2("Lorem Ipsum").save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())

    def test_add_h3(self):
        A4PortraitTemplate().add_h3("Lorem Ipsum").save(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())

    def test_add_h4(self):
        A4PortraitTemplate().add_h4("Lorem Ipsum").save(self.get_fourth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())

    def test_add_h5(self):
        A4PortraitTemplate().add_h5("Lorem Ipsum").save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())

    def test_add_h6(self):
        A4PortraitTemplate().add_h6("Lorem Ipsum").save(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())

    def test_add_h1_h6(self):
        A4PortraitTemplate().add_h1("Lorem Ipsum").add_h2("Lorem Ipsum").add_h3(
            "Lorem Ipsum"
        ).add_h4("Lorem Ipsum").add_h5("Lorem Ipsum").add_h6("Lorem Ipsum").save(
            self.get_seventh_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())

    def test_add_h1_h2_h2(self):
        A4PortraitTemplate().add_h1("Lorem Ipsum").add_h2("Lorem Ipsum").add_h2("Lorem Ipsum").add_h1("Lorem Ipsum").save(
            self.get_eight_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_eight_output_file())