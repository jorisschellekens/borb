import math
import random

from borb.pdf import A4PortraitTemplate
from borb.pdf import Lipsum
from borb.pdf.template.a4_2_column_portrait_template import A42ColumnPortraitTemplate
from borb.pdf.template.slide_template import SlideTemplate
from tests.test_case import TestCase


class TestCreateFullA42ColumnPortraitTemplate(TestCase):
    def test_create_full_a4_2column_portrait_template(self):
        random.seed(0)
        (
            A42ColumnPortraitTemplate()
            .add_h1(text="Lorem Ipsum")
            # bar chart
            .add_h2("Barchart")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_barchart(
                xs=[40, 60],
                labels=["Consectetur", "Nunc"],
            )
            # blank
            .add_blank_page()
            # image
            .add_h2(text="Image")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_image(
                url_or_path="https://images.unsplash.com/photo-1497436072909-60f360e1d4b1"
            )
            # line chart
            .add_h2(text="Linechart")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_linechart(
                xs=[[i for i in range(0, 360)], [i for i in range(0, 360)]],
                ys=[
                    [math.sin(math.radians(i)) for i in range(0, 360)],
                    [math.cos(math.radians(i)) for i in range(0, 360)],
                ],
                labels=["sin(x)", "cos(x)"],
            )
            # map
            .add_h2(text="Map")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_map_of_the_contiguous_united_states(
                marked_states=["Texas"],
            )
            .add_map_of_the_world(
                marked_countries=["Poland"],
            )
            # pie chart
            .add_h2(text="Piechart")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_piechart(
                xs=[10, 20, 30, 5],
                labels=["Lorem", "Ipsum", "Dolor", "Sit"],
            )
            # quote
            .add_h2(text="Quote")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_quote(
                quote_author="Robert Frost",
                quote_text="Two roads diverged in a wood, and I, I took the one less travelled by, and that has made all the difference.",
            )
            # table
            .add_h2(text="Table")
            .add_text(Lipsum.generate_lipsum_text(3))
            .add_table(
                tabular_data=[
                    ["", "Lorem", "Ipsum", "Dolor"],
                    [2001, 0, 1, 20],
                    [2002, 1, 34, 34],
                ],
            )
            .save(self.get_first_output_file())
        )
