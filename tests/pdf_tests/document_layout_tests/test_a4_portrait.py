import math
import unittest

from borb.pdf.document_layout.a4_portrait import A4Portrait
from borb.pdf.layout_element.image.avatar import Avatar
from borb.pdf.lipsum.lipsum import Lipsum


class TestA4Portrait(unittest.TestCase):

    def test_a4_portrait(self):
        (
            A4Portrait()
            # avatar
            .append_section_title(title="Avatar")
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
            .append_section_title(title="Bar Chart")
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
            .append_section_title(title="Big Number")
            .append_big_number("95%")
            .append_big_number_and_text(
                big_number="95%",
                title=Lipsum.generate_lorem_ipsum(50),
                text=Lipsum.generate_lorem_ipsum(500),
            )
            # blank
            .append_section_title(title="Blank")
            .append_blank()
            # code snippet
            .append_section_title("Code Snippet")
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
            .append_section_title("Image")
            .append_image(
                url_or_path="https://images.unsplash.com/photo-1501438400798-b40ff50396c8"
            )
            .append_image_and_text(
                path_or_url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # line chart
            .append_section_title(title="Line Chart")
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
            .append_section_title(title="Map of Europe")
            .append_map_of_europe(marked_countries=["Germany"])
            .append_map_of_europe_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                marked_countries=["Germany"],
            )
            # ordered list
            .append_section_title("Ordered List")
            .append_ordered_list(list_data=[f"List Item {i}" for i in range(0, 3)])
            .append_ordered_list_and_text(
                list_data=[f"List Item {i}" for i in range(0, 3)],
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # pie chart
            .append_section_title(title="Pie Chart")
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
            .append_section_title(title="QR Code")
            .append_qr_code(
                "https://images.unsplash.com/photo-1501438400798-b40ff50396c8"
            )
            .append_qr_code_and_text(
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
                url="https://images.unsplash.com/photo-1501438400798-b40ff50396c8",
            )
            # quote
            .append_section_title("Quote")
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
            .append_section_title(title="Single Column of Text")
            .append_single_column_of_text(
                text=Lipsum.generate_lorem_ipsum(500),
            )
            # table
            .append_section_title("Table")
            .append_table(
                tabular_data=[["Lorem", "Ipsum", "Dolor"], [10, 20, 30], [40, 50, 60]]
            )
            .append_table_and_text(
                tabular_data=[["Lorem", "Ipsum", "Dolor"], [10, 20, 30], [40, 50, 60]],
                text=Lipsum.generate_lorem_ipsum(200),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # two columns of text
            .append_section_title(title="Two Columns of Text")
            .append_two_columns_of_text(
                text_left=Lipsum.generate_lorem_ipsum(500),
                text_right=Lipsum.generate_lorem_ipsum(500),
            )
            # unordered list
            .append_section_title("Unordered List")
            .append_unordered_list(list_data=[f"List Item {i}" for i in range(0, 3)])
            .append_unordered_list_and_text(
                list_data=[f"List Item {i}" for i in range(0, 3)],
                text=Lipsum.generate_lorem_ipsum(500),
                title=Lipsum.generate_lorem_ipsum(50),
            )
            # save
            .save("assets/test_a4_portrait.pdf")
        )
