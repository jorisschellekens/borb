import math
import random


from borb.pdf import Lipsum
from borb.pdf.template.slide_template import SlideTemplate
from tests.test_case import TestCase


class TestCreateFullSlideTemplate(TestCase):
    def test_create_full_slide_template(self):
        random.seed(0)
        (
            SlideTemplate()
            .add_title_slide(
                author="Joris Schellekens",
                date="Oct. 31 2023",
                subtitle="A beautiful and simple addition to borb",
                title="SlideTemplate",
                version="2.0.19",
            )
            # bar chart
            .add_section_title_slide(
                title="Bar Chart", subtitle="Dolor Sit Amet", nr="01"
            )
            .add_barchart_and_text_slide(
                xs=[40, 60],
                labels=["Consectetur", "Nunc"],
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_barchart_slide(xs=[40, 60, 20], labels=["Consectetur", "Nunc", "Elit"])
            # big number
            .add_section_title_slide(
                title="Big number", subtitle="Dolor Sit Amet", nr="02"
            )
            .add_big_number_and_text_slide(
                big_number="95%",
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_big_number_and_text_slide(
                big_number="90%",
                title="Lorem Ipsum",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_big_number_and_text_slide(
                big_number="85%",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_big_number_and_text_slide(
                big_number="80%", text=Lipsum.generate_lipsum_text(5)
            )
            .add_big_number_slide("75%")
            # blank
            .add_section_title_slide(title="Blank", subtitle="Dolor Sit Amet", nr="03")
            .add_blank_slide()
            # image
            .add_section_title_slide(title="Image", subtitle="Dolor Sit Amet", nr="04")
            .add_image_and_text_slide(
                image_url="https://images.unsplash.com/photo-1497436072909-60f360e1d4b1",
                subtitle="Dolor Sit Amet",
                title="Lorem Ipsum",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_image_slide(
                image_url="https://images.unsplash.com/photo-1497436072909-60f360e1d4b1"
            )
            # line chart
            .add_section_title_slide(
                title="Line Chart", subtitle="Dolor Sit Amet", nr="05"
            )
            .add_linechart_and_text_slide(
                xs=[[i for i in range(0, 360)], [i for i in range(0, 360)]],
                ys=[
                    [math.sin(math.radians(i)) for i in range(0, 360)],
                    [math.cos(math.radians(i)) for i in range(0, 360)],
                ],
                labels=["sin(x)", "cos(x)"],
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_linechart_slide(
                xs=[[i for i in range(0, 360)], [i for i in range(0, 360)]],
                ys=[
                    [math.sin(math.radians(i)) for i in range(0, 360)],
                    [math.cos(math.radians(i)) for i in range(0, 360)],
                ],
                labels=["sin(x)", "cos(x)"],
            )
            # map
            .add_section_title_slide(title="Map", subtitle="Dolor Sit Amet", nr="06")
            .add_map_of_the_contiguous_united_states_and_text_slide(
                marked_states=["Texas"],
                subtitle="Dolor Sit Amet",
                title="Lorem Ipsum",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_map_of_the_contiguous_united_states_slide(marked_states=["Texas"])
            .add_map_of_the_world_and_text_slide(
                marked_countries=["Poland"],
                subtitle="Dolor Sit Amet",
                title="Lorem Ipsum",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_map_of_the_world_slide(marked_countries=["Poland"])
            # pie chart
            .add_section_title_slide(
                title="Pie Chart", subtitle="Dolor Sit Amet", nr="07"
            )
            .add_piechart_and_text_slide(
                xs=[10, 20, 30, 5],
                labels=["Lorem", "Ipsum", "Dolor", "Sit"],
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_piechart_slide(
                xs=[10, 20, 30, 5], labels=["Lorem", "Ipsum", "Dolor", "Sit"]
            )
            # quote
            .add_section_title_slide(title="Quote", subtitle="Dolor Sit Amet", nr="08")
            .add_quote_and_text_slide(
                quote_author="Robert Frost",
                quote_text="Two roads diverged in a wood, and I, I took the one less travelled by, and that has made all the difference.",
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_quote_slide(
                quote_author="Robert Frost",
                quote_text="Two roads diverged in a wood, and I, I took the one less travelled by, and that has made all the difference.",
            )
            # single column text
            .add_section_title_slide(
                title="Single Column Text", subtitle="Dolor Sit Amet", nr="09"
            )
            .add_single_column_text_slide(
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(10),
            )
            # table
            .add_section_title_slide(title="Table", subtitle="Dolor Sit Amet", nr="10")
            .add_table_and_text_slide(
                tabular_data=[
                    ["", "Lorem", "Ipsum", "Dolor"],
                    [2001, 0, 1, 20],
                    [2002, 1, 34, 34],
                ],
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
                text=Lipsum.generate_lipsum_text(5),
            )
            .add_table_slide(
                tabular_data=[
                    ["", "Lorem", "Ipsum", "Dolor"],
                    [2001, 0, 1, 20],
                    [2002, 1, 34, 34],
                ]
            )
            # two column text
            .add_section_title_slide(
                title="Two Column Text", subtitle="Dolor Sit Amet", nr="11"
            )
            .add_two_column_text_slide(
                text_left=Lipsum.generate_lipsum_text(5),
                text_right=Lipsum.generate_lipsum_text(5),
                title="Lorem Ipsum",
                subtitle="Dolor Sit Amet",
            )
            .save(self.get_first_output_file())
        )
