#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an A4 portrait page layout for PDF documents.

The `A4Portrait` class allows users to easily add content to a PDF document
without worrying about formatting or layout details.
It automatically manages the styling, positioning, and arrangement of various content types,
enabling users to focus solely on the information they want to present.

With methods for adding tables, text, images, and other elements,
the class ensures that all content is seamlessly integrated into the A4 portrait format,
making it ideal for users who prioritize content over design complexities.
"""
import pathlib
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.document import Document
from borb.pdf.document_layout.document_layout import DocumentLayout
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.image.avatar import Avatar
from borb.pdf.layout_element.image.chart import Chart
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.image.qr_code import QRCode
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.list.unordered_list import UnorderedList
from borb.pdf.layout_element.shape.map import Map
from borb.pdf.layout_element.shape.map_of_europe import MapOfEurope
from borb.pdf.layout_element.shape.map_of_the_contiguous_united_states_of_america import (
    MapOfTheContiguousUnitedStatesOfAmerica,
)
from borb.pdf.layout_element.shape.map_of_the_united_states_of_america import (
    MapOfTheUnitedStatesOfAmerica,
)
from borb.pdf.layout_element.shape.map_of_the_world import MapOfTheWorld
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.table.table_util import TableUtil
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.code_snippet import CodeSnippet
from borb.pdf.layout_element.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout
from borb.pdf.page_layout.single_column_layout import SingleColumnLayout
from borb.pdf.visitor.pdf import PDF


class A4Portrait(DocumentLayout):
    """
    Represents an A4 portrait page layout for PDF documents.

    The `A4Portrait` class allows users to easily add content to a PDF document
    without worrying about formatting or layout details.
    It automatically manages the styling, positioning, and arrangement of various content types,
    enabling users to focus solely on the information they want to present.

    With methods for adding tables, text, images, and other elements,
    the class ensures that all content is seamlessly integrated into the A4 portrait format,
    making it ideal for users who prioritize content over design complexities.
    """

    #
    # CONSTRUCTOR
    #

    __DARK_GRAY: Color = X11Color.DARK_GRAY
    __LIGHT_GRAY: Color = X11Color.LIGHT_GRAY.lighter()
    __VERY_DARK_GRAY: Color = X11Color.DARK_GRAY.darker()
    __YELLOW_MUNSELL: Color = X11Color.YELLOW_MUNSELL

    def __init__(self):
        """
        Initialize an A4Portrait document object, representing an A4-sized portrait-oriented PDF.

        This constructor sets up the base structure for an A4 portrait document .
        """
        # create empty Document
        self.__document: Document = Document()  # type: ignore[annotation-unchecked]

        # create empty Page
        page: Page = Page()  # type: ignore[annotation-unchecked]
        self.__document.append_page(page)
        self.__column_width: int = page.get_size()[0] - 2 * (page.get_size()[0] // 10)  # type: ignore[annotation-unchecked]
        self.__column_height: int = page.get_size()[1] - 2 * (page.get_size()[1] // 10)  # type: ignore[annotation-unchecked]

        # create SingleColumnLayout
        self.__layout: PageLayout = SingleColumnLayout(page)  # type: ignore[annotation-unchecked]

        # counters (to enable 'table 232: ...')
        self._number_of_layout_elements: typing.Dict[str, int] = {}  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def __add_title_and_text(
        self, e: typing.Union[LayoutElement, str], text: str, title: str
    ):
        name: str = ""
        if isinstance(e, str):
            name = e
        else:
            name = e.__class__.__name__
            if name in ["Avatar"]:
                name = "Image"
            if name in ["FixedColumnWidthTable", "FlexibleColumnWidthTable"]:
                name = "Table"
            if name in [
                "MapOfEurope",
                "MapOfTheWorld",
                "MapOfTheContiguousUnitedStatesOfAmerica",
                "MapOfTheUnitedStatesOfAmerica",
            ]:
                name = "Map"
            if name in ["OrderedList", "UnorderedList"]:
                name = "List"
        nr: int = self._number_of_layout_elements.get(name, 0)
        self.__layout.append_layout_element(
            HeterogeneousParagraph(
                chunks=[
                    Chunk(
                        f"{name} {nr}: ",
                        font=Standard14Fonts.get("Helvetica-Bold"),
                    ),
                    Chunk(f"{title}, ", font=Standard14Fonts.get("Helvetica-Oblique")),
                    Chunk(text),
                ]
            )
        )

    def __update_counter(self, e: typing.Union[LayoutElement, str]):
        name: str = ""
        if isinstance(e, str):
            name = e
        else:
            name = e.__class__.__name__
            if name in ["Avatar"]:
                name = "Image"
            if name in ["FixedColumnWidthTable", "FlexibleColumnWidthTable"]:
                name = "Table"
            if name in [
                "MapOfEurope",
                "MapOfTheWorld",
                "MapOfTheContiguousUnitedStatesOfAmerica",
                "MapOfTheUnitedStatesOfAmerica",
            ]:
                name = "Map"
            if name in ["OrderedList", "UnorderedList"]:
                name = "List"
        self._number_of_layout_elements[name] = (
            self._number_of_layout_elements.get(name, 0) + 1
        )

    #
    # PUBLIC
    #

    def append_avatar(
        self,
        background_style_type: Avatar.BackgroundStyleType = Avatar.BackgroundStyleType.CIRCLE,
        clothing_type: Avatar.ClothingType = Avatar.ClothingType.HOODIE,
        eye_type: Avatar.EyeType = Avatar.EyeType.DEFAULT,
        eyebrow_type: Avatar.EyebrowType = Avatar.EyebrowType.DEFAULT,
        facial_hair_type: Avatar.FacialHairType = Avatar.FacialHairType.BEARD_MEDIUM,
        glasses_type: Avatar.GlassesType = Avatar.GlassesType.PRESCRIPTION_BLACK,
        hair_color_type: Avatar.HairColorType = Avatar.HairColorType.BROWN,
        mouth_type: Avatar.MouthType = Avatar.MouthType.SMILE,
        shirt_logo_type: Avatar.ShirtLogoType = Avatar.ShirtLogoType.BEAR,
        skin_color_type: Avatar.SkinColorType = Avatar.SkinColorType.LIGHT,
        top_of_head_type: Avatar.TopOfHeadType = Avatar.TopOfHeadType.SHORT_HAIR_SIDES,
    ) -> "A4Portrait":
        """
        Add a customizable avatar to the document.

        This method allows the creation of an avatar with detailed customization options,
        specifying features such as hairstyle, clothing, and accessories. Useful for adding
        a personalized graphic representation within the document.

        :param background_style_type: Style of the avatar background (e.g., circle or square).
        :param clothing_type: Clothing style for the avatar.
        :param eye_type: Type of eyes for the avatar.
        :param eyebrow_type: Eyebrow style for the avatar.
        :param facial_hair_type: Facial hair style for the avatar.
        :param glasses_type: Glasses type for the avatar.
        :param hair_color_type: Hair color for the avatar.
        :param mouth_type: Mouth style for the avatar.
        :param shirt_logo_type: Logo style on the avatar’s shirt.
        :param skin_color_type: Skin color of the avatar.
        :param top_of_head_type: Hairstyle or head accessory of the avatar.
        :return: Returns the A4Portrait instance for method chaining.
        """
        W, H = self.__column_width, self.__column_height

        # add
        image: Image = Avatar(
            background_circle_color=A4Portrait.__YELLOW_MUNSELL,
            background_style_type=background_style_type,
            clothing_type=clothing_type,
            eyebrow_type=eyebrow_type,
            eye_type=eye_type,
            facial_hair_type=facial_hair_type,
            glasses_type=glasses_type,
            hair_color_type=hair_color_type,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            margin_bottom=H // 10,
            margin_left=W // 10,
            margin_right=W // 10,
            margin_top=H // 10,
            mouth_type=mouth_type,
            shirt_logo_type=shirt_logo_type,
            size=(256, 256),
            skin_color_type=skin_color_type,
            top_of_head_type=top_of_head_type,
        )
        self.__layout.append_layout_element(image)
        self.__update_counter(image)
        return self

    def append_avatar_and_text(
        self,
        text: str,
        title: str,
        background_style_type: Avatar.BackgroundStyleType = Avatar.BackgroundStyleType.CIRCLE,
        clothing_type: Avatar.ClothingType = Avatar.ClothingType.HOODIE,
        eye_type: Avatar.EyeType = Avatar.EyeType.DEFAULT,
        eyebrow_type: Avatar.EyebrowType = Avatar.EyebrowType.DEFAULT,
        facial_hair_type: Avatar.FacialHairType = Avatar.FacialHairType.BEARD_MEDIUM,
        glasses_type: Avatar.GlassesType = Avatar.GlassesType.PRESCRIPTION_BLACK,
        hair_color_type: Avatar.HairColorType = Avatar.HairColorType.BROWN,
        mouth_type: Avatar.MouthType = Avatar.MouthType.SMILE,
        shirt_logo_type: Avatar.ShirtLogoType = Avatar.ShirtLogoType.BEAR,
        skin_color_type: Avatar.SkinColorType = Avatar.SkinColorType.LIGHT,
        top_of_head_type: Avatar.TopOfHeadType = Avatar.TopOfHeadType.SHORT_HAIR_SIDES,
    ) -> "A4Portrait":
        """
        Add a customizable avatar to the document alongside a title and descriptive text.

        This method creates an avatar with various customizable features such as hairstyle,
        clothing, and accessories, and includes a section for a title and descriptive text
        beside the avatar. Useful for adding a personalized representation with contextual
        information within the document.

        :param text: The descriptive text to accompany the avatar.
        :param title: The title displayed with the avatar.
        :param background_style_type: Style of the avatar background (e.g., circle or square).
        :param clothing_type: Clothing style for the avatar.
        :param eye_type: Eye style for the avatar.
        :param eyebrow_type: Eyebrow style for the avatar.
        :param facial_hair_type: Facial hair style for the avatar.
        :param glasses_type: Glasses type for the avatar.
        :param hair_color_type: Hair color for the avatar.
        :param mouth_type: Mouth style for the avatar.
        :param shirt_logo_type: Logo style on the avatar’s shirt.
        :param skin_color_type: Skin color of the avatar.
        :param top_of_head_type: Hairstyle or head accessory of the avatar.
        :return: Returns the A4Portrait instance for method chaining.
        """
        W, H = self.__column_width, self.__column_height

        # add
        image: Image = Avatar(
            background_circle_color=A4Portrait.__YELLOW_MUNSELL,
            background_style_type=background_style_type,
            clothing_type=clothing_type,
            eyebrow_type=eyebrow_type,
            eye_type=eye_type,
            facial_hair_type=facial_hair_type,
            glasses_type=glasses_type,
            hair_color_type=hair_color_type,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            margin_bottom=H // 10,
            margin_left=W // 10,
            margin_right=W // 10,
            margin_top=H // 10,
            mouth_type=mouth_type,
            shirt_logo_type=shirt_logo_type,
            size=(256, 256),
            skin_color_type=skin_color_type,
            top_of_head_type=top_of_head_type,
        )
        self.__layout.append_layout_element(image)
        self.__update_counter(image)
        self.__add_title_and_text(image, text, title)
        return self

    def append_barchart(
        self,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a bar chart to the A4 portrait document.

        This method renders a bar chart using the specified data and optionally
        labels the y-axis.

        :param xs: A list of float values representing the heights of the bars.
        :param ys: A list of strings representing the labels for each bar.
        :param y_label: An optional label for the y-axis.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of bars (xs) must match the number of labels (ys)."
        # fmt: on
        W, H = self.__column_width, self.__column_height

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_barchart method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(ys, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W, int(W * 0.62)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__layout.append_layout_element(chart)
        self.__update_counter(chart)
        return self

    def append_barchart_and_text(
        self,
        text: str,
        title: str,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a bar chart along with descriptive text to the A4 portrait document.

        This method inserts a bar chart into the document, using the provided data for the x and y axes.
        After the chart, it adds a caption containing the chart's title and the accompanying descriptive text.
        Optionally, a label can be added for the y-axis.

        :param text:    The descriptive text to display beneath the chart.
        :param title:   The title of the chart, displayed in the caption and chart label.
        :param xs:      A list of numerical values for the x-axis of the bar chart.
        :param ys:      A list of corresponding labels for the y-axis (categories).
        :param y_label: An optional label for the y-axis. Defaults to None if not provided.
        :return:        Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of bars (xs) must match the number of labels (ys)."
        # fmt: on
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)

        # create chart
        try:
            import matplotlib.pyplot
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_barchart_and_text method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(ys, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W2, H2),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__layout.append_layout_element(chart)
        self.__update_counter(chart)
        self.__add_title_and_text(chart, text, title)
        return self

    def append_big_number(self, big_number: str) -> "A4Portrait":
        """
        Add a prominently displayed big number to the document.

        This method allows the user to insert a large number, which can be used for emphasis,
        such as in call-outs or highlights. The number will be rendered larger than standard text.

        :param big_number: The number to be displayed prominently.
        :return: The A4Portrait instance for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        max_paragraph: typing.Optional[Paragraph] = None
        for font_size in range(64, 8, -1):
            tmp_paragraph: Paragraph = Paragraph(
                big_number,
                font_size=font_size,
                font=Standard14Fonts.get("Helvetica-Bold"),
                font_color=X11Color.YELLOW_MUNSELL,
                margin_top=12,
                margin_bottom=12,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            )
            w, h = tmp_paragraph.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_paragraph = tmp_paragraph
                break
        # fmt: off
        assert max_paragraph is not None, "Unable to fit the big number within the available space. Ensure the input is not excessively long or the layout constraints are adjusted."
        # fmt: on
        self.__layout.append_layout_element(max_paragraph)
        self.__update_counter("Number")
        return self

    def append_big_number_and_text(
        self, big_number: str, text: str, title: str
    ) -> "A4Portrait":
        """
        Add a big number with accompanying text and title to the document.

        This method allows the user to insert a prominently displayed number along with
        a descriptive text and a title. This can be useful for emphasizing key statistics
        or highlights in the document.

        :param big_number: The number to be displayed prominently.
        :param text: The descriptive text to accompany the big number.
        :param title: The title to be displayed above the big number and text.
        :return: The A4Portrait instance for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        max_paragraph: typing.Optional[Paragraph] = None
        for font_size in range(64, 8, -1):
            tmp_paragraph: Paragraph = Paragraph(
                big_number,
                font_size=font_size,
                font=Standard14Fonts.get("Helvetica-Bold"),
                font_color=X11Color.YELLOW_MUNSELL,
                margin_top=12,
                margin_bottom=12,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            )
            w, h = tmp_paragraph.get_size(available_space=(W2, H2))
            if w <= W2 and h <= H2:
                max_paragraph = tmp_paragraph
                break
        # fmt: off
        assert max_paragraph is not None, "Unable to fit the big number within the available space. Ensure the input is not excessively long or the layout constraints are adjusted."
        # fmt: on
        self.__layout.append_layout_element(max_paragraph)
        self.__update_counter("Number")
        self.__add_title_and_text("Number", text, title)
        return self

    def append_blank(self) -> "A4Portrait":
        """
        Add a blank page to the A4 portrait document.

        This method inserts a new, empty page into the document, allowing for additional content to be
        added later as needed.

        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        assert isinstance(self.__layout, SingleColumnLayout)
        self.__layout.next_page()
        self.__layout.append_layout_element(
            Paragraph(
                "This page is intentionally left blank.",
                font_color=A4Portrait.__DARK_GRAY,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
            )
        )
        self.__layout.next_page()
        return self

    def append_code_snippet(self, code: str) -> "A4Portrait":
        """
        Add a code snippet to the A4 portrait document.

        This method inserts a formatted code block into the document for better
        readability and presentation.

        :param code: A string containing the code snippet to be added.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        max_code_snippet: typing.Optional[CodeSnippet] = None
        for font_size in range(12, 8, -1):
            tmp_code_snippet = CodeSnippet(
                code=code,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=12,
            )
            w, h = tmp_code_snippet.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_code_snippet = tmp_code_snippet
                break
        # fmt: off
        assert max_code_snippet is not None, "Unable to fit the code snippet within the available space. Ensure the input is not excessively long or the layout constraints are adjusted."
        # fmt: on
        self.__layout.append_layout_element(max_code_snippet)
        self.__update_counter(max_code_snippet)
        return self

    def append_code_snippet_and_text(
        self, code: str, text: str, title: str
    ) -> "A4Portrait":
        """
        Add a code snippet along with descriptive text to the A4 portrait document.

        This method inserts a formatted code snippet into the document, followed by a caption containing
        the snippet's title and accompanying descriptive text.

        :param code: The code snippet to display in the document.
        :param text: The descriptive text to display beneath the code snippet.
        :param title: The title for the code snippet, displayed in the caption.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        max_code_snippet: typing.Optional[CodeSnippet] = None
        for font_size in range(12, 8, -1):
            tmp_code_snippet = CodeSnippet(
                code=code,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=12,
            )
            w, h = tmp_code_snippet.get_size(available_space=(W2, H2))
            if w <= W2 and h <= H2:
                max_code_snippet = tmp_code_snippet
                break
        # fmt: off
        assert max_code_snippet is not None, "Unable to fit the code snippet within the available space. Ensure the input is not excessively long or the layout constraints are adjusted."
        # fmt: on
        self.__layout.append_layout_element(max_code_snippet)
        self.__update_counter(max_code_snippet)
        self.__add_title_and_text(max_code_snippet, text, title)
        return self

    def append_image(
        self, url_or_path: typing.Union[str, pathlib.Path]
    ) -> "A4Portrait":
        """
        Add an image to the A4 portrait document.

        This method inserts an image from a specified URL or file path into the document.

        :param url_or_path: The URL or file path of the image to be added.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        img: Image = Image(
            url_or_path,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=12,
            padding_top=12,
            size=(W, int(W * 0.62)),
        )
        self.__layout.append_layout_element(img)
        self.__update_counter(img)
        return self

    def append_image_and_text(
        self,
        path_or_url: typing.Union[pathlib.Path, str],
        text: str,
        title: str,
    ) -> "A4Portrait":
        """
        Add an image along with descriptive text to the A4 portrait document.

        This method inserts an image into the document, either from a local file path or a URL.
        After the image, it adds a caption containing the image's title and accompanying descriptive text.

        :param path_or_url: The file path or URL of the image to be displayed.
        :param text: The descriptive text to display beneath the image.
        :param title: The title of the image, displayed in the caption.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        img: Image = Image(
            bytes_path_pil_image_or_url=path_or_url,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=12,
            padding_top=12,
            size=(W2, H2),
        )
        self.__layout.append_layout_element(img)
        self.__update_counter(img)
        self.__add_title_and_text(img, text, title)
        return self

    def append_line_chart(
        self,
        labels: typing.List[str],
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a line chart to the A4 portrait document.

        This method generates a line chart based on the provided data and inserts it into the document.

        :param labels: The labels for the x-axis, corresponding to the data points.
        :param xs: A list of lists containing the x-values for each line in the chart.
        :param ys: A list of lists containing the y-values for each line in the chart.
        :param x_label: An optional label for the x-axis.
        :param y_label: An optional label for the y-axis.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of x-value lists must match the number of y-value lists. Ensure the input data is structured correctly."
        assert all(len(x) == len(y) for x, y in zip(xs, ys)), "Each x-value list must have the same length as its corresponding y-value list. Verify that each line's data points align correctly."
        # fmt: on
        W, H = self.__column_width, self.__column_height

        # create chart
        try:
            import matplotlib.pyplot
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_line_chart method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W, int(W * 0.62)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__layout.append_layout_element(chart)
        self.__update_counter(chart)

        return self

    def append_line_chart_and_text(
        self,
        labels: typing.List[str],
        text: str,
        title: str,
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a line chart along with descriptive text to the A4 portrait document.

        This method inserts a line chart into the document, using the provided data for multiple series,
        and adds a caption containing the chart's title and accompanying descriptive text.
        Optionally, labels can be added for both the x-axis and y-axis.

        :param labels: A list of labels for each data series in the chart.
        :param text: The descriptive text to display beneath the line chart.
        :param title: The title of the line chart, displayed in the caption.
        :param xs: A list of lists containing x-axis values for each data series.
        :param ys: A list of lists containing y-axis values for each data series.
        :param x_label: An optional label for the x-axis.
        :param y_label: An optional label for the y-axis.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of x-value lists must match the number of y-value lists. Ensure the input data is structured correctly."
        assert all(len(x) == len(y) for x, y in zip(xs, ys)), "Each x-value list must have the same length as its corresponding y-value list. Verify that each line's data points align correctly."
        # fmt: on
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)

        # create chart
        try:
            import matplotlib.pyplot
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_line_chart_and_text method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W2, H2),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__layout.append_layout_element(chart)
        self.__update_counter(chart)
        self.__add_title_and_text(chart, text, title)

        return self

    def append_map_of_europe(
        self, marked_countries: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of Europe to the PDF document, with optional highlighted countries.

        The `add_map_of_europe` method creates a slide featuring a map of Europe.
        Optionally, specific countries can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_countries:    A list of country names (strings) to be highlighted on the map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        map: Map = MapOfEurope(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_countries:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, int(W * 0.62)))
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        return self

    def append_map_of_europe_and_text(
        self, text: str, title: str, marked_countries: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of Europe, accompanying text, and a title to the PDF document.

        The `add_map_of_europe_and_text` method creates a slide that features a map of Europe,
        with the option to highlight specific countries.
        The slide also includes descriptive text and a title,
        making it useful for presenting geographic data or emphasizing particular countries in Europe.

        :param text:                The descriptive text to be displayed alongside or below the map.
        :param title:               The title text to be prominently displayed at the top of the slide.
        :param marked_countries:    A list of country names (strings) to be highlighted on the map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        map: Map = MapOfEurope(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W2, H2))
        for c in marked_countries:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        self.__add_title_and_text(map, text, title)
        return self

    def append_map_of_the_contiguous_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of the contiguous United States to the PDF document, with optional highlighted states.

        The `add_map_of_the_contiguous_united_states` method creates a slide
        featuring a map of the contiguous United States (excluding Alaska and Hawaii).
        Optionally, specific states can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_states:   A list of state names (strings) to be highlighted on the map.
                                Default is an empty list (no states highlighted).
        :return:                Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        map: Map = MapOfTheContiguousUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_states:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, int(W * 0.62)))
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        return self

    def append_map_of_the_contiguous_united_states_and_text(
        self, text: str, title: str, marked_states: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of the contiguous United States, accompanying text, and a title to the PDF document.

        The `add_map_of_the_contiguous_united_states_and_text` method creates a slide
        that features a map of the contiguous United States (excluding Alaska and Hawaii),
        with the option to highlight specific states.
        The slide also includes descriptive text and a title,
        making it useful for presenting geographic data or focusing on specific states.

        :param text:            The descriptive text to be displayed alongside or below the map.
        :param title:           The title text to be prominently displayed at the top of the slide.
        :param marked_states:   A list of state names (strings) to be highlighted on the map.
                                Default is an empty list (no states highlighted).
        :return:                Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        map: Map = MapOfTheContiguousUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W2, H2))
        for c in marked_states:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        self.__add_title_and_text(map, text, title)
        return self

    def append_map_of_the_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of the United States to the PDF document, with optional highlighted states.

        The `add_map_of_the_united_states` method creates a slide featuring a map of the United States.
        Optionally, specific states can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_states:   A list of state names (strings) to be highlighted on the map.
                                Default is an empty list (no states highlighted).
        :return:                Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        map: Map = MapOfTheUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_states:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, int(W * 0.62)))
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        return self

    def append_map_of_the_united_states_and_text(
        self, text: str, title: str, marked_states: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a map of the United States, accompanying text, and a title to the PDF document.

        The `add_map_of_the_united_states_and_text` method creates a slide that features a map of the United States,
        with the option to highlight specific states.
        Descriptive text and a title are also included on the slide.
        This is useful for presenting geographic data or visualizing information by state.

        :param text:            The descriptive text to be displayed alongside or below the map.
        :param title:           The title text to be prominently displayed at the top of the slide.
        :param marked_states:   A list of state names (strings) to be highlighted on the map.
                                Default is an empty list (no states highlighted).
        :return:                Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        map: Map = MapOfTheUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W2, H2))
        for c in marked_states:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        self.__add_title_and_text(map, text, title)
        return self

    def append_map_of_the_world(
        self, marked_countries: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a world map to the PDF document, with optional highlighted countries.

        The `add_map_of_the_world` method creates a slide featuring a world map.
        Optionally, specific countries can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_countries:    A list of country names (strings) to be highlighted on the world map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        map: Map = MapOfTheWorld(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_countries:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, int(W * 0.62)))
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        return self

    def append_map_of_the_world_and_text(
        self, text: str, title: str, marked_countries: typing.List[str] = []
    ) -> "A4Portrait":
        """
        Add a slide with a world map, accompanying text, and a title to the PDF document.

        The `add_map_of_the_world_and_text` method creates a slide that features a world map,
        with optional highlighted countries.
        Descriptive text and a title are also included on the slide.
        This method is useful for visually presenting geographic data, highlighting specific countries,
        or adding context with textual explanation.

        :param text:                The descriptive text to be displayed alongside or below the world map.
        :param title:               The title text to be prominently displayed at the top of the slide.
        :param marked_countries:    A list of country names (strings) to be highlighted on the world map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        map: Map = MapOfTheWorld(
            stroke_color=X11Color.WHITE,
            fill_color=A4Portrait.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W2, H2))
        for c in marked_countries:
            map.set_fill_color(fill_color=A4Portrait.__YELLOW_MUNSELL, name=c)
        self.__layout.append_layout_element(map)
        self.__update_counter(map)
        self.__add_title_and_text(map, text, title)
        return self

    def append_ordered_list(self, list_data: typing.List[str]) -> "A4Portrait":
        """
        Add an ordered list to the A4 portrait document.

        This method inserts an ordered list based on the provided list of strings.

        :param list_data: A list of strings representing the items in the ordered list.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        l: OrderedList = OrderedList()
        for li in list_data:
            l.append_layout_element(Paragraph(li))
        self.__layout.append_layout_element(l)
        self.__update_counter(l)
        return self

    def append_ordered_list_and_text(
        self, list_data: typing.List[str], text: str, title: str
    ) -> "A4Portrait":
        """
        Add an ordered list and descriptive text to the A4 portrait document.

        This method inserts an ordered list (numbered) along with a caption that includes
        the title and descriptive text beneath the list.

        :param list_data: The items to include in the ordered list.
        :param text: The descriptive text to display beneath the ordered list.
        :param title: The title displayed in the caption beneath the ordered list.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        l: OrderedList = OrderedList(
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE
        )
        for li in list_data:
            l.append_layout_element(Paragraph(li))
        self.__layout.append_layout_element(l)
        self.__update_counter(l)
        self.__add_title_and_text(l, text, title)
        return self

    def append_pie_chart(
        self,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a pie chart to the A4 portrait document.

        This method generates a pie chart from the provided data and includes
        an optional label for the y-axis to enhance understanding.

        :param xs: A list of float values representing the sizes of each slice.
        :param ys: A list of strings representing the labels for each slice.
        :param y_label: An optional string for the y-axis label.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of pie chart slices (xs) must match the number of labels (ys). Ensure that each slice has a corresponding label."
        # fmt: on
        W, H = self.__column_width, self.__column_height

        # create chart
        try:
            import matplotlib.pyplot
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_pie_chart method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(xs, labels=ys)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W - 2 * (W // 10), H - 2 * (H // 10)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__update_counter(chart)
        self.__layout.append_layout_element(chart)
        return self

    def append_pie_chart_and_text(
        self,
        text: str,
        title: str,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "A4Portrait":
        """
        Add a pie chart along with descriptive text to the A4 portrait document.

        This method inserts a pie chart into the document, using the provided values (`xs`) and labels (`ys`).
        A caption containing the chart's title and accompanying descriptive text is added beneath the chart.
        Optionally, a label can be added for the y-axis.

        :param text: The descriptive text to display beneath the pie chart.
        :param title: The title of the pie chart, displayed in the caption.
        :param xs: A list of values representing the chart's data.
        :param ys: A list of labels corresponding to the values in `xs`.
        :param y_label: Optional label for the y-axis (though typically not used in pie charts).
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        # fmt: off
        assert len(xs) == len(ys), "The number of pie chart slices (xs) must match the number of labels (ys). Ensure that each slice has a corresponding label."
        # fmt: on
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)

        # create chart
        try:
            import matplotlib.pyplot
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_pie_chart_and_text method in the A4Portrait class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(xs, labels=ys)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        chart = Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W2, H2),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        )
        self.__update_counter(chart)
        self.__layout.append_layout_element(chart)
        self.__add_title_and_text(chart, text, title)
        return self

    def append_qr_code(self, url: str) -> "A4Portrait":
        """
        Add a QR code to the A4 portrait document.

        This method generates a QR code from the provided URL and inserts it into the document.

        :param url: The URL to encode in the QR code.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        qr_code: QRCode = QRCode(
            qr_code_data=url,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=12,
            padding_top=12,
            size=(100, 100),
        )
        self.__layout.append_layout_element(qr_code)
        self.__update_counter(qr_code)
        return self

    def append_qr_code_and_text(self, text: str, title: str, url: str) -> "A4Portrait":
        """
        Add a QR code and descriptive text to the A4 portrait document.

        This method generates and inserts a QR code based on the provided URL, along with a caption that includes
        the title and descriptive text beneath the QR code.

        :param text: The descriptive text to display beneath the QR code.
        :param title: The title displayed in the caption beneath the QR code.
        :param url: The URL to encode in the QR code.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        qr_code: QRCode = QRCode(
            qr_code_data=url,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=12,
            padding_top=12,
            size=(100, 100),
        )
        self.__layout.append_layout_element(qr_code)
        self.__update_counter(qr_code)
        self.__add_title_and_text(qr_code, text, title)
        return self

    def append_quote(self, author: str, quote: str) -> "A4Portrait":
        """
        Add a quote to the A4 portrait document.

        This method inserts a quote attributed to a specific author, enhancing the document's content
        with meaningful text.

        :param author: The name of the author of the quote.
        :param quote: The text of the quote to be added.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        max_table: typing.Optional[Table] = None
        for font_size in range(12, 8, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=int(font_size * 1.2),
                    padding_bottom=int(font_size * 1.2),
                    padding_left=W // 4,
                    padding_right=W // 4,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Paragraph(
                        text=quote,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        font_size=font_size,
                        font_color=A4Portrait.__DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=author,
                        text_alignment=LayoutElement.TextAlignment.RIGHT,
                        font=Standard14Fonts.get("Helvetica-Bold"),
                        font_size=(font_size - 2),
                        font_color=A4Portrait.__YELLOW_MUNSELL,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_table = tmp_table
                break
        # fmt: off
        assert max_table is not None, "Failed to fit the quote and author within the available space. Try reducing the length of the quote or ensure the document has sufficient room for this element."
        # fmt: on
        self.__layout.append_layout_element(max_table)
        self.__update_counter("Quote")
        return self

    def append_quote_and_text(
        self, author: str, quote: str, text: str, title: str
    ) -> "A4Portrait":
        """
        Add a quote along with descriptive text to the A4 portrait document.

        This method inserts a quote attributed to the specified author into the document.
        A caption containing the quote's title and accompanying descriptive text is added below the quote.

        :param author: The name of the person to whom the quote is attributed.
        :param quote: The quote text to be displayed.
        :param text: The descriptive text to display beneath the quote.
        :param title: The title of the quote, displayed in the caption.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)

        max_table: typing.Optional[Table] = None
        for font_size in range(12, 8, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=int(font_size * 1.2),
                    padding_bottom=int(font_size * 1.2),
                    padding_left=W // 4,
                    padding_right=W // 4,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Paragraph(
                        text=quote,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        font_size=font_size,
                        font_color=A4Portrait.__DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=author,
                        text_alignment=LayoutElement.TextAlignment.RIGHT,
                        font=Standard14Fonts.get("Helvetica-Bold"),
                        font_size=(font_size - 2),
                        font_color=A4Portrait.__YELLOW_MUNSELL,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=(W2, H2))
            if w <= W2 and h <= H2:
                max_table = tmp_table
                break
        # fmt: off
        assert max_table is not None, "Failed to fit the quote and author within the available space. Try reducing the length of the quote or ensure the document has sufficient room for this element."
        # fmt: on
        self.__layout.append_layout_element(max_table)
        self.__update_counter("Quote")
        self.__add_title_and_text("Quote", text, title)
        return self

    def append_section_title(self, title: str) -> "A4Portrait":
        """
        Add a section title to the document, styled prominently to differentiate from regular text.

        This method inserts a section title, typically larger and styled to act as a header,
        making it clear that a new section of content begins here.

        :param title: The section title to be added to the document.
        :return: The current instance of the A4Portrait document, allowing for method chaining.
        """
        self.__layout.append_layout_element(
            Paragraph(
                text=title,
                font=Standard14Fonts.get("Helvetica-Bold"),
                font_color=X11Color.YELLOW_MUNSELL,
                font_size=16,
            )
        )
        return self

    def append_single_column_of_text(self, text: str) -> "A4Portrait":
        """
        Add a single column of text to the A4 portrait document.

        This method inserts a paragraph of text into the document's single-column layout.
        The text is added as a new paragraph element, which will flow according to the layout's
        settings for line height, alignment, and other styling properties.

        :param text: The text content to add as a single column paragraph.
        :return: Returns the A4Portrait instance to allow for method chaining.
        """
        self.__layout.append_layout_element(Paragraph(text))
        return self

    def append_table(
        self, tabular_data: typing.List[typing.List[typing.Any]]
    ) -> "A4Portrait":
        """
        Add a table to the A4 portrait document.

        This method inserts a table into the document using the provided tabular data.

        :param tabular_data: A nested list where each inner list represents a row of the table.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        max_table: typing.Optional[Table] = None
        for font_size in range(12, 8, -1):
            tmp_table = TableUtil.from_2d_data(
                tabular_data=tabular_data,
                fixed_column_width=True,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=12,
                padding_bottom=12,
            )
            tmp_table.set_padding_on_all_cells(
                padding_top=3, padding_right=3, padding_bottom=3, padding_left=3
            )
            w, h = tmp_table.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_table = tmp_table
                break
        # fmt: off
        assert max_table is not None, "Unable to fit the table within the available space. Consider reducing the number of rows, columns, or content size in the table, or ensure the document layout provides enough room for this element."
        # fmt: on
        self.__layout.append_layout_element(max_table)
        self.__update_counter(max_table)
        return self

    def append_table_and_text(
        self, tabular_data: typing.List[typing.List[str]], text: str, title: str
    ) -> "A4Portrait":
        """
        Add a table along with descriptive text to the A4 portrait document.

        This method inserts a table into the document based on the provided tabular data.
        A caption containing the table's title and accompanying descriptive text is added below the table.

        :param tabular_data: A list of lists, where each inner list represents a row of the table.
        :param text: The descriptive text to display beneath the table.
        :param title: The title of the table, displayed in the caption.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W2: int = int(W * 1.2 * 0.62)
        H2: int = int(W2 * 0.62)
        max_table: typing.Optional[Table] = None
        for font_size in range(12, 8, -1):
            tmp_table = TableUtil.from_2d_data(
                tabular_data=tabular_data,
                fixed_column_width=False,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=12,
            )
            tmp_table.set_padding_on_all_cells(
                padding_top=3, padding_right=3, padding_bottom=3, padding_left=3
            )
            w, h = tmp_table.get_size(available_space=(W2, H2))
            if w <= W2 and h <= H2:
                max_table = tmp_table
                break
        # fmt: off
        assert max_table is not None, "Unable to fit the table within the available space. Consider reducing the number of rows, columns, or content size in the table, or ensure the document layout provides enough room for this element."
        # fmt: on
        self.__layout.append_layout_element(max_table)
        self.__update_counter(max_table)
        self.__add_title_and_text(max_table, text, title)
        return self

    def append_two_columns_of_text(
        self, text_left: str, text_right: str
    ) -> "A4Portrait":
        """
        Add two columns of text to the A4 portrait document.

        This method inserts a pair of paragraphs into the document, with the first paragraph
        positioned on the left side of the page and the second on the right. Each text block
        will appear in its own column within the page layout, allowing for a side-by-side
        comparison or complementary presentation of information.

        :param text_left: Text content to be added to the left column.
        :param text_right: Text content to be added to the right column.
        :return: Returns the A4Portrait instance to enable method chaining.
        """
        W, H = self.__column_width, self.__column_height
        W_FULL_PAGE: int = int(W * 1.2)
        self.__layout.append_layout_element(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=1)
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        text_left, text_alignment=LayoutElement.TextAlignment.JUSTIFIED
                    ),
                    padding_right=W_FULL_PAGE // 20,
                )
            )
            .append_layout_element(
                Table.TableCell(
                    Paragraph(
                        text_right, text_alignment=LayoutElement.TextAlignment.JUSTIFIED
                    ),
                    padding_left=W_FULL_PAGE // 20,
                )
            )
            .no_borders()
        )
        return self

    def append_unordered_list(self, list_data: typing.List[str]) -> "A4Portrait":
        """
        Add an unordered list to the A4 portrait document.

        This method inserts an unordered list (bulleted) into the document.

        :param list_data: The items to include in the unordered list.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        l: UnorderedList = UnorderedList()
        for li in list_data:
            l.append_layout_element(Paragraph(li))
        self.__layout.append_layout_element(l)
        self.__update_counter(l)
        return self

    def append_unordered_list_and_text(
        self, list_data: typing.List[str], text: str, title: str
    ) -> "A4Portrait":
        """
        Add an unordered list along with descriptive text to the A4 portrait document.

        This method inserts an unordered list (bulleted) into the document based on the provided list data.
        A caption containing the list's title and accompanying descriptive text is added below the list.

        :param list_data: A list of strings representing the items in the unordered list.
        :param text: The descriptive text to display beneath the unordered list.
        :param title: The title of the unordered list, displayed in the caption.
        :return: Returns the modified A4Portrait document, allowing for method chaining.
        """
        l: UnorderedList = UnorderedList(
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE
        )
        for li in list_data:
            l.append_layout_element(Paragraph(li))
        self.__layout.append_layout_element(l)
        self.__update_counter(l)
        self.__add_title_and_text(l, text, title)
        return self

    def save(self, path: str) -> "A4Portrait":
        """
        Save the A4Portrait to a specified file path.

        This method writes the current A4Portrait document to the given file path.
        The document will be saved in the PDF format. If the file already exists,
        it may be overwritten.

        :param path:    The file path where the A4Portrait will be saved.
        :return:        Self, allowing for method chaining.
        """
        PDF.write(what=self.__document, where_to=path)
        return self
