import math
import random

from borb.pdf import A4PortraitTemplate
from borb.pdf import Lipsum
from tests.test_case import TestCase


class TestA4PortraitTemplate(TestCase):
    def test_add_barchart(self):
        A4PortraitTemplate().add_barchart(
            xs=[10, 20, 30, 40],
            labels=["lorem", "ipsum", "dolor", "sit"],
            y_label="word frequency",
        ).save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_h1(self):
        random.seed(0)
        A4PortraitTemplate().add_h1(Lipsum.generate_lipsum_text(1)).save(
            self.get_second_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_h2(self):
        random.seed(0)
        A4PortraitTemplate().add_h2(Lipsum.generate_lipsum_text(1)).save(
            self.get_third_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_h3(self):
        random.seed(0)
        A4PortraitTemplate().add_h3(Lipsum.generate_lipsum_text(1)).save(
            self.get_fourth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_h4(self):
        random.seed(0)
        A4PortraitTemplate().add_h4(Lipsum.generate_lipsum_text(1)).save(
            self.get_fifth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_h5(self):
        random.seed(0)
        A4PortraitTemplate().add_h5(Lipsum.generate_lipsum_text(1)).save(
            self.get_sixth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_h6(self):
        random.seed(0)
        A4PortraitTemplate().add_h6(Lipsum.generate_lipsum_text(1)).save(
            self.get_seventh_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_image(self):
        A4PortraitTemplate().add_image(
            "https://images.unsplash.com/photo-1497436072909-60f360e1d4b1"
        ).save(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_linechart(self):
        A4PortraitTemplate().add_linechart(
            xs=[[i for i in range(0, 360)]],
            ys=[[math.sin(math.radians(i)) for i in range(0, 360)]],
            labels=["sin(x)"],
            x_label="x",
            y_label="y",
        ).save(self.get_nineth_output_file())
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())

    def test_add_map_of_europe(self):
        A4PortraitTemplate().add_map_of_europe(marked_countries=["Poland"]).save(
            self.get_tenth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_tenth_output_file())
        self.check_pdf_using_validator(self.get_tenth_output_file())

    def test_add_map_of_the_contiguous_united_states(self):
        A4PortraitTemplate().add_map_of_the_contiguous_united_states(
            marked_states=["Texas"]
        ).save(self.get_eleventh_output_file())
        self.compare_visually_to_ground_truth(self.get_eleventh_output_file())
        self.check_pdf_using_validator(self.get_eleventh_output_file())

    def test_add_map_of_the_united_states(self):
        A4PortraitTemplate().add_map_of_the_united_states(marked_states=["Texas"]).save(
            self.get_twelfth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_twelfth_output_file())
        self.check_pdf_using_validator(self.get_twelfth_output_file())

    def test_add_map_of_the_world(self):
        A4PortraitTemplate().add_map_of_the_world(marked_countries=["Spain"]).save(
            self.get_thirteenth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_thirteenth_output_file())
        self.check_pdf_using_validator(self.get_thirteenth_output_file())

    def test_add_ordered_list(self):
        random.seed(0)
        A4PortraitTemplate().add_ordered_list(
            [
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(2),
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(2),
                Lipsum.generate_lipsum_text(1),
            ]
        ).save(self.get_fourteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourteenth_output_file())
        self.check_pdf_using_validator(self.get_fourteenth_output_file())

    def test_add_page(self):
        A4PortraitTemplate().add_page().save(self.get_fifteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifteenth_output_file())
        self.check_pdf_using_validator(self.get_fifteenth_output_file())

    def test_add_piechart(self):
        A4PortraitTemplate().add_piechart(
            xs=[10, 20, 30, 40],
            labels=["lorem", "ipsum", "dolor", "sit"],
        ).save(self.get_sixteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixteenth_output_file())
        self.check_pdf_using_validator(self.get_sixteenth_output_file())

    def test_add_qr_code(self):
        A4PortraitTemplate().add_qr_code("https://www.borbpdf.com/").save(
            self.get_seventeenth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_seventeenth_output_file())
        self.check_pdf_using_validator(self.get_seventeenth_output_file())

    def test_add_quote(self):
        A4PortraitTemplate().add_quote(
            quote_author="Robert Frost",
            quote_text="Two roads diverged in a wood, and I, I took the one less travelled by, and that has made all the difference.",
        ).save(self.get_eighteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_eighteenth_output_file())
        self.check_pdf_using_validator(self.get_eighteenth_output_file())

    def test_add_table(self):
        A4PortraitTemplate().add_table(
            tabular_data=[
                ["", "Lorem", "Ipsum", "Dolor"],
                [2001, 0, 1, 20],
                [2002, 1, 34, 34],
            ]
        ).save(self.get_nineteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_nineteenth_output_file())
        self.check_pdf_using_validator(self.get_nineteenth_output_file())

    def test_add_text(self):
        random.seed(0)
        A4PortraitTemplate().add_text(Lipsum.generate_lipsum_text(3)).add_text(
            Lipsum.generate_lipsum_text(3)
        ).save(self.get_twentieth_output_file())
        self.compare_visually_to_ground_truth(self.get_twentieth_output_file())
        self.check_pdf_using_validator(self.get_twentieth_output_file())

    def test_add_unordered_list(self):
        random.seed(0)
        A4PortraitTemplate().add_ordered_list(
            [
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(2),
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(2),
                Lipsum.generate_lipsum_text(1),
            ]
        ).save(self.get_umpteenth_output_file(21))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(21))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(21))
