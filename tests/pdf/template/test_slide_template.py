import math
import random

from borb.pdf import Lipsum
from borb.pdf.template.slide_template import SlideTemplate
from tests.test_case import TestCase


class TestSlideTemplate(TestCase):
    def test_add_barchart_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_barchart_and_text_slide(
            xs=[10, 20, 30, 40],
            labels=["lorem", "ipsum", "dolor", "sit"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
            y_label="word frequency",
        ).save(self.get_first_output_file())
        self.compare_visually_to_ground_truth(self.get_first_output_file())
        self.check_pdf_using_validator(self.get_first_output_file())

    def test_add_barchart_slide(self):
        SlideTemplate().add_barchart_slide(
            xs=[10, 20, 30, 40],
            labels=["lorem", "ipsum", "dolor", "sit"],
            y_label="word frequency",
        ).save(self.get_second_output_file())
        self.compare_visually_to_ground_truth(self.get_second_output_file())
        self.check_pdf_using_validator(self.get_second_output_file())

    def test_add_big_number_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_big_number_and_text_slide(
            big_number="95%",
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_third_output_file())
        self.compare_visually_to_ground_truth(self.get_third_output_file())
        self.check_pdf_using_validator(self.get_third_output_file())

    def test_add_big_number_slide(self):
        SlideTemplate().add_big_number_slide(big_number="95%").save(
            self.get_fourth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_fourth_output_file())
        self.check_pdf_using_validator(self.get_fourth_output_file())

    def test_add_blank_slide(self):
        SlideTemplate().add_blank_slide().save(self.get_fifth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifth_output_file())
        self.check_pdf_using_validator(self.get_fifth_output_file())

    def test_add_image_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_image_and_text_slide(
            image_url="https://images.unsplash.com/photo-1439853949127-fa647821eba0",
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_sixth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixth_output_file())
        self.check_pdf_using_validator(self.get_sixth_output_file())

    def test_add_image_slide(self):
        SlideTemplate().add_image_slide(
            image_url="https://images.unsplash.com/photo-1439853949127-fa647821eba0"
        ).save(self.get_seventh_output_file())
        self.compare_visually_to_ground_truth(self.get_seventh_output_file())
        self.check_pdf_using_validator(self.get_seventh_output_file())

    def test_add_linechart_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_linechart_and_text_slide(
            xs=[[i for i in range(0, 360)]],
            ys=[[math.sin(math.radians(i)) for i in range(0, 360)]],
            labels=["sin(x)"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
            x_label="x",
            y_label="y",
        ).save(self.get_eight_output_file())
        self.compare_visually_to_ground_truth(self.get_eight_output_file())
        self.check_pdf_using_validator(self.get_eight_output_file())

    def test_add_linechart_slide(self):
        SlideTemplate().add_linechart_slide(
            xs=[[i for i in range(0, 360)]],
            ys=[[math.sin(math.radians(i)) for i in range(0, 360)]],
            labels=["sin(x)"],
            x_label="x",
            y_label="y",
        ).save(self.get_nineth_output_file())
        self.compare_visually_to_ground_truth(self.get_nineth_output_file())
        self.check_pdf_using_validator(self.get_nineth_output_file())

    def test_add_map_of_europe_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_map_of_europe_and_text_slide(
            marked_countries=["Spain"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_tenth_output_file())
        self.compare_visually_to_ground_truth(self.get_tenth_output_file())
        self.check_pdf_using_validator(self.get_tenth_output_file())

    def test_add_map_of_europe_slide(self):
        SlideTemplate().add_map_of_europe_slide(marked_countries=["Spain"]).save(
            self.get_eleventh_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_eleventh_output_file())
        self.check_pdf_using_validator(self.get_eleventh_output_file())

    def test_add_map_of_the_contiguous_united_states_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_map_of_the_contiguous_united_states_and_text_slide(
            marked_states=["Texas"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_twelfth_output_file())
        self.compare_visually_to_ground_truth(self.get_twelfth_output_file())
        self.check_pdf_using_validator(self.get_twelfth_output_file())

    def test_add_map_of_the_contiguous_united_states_slide(self):
        SlideTemplate().add_map_of_the_contiguous_united_states_slide(
            marked_states=["Texas"]
        ).save(self.get_thirteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_thirteenth_output_file())
        self.check_pdf_using_validator(self.get_thirteenth_output_file())

    def test_add_map_of_the_united_states_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_map_of_the_united_states_and_text_slide(
            marked_states=["Texas"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_fourteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_fourteenth_output_file())
        self.check_pdf_using_validator(self.get_fourteenth_output_file())

    def test_add_map_of_the_united_states_slide(self):
        SlideTemplate().add_map_of_the_united_states_slide(
            marked_states=["Texas"]
        ).save(self.get_fifteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_fifteenth_output_file())
        self.check_pdf_using_validator(self.get_fifteenth_output_file())

    def test_add_map_of_the_world_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_map_of_the_world_and_text_slide(
            marked_countries=["Spain"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_sixteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_sixteenth_output_file())
        self.check_pdf_using_validator(self.get_sixteenth_output_file())

    def test_add_map_of_the_world_slide(self):
        SlideTemplate().add_map_of_the_world_slide(marked_countries=["Spain"]).save(
            self.get_seventeenth_output_file()
        )
        self.compare_visually_to_ground_truth(self.get_seventeenth_output_file())
        self.check_pdf_using_validator(self.get_seventeenth_output_file())

    def test_add_ordered_list_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_ordered_list_and_text_slide(
            list_items=["Lorem", "Ipsum", "Dolor"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_eighteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_eighteenth_output_file())
        self.check_pdf_using_validator(self.get_eighteenth_output_file())

    def test_add_ordered_list_slide(self):
        random.seed(0)
        SlideTemplate().add_ordered_list_slide(
            list_items=[
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(1),
            ]
        ).save(self.get_nineteenth_output_file())
        self.compare_visually_to_ground_truth(self.get_nineteenth_output_file())
        self.check_pdf_using_validator(self.get_nineteenth_output_file())

    def test_add_piechart_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_piechart_and_text_slide(
            xs=[10, 20, 30, 20, 10],
            labels=["lorem", "ipsum", "dolor", "sit", "amet"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_twentieth_output_file())
        self.compare_visually_to_ground_truth(self.get_twentieth_output_file())
        self.check_pdf_using_validator(self.get_twentieth_output_file())

    def test_add_piechart_slide(self):
        SlideTemplate().add_piechart_slide(
            xs=[10, 20, 30, 20, 10], labels=["lorem", "ipsum", "dolor", "sit", "amet"]
        ).save(self.get_umpteenth_output_file(21))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(21))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(21))

    def test_add_qr_code_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_qr_code_and_text_slide(
            data="https://www.borbpdf.com/",
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(22))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(22))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(22))

    def test_add_qr_code_slide(self):
        SlideTemplate().add_qr_code_slide(data="https://www.borbpdf.com/").save(
            self.get_umpteenth_output_file(23)
        )
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(23))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(23))

    def test_add_quote_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_quote_and_text_slide(
            quote_author="Lorem Ipsum",
            quote_text=Lipsum.generate_lipsum_text(1),
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(24))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(24))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(24))

    def test_add_quote_slide(self):
        random.seed(0)
        SlideTemplate().add_quote_slide(
            quote_author="Lorem Ipsum", quote_text=Lipsum.generate_lipsum_text(2)
        ).save(self.get_umpteenth_output_file(25))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(25))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(25))

    def test_add_section_title_slide(self):
        random.seed(0)
        SlideTemplate().add_section_title_slide(
            nr="01", subtitle="Dolor Sit Amet", title="Lorem Ipsum"
        ).save(self.get_umpteenth_output_file(26))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(26))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(26))

    def test_add_single_column_text_slide(self):
        random.seed(0)
        SlideTemplate().add_single_column_text_slide(
            text=Lipsum.generate_lipsum_text(5),
            subtitle="Dolor Sit Amet",
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(27))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(27))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(27))

    def test_add_table_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_table_and_text_slide(
            tabular_data=[
                ["", "Lorem", "Ipsum"],
                [2020, "55%", "45%"],
                [2022, "40%", "60%"],
            ],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(28))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(28))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(28))

    def test_add_table_slide(self):
        SlideTemplate().add_table_slide(
            tabular_data=[
                ["", "Lorem", "Ipsum"],
                [2020, "55%", "45%"],
                [2022, "40%", "60%"],
            ]
        ).save(self.get_umpteenth_output_file(29))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(29))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(29))

    def test_add_title_slide(self):
        SlideTemplate().add_title_slide(
            author="Joris Schellekens",
            date="nov 4 2023",
            subtitle="Dolor Sit Amet",
            title="Lorem Ipsum",
            version="2.0.19",
        ).save(self.get_umpteenth_output_file(30))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(30))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(30))

    def test_add_two_column_text_slide(self):
        random.seed(0)
        SlideTemplate().add_two_column_text_slide(
            text_left=Lipsum.generate_lipsum_text(3),
            text_right=Lipsum.generate_lipsum_text(3),
            subtitle="Dolor Sit Amet",
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(31))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(31))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(31))

    def test_add_unordered_list_and_text_slide(self):
        random.seed(0)
        SlideTemplate().add_unordered_list_and_text_slide(
            list_items=["Lorem", "Ipsum", "Dolor"],
            subtitle="Dolor Sit Amet",
            text=Lipsum.generate_lipsum_text(5),
            title="Lorem Ipsum",
        ).save(self.get_umpteenth_output_file(32))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(32))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(32))

    def test_add_unordered_list_slide(self):
        random.seed(0)
        SlideTemplate().add_unordered_list_slide(
            list_items=[
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(1),
                Lipsum.generate_lipsum_text(1),
            ]
        ).save(self.get_umpteenth_output_file(33))
        self.compare_visually_to_ground_truth(self.get_umpteenth_output_file(33))
        self.check_pdf_using_validator(self.get_umpteenth_output_file(33))
