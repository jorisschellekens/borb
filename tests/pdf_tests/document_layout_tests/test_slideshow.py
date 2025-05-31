import math
import unittest

from borb.pdf.document_layout.slideshow import Slideshow
from borb.pdf.layout_element.image.avatar import Avatar
from borb.pdf.lipsum.lipsum import Lipsum


class TestSlideshow(unittest.TestCase):

    def test_slideshow(self):
        (
            Slideshow()
            .append_title(subtitle="Dolor Sit Amet", title="Lorem Ipsum")
            # avatar
            .append_section_title(subtitle="Avatar", title="1.")
            .append_avatar(
                background_style_type=Avatar.BackgroundStyleType.CIRCLE,
                clothing_type=Avatar.ClothingType.BLAZER_AND_SHIRT,
                eye_type=Avatar.EyeType.HAPPY,
                eyebrow_type=Avatar.EyebrowType.RAISED_EXCITED_NATURAL,
                facial_hair_type=Avatar.FacialHairType.BEARD_LIGHT,
                glasses_type=Avatar.GlassesType.PRESCRIPTION_BLACK,
                hair_color_type=Avatar.HairColorType.BLACK,
                mouth_type=Avatar.MouthType.SMILE,
                skin_color_type=Avatar.SkinColorType.PALE,
                top_of_head_type=Avatar.TopOfHeadType.SHORT_HAIR_SHORT_FLAT,
            )
            .append_avatar_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                background_style_type=Avatar.BackgroundStyleType.CIRCLE,
                clothing_type=Avatar.ClothingType.BLAZER_AND_SHIRT,
                eye_type=Avatar.EyeType.HAPPY,
                eyebrow_type=Avatar.EyebrowType.RAISED_EXCITED_NATURAL,
                facial_hair_type=Avatar.FacialHairType.BEARD_LIGHT,
                glasses_type=Avatar.GlassesType.PRESCRIPTION_BLACK,
                hair_color_type=Avatar.HairColorType.BLACK,
                mouth_type=Avatar.MouthType.SMILE,
                skin_color_type=Avatar.SkinColorType.PALE,
                top_of_head_type=Avatar.TopOfHeadType.SHORT_HAIR_SHORT_FLAT,
            )
            # bar chart
            .append_section_title(subtitle="Bar Chart", title="2.")
            .append_barchart(
                xs=[20, 30, 40], ys=["Lorem", "Ipsum", "Dolor"], y_label="Fruit"
            )
            .append_barchart_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                xs=[20.0, 30, 40],
                ys=["Lorem", "Ipsum", "Dolor"],
                y_label="Fruit",
            )
            # big number
            .append_section_title(subtitle="Big Number", title="3.")
            .append_big_number("95%")
            .append_big_number_and_text(
                big_number="95%",
                title=Lipsum.generate_lorem_ipsum(50),
                text=Lipsum.generate_lorem_ipsum(500),
            )
            # blank
            .append_section_title(subtitle="Blank", title="4.")
            .append_blank()
            # code snippet
            .append_section_title(subtitle="Code Snippet", title="5.")
            .append_code_snippet(
                code="""
            def fib(n: int) -> int:
                if n == 0 or n == 1:
                    return 1
                else:
                    return fib(n-1) + fib(n-2)
            """
            )
            .append_code_snippet_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                code="""
        def fib(n: int) -> int:
            if n == 0 or n == 1:
                return 1
            else:
                return fib(n-1) + fib(n-2)
        """,
            )
            # image
            .append_section_title(subtitle="Image", title="6.")
            .append_image(
                "https://images.unsplash.com/photo-1501438400798-b40ff50396c8"
            )
            .append_image_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                path_or_url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
            )
            # line chart
            .append_section_title(subtitle="Line Chart", title="7.")
            .append_line_chart(
                xs=[[i for i in range(0, 360)]],
                ys=[[math.sin(math.radians(i)) for i in range(0, 360)]],
                labels=["sin(x)"],
            )
            .append_line_chart_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                xs=[[i for i in range(0, 360)]],
                ys=[[math.sin(math.radians(i)) for i in range(0, 360)]],
                labels=["sin(x)"],
            )
            # map
            .append_section_title(subtitle="Map of Europe", title="9. ")
            .append_map_of_europe(marked_countries=["Germany"])
            .append_map_of_europe_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                marked_countries=["Germany"],
            )
            # ordered list
            .append_section_title(subtitle="Ordered List", title="8.")
            .append_ordered_list(list_data=[f"List Item {i}" for i in range(0, 3)])
            .append_ordered_list_and_text(
                list_data=[f"List Item {i}" for i in range(0, 3)],
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # pie chart
            .append_section_title(subtitle="Pie Chart", title="9.")
            .append_pie_chart(
                xs=[20.0, 30, 40], ys=["Lorem", "Ipsum", "Dolor"], y_label="Fruit"
            )
            .append_pie_chart_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                xs=[20.0, 30, 40],
                ys=["Lorem", "Ipsum", "Dolor"],
                y_label="Fruit",
            )
            # QR code
            .append_section_title(subtitle="QR Code", title="10.")
            .append_qr_code(
                "https://images.unsplash.com/photo-1501438400798-b40ff50396c8"
            )
            .append_qr_code_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
            )
            # quote
            .append_section_title(subtitle="Quote", title="11.")
            .append_quote(
                quote=Lipsum.generate_lorem_ipsum(100),
                author=Lipsum.generate_lorem_ipsum(32),
            )
            .append_quote_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                quote=Lipsum.generate_lorem_ipsum(100),
                author=Lipsum.generate_lorem_ipsum(32),
            )
            # single column of text
            .append_section_title(subtitle="Single Column of Text", title="12.")
            .append_single_column_of_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # table
            .append_section_title(subtitle="Table", title="13.")
            .append_table(
                tabular_data=[["Lorem", "Ipsum", "Dolor"], [10, 20, 30], [40, 50, 60]]
            )
            # two columns of text
            .append_section_title(subtitle="Two Columns of Text", title="14.")
            .append_two_columns_of_text(
                title=Lipsum.generate_lorem_ipsum(50),
                text_left=Lipsum.generate_lorem_ipsum(500),
                text_right=Lipsum.generate_lorem_ipsum(500),
            )
            # unordered list
            .append_section_title(subtitle="Unordered List", title="15.")
            .append_unordered_list(list_data=[f"List Item {i}" for i in range(0, 3)])
            .append_unordered_list_and_text(
                list_data=[f"List Item {i}" for i in range(0, 3)],
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            .save("assets/test_slideshow.pdf")
        )
