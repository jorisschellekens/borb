#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the highest level of abstraction in the PDF library.

The `Slideshow` class allows users to create a PDF document resembling a
slideshow without concerning themselves with formatting details. Users are
only required to provide content, while the class handles layout and
presentation.

It includes methods for easily creating slides tailored to specific content
types, such as slides featuring charts, text, tables, and more.
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
from borb.pdf.layout_element.shape.map_of_europe import MapOfEurope
from borb.pdf.layout_element.shape.map_of_the_contiguous_united_states_of_america import (
    MapOfTheContiguousUnitedStatesOfAmerica,
)
from borb.pdf.layout_element.shape.map_of_the_united_states_of_america import (
    MapOfTheUnitedStatesOfAmerica,
)
from borb.pdf.layout_element.shape.map_of_the_world import MapOfTheWorld
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.table.table_util import TableUtil
from borb.pdf.layout_element.text.code_snippet import CodeSnippet
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.visitor.pdf import PDF


class Slideshow(DocumentLayout):
    """
    Represents the highest level of abstraction in the PDF library.

    The `Slideshow` class allows users to create a PDF document resembling a
    slideshow without concerning themselves with formatting details. Users are
    only required to provide content, while the class handles layout and
    presentation.

    It includes methods for easily creating slides tailored to specific content
    types, such as slides featuring charts, text, tables, and more.
    """

    __DARK_GRAY: Color = X11Color.DARK_GRAY
    __LIGHT_GRAY: Color = X11Color.LIGHT_GRAY.lighter()
    __VERY_DARK_GRAY: Color = X11Color.DARK_GRAY.darker()
    __YELLOW_MUNSELL: Color = X11Color.YELLOW_MUNSELL
    __SECTION_TITLE_IMAGES: typing.List[str] = [
        "https://images.unsplash.com/photo-1512850842-7b9619f6c143",
        "https://images.unsplash.com/photo-1542753172-bcd7253a78a1",
        "https://images.unsplash.com/photo-1551041181-cacd7047d18d",
        "https://images.unsplash.com/photo-1555859623-1caf19ff9bbb",
        "https://images.unsplash.com/photo-1561700398-b25aeb4454fc",
        "https://images.unsplash.com/photo-1439337153520-7082a56a81f4",
        "https://images.unsplash.com/photo-1460551882935-745bdcaf8009",
        "https://images.unsplash.com/photo-1476891626313-2cecb3820a69",
        "https://images.unsplash.com/photo-1490004531003-9bda21d243db",
        "https://images.unsplash.com/photo-1495745713439-7efd16a9555c",
        "https://images.unsplash.com/photo-1504019853082-9a4cb128c1ef",
        "https://images.unsplash.com/photo-1521035227181-90af4feddc6c",
        "https://images.unsplash.com/photo-1524230572899-a752b3835840",
        "https://images.unsplash.com/photo-1527576539890-dfa815648363",
        "https://images.unsplash.com/photo-1527698334848-f475f9d99449",
        "https://images.unsplash.com/photo-1532374281774-97f9514fcfea",
        "https://images.unsplash.com/photo-1568194143771-9be23c309f28",
        "https://images.unsplash.com/photo-1574492956703-638af28b0065",
        "https://images.unsplash.com/photo-1582140161604-0b909c97653c",
        "https://images.unsplash.com/photo-1622465791213-ceb53325aa9f",
    ]

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the Slideshow object with a specified theme for content generation.

        The `Slideshow` class provides a high-level interface for creating presentations
        by allowing users to focus solely on the content without needing to manage style or layout options.
        This constructor initializes the slideshow with a default document structure
        and applies a theme that defines the color scheme for the slides.
        If a custom theme is provided, it overrides the default colors where specified.
        The flexibility of this class makes it easy to generate visually coherent presentations
        while minimizing the complexity involved in layout management.

        """
        self.__document: Document = Document()  # type: ignore[annotation-unchecked]
        self.__page: typing.Optional[Page] = None  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    def __empty_slide(self) -> None:
        self.__page = Page(width_in_points=950, height_in_points=540)
        self.__document.append_page(page=self.__page)

    def __slide_with_text(self, text: str, title: str) -> None:
        self.__empty_slide()

        # Color half the page
        assert self.__page is not None
        W, H = self.__page.get_size()
        Shape(
            coordinates=[
                (0.0, 0.0),
                (0, H),
                (W // 2, H),
                (W // 2, 0),
                (0, 0),
            ],
            stroke_color=Slideshow.__LIGHT_GRAY,
            fill_color=Slideshow.__LIGHT_GRAY,
        ).paint(
            available_space=(
                W // 2,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )

        # Attempt to fit a Table with title and text
        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=H // 10,
                    padding_bottom=H // 10,
                    padding_right=W // 20,
                    padding_left=W // 20,
                )
                .append_layout_element(
                    Paragraph(
                        text=title,
                        font_size=font_size + 2,
                        font_color=Slideshow.__VERY_DARK_GRAY,
                        font=Standard14Fonts.get("Helvetica-Bold"),
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=text,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                    )
                )
            ).no_borders()
            w, h = tmp_table.get_size(
                available_space=(
                    W // 2,
                    H,
                )
            )
            if w <= W // 2 and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                W // 2,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
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
    ) -> "Slideshow":
        """
        Add a customizable cartoon avatar to the slideshow.

        This method allows users to insert a cartoon-style avatar into a PDF slideshow.
        The avatar can be personalized through a variety of attributes, including clothing,
        hair color, facial features, and accessories.
        Users can choose from different predefined options for each attribute to represent a unique avatar.
        The avatar can be placed on a background with various styles such as a circle or transparent background.
        After customization, the avatar is added as an element to the slideshow.
        This method returns the slideshow instance to allow for method chaining,
        enabling the user to continue adding other elements.

        :param background_style_type: The style of the avatar's background (e.g., circle, transparent). Defaults to CIRCLE.
        :param clothing_type: The type of clothing the avatar wears (e.g., hoodie, t-shirt). Defaults to HOODIE.
        :param eyebrow_type: The style of the avatar's eyebrows (e.g., default, thick). Defaults to DEFAULT.
        :param eye_type: The style of the avatar's eyes (e.g., default, squint). Defaults to DEFAULT.
        :param facial_hair_type: The type of facial hair (e.g., beard, clean-shaven). Defaults to BEARD_MEDIUM.
        :param glasses_type: The type of glasses worn by the avatar (e.g., prescription, sunglasses). Defaults to PRESCRIPTION_BLACK.
        :param hair_color_type: The color of the avatar's hair (e.g., brown, blond). Defaults to BROWN.
        :param mouth_type: The expression of the avatar's mouth (e.g., smile, frown). Defaults to SMILE.
        :param shirt_logo_type: The logo displayed on the avatar's shirt (e.g., bear, skull). Defaults to BEAR.
        :param skin_color_type: The skin color of the avatar (e.g., light, dark). Defaults to LIGHT.
        :param top_of_head_type: The style of the avatar's hair or headwear (e.g., short hair, hat). Defaults to SHORT_HAIR_SIDES.
        :return: Returns the slideshow instance with the avatar added, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        # add
        Avatar(
            background_circle_color=Slideshow.__YELLOW_MUNSELL,
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
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
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
    ) -> "Slideshow":
        """
        Add a customizable avatar and accompanying text to the slideshow.

        This method creates an avatar with customizable appearance options and places it
        alongside a title and body text in the slideshow. Each attribute parameter allows
        specification of details like facial features, clothing style, and accessories to
        personalize the avatar.

        :param text: The body text to display alongside the avatar.
        :param title: Title text to display above or near the avatar.
        :param background_style_type: Style of the avatar background (e.g., circle, square).
        :param clothing_type: Type of clothing the avatar wears.
        :param eye_type: Style of the avatar’s eyes.
        :param eyebrow_type: Style of the avatar’s eyebrows.
        :param facial_hair_type: Type of facial hair for the avatar.
        :param glasses_type: Style of glasses for the avatar.
        :param hair_color_type: Color of the avatar’s hair.
        :param mouth_type: Style of the avatar’s mouth.
        :param shirt_logo_type: Style of logo on the avatar’s shirt.
        :param skin_color_type: Skin color of the avatar.
        :param top_of_head_type: Hair or head style of the avatar.
        :return: Returns the Slideshow instance for method chaining.
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        Avatar(
            background_circle_color=Slideshow.__YELLOW_MUNSELL,
            background_style_type=background_style_type,
            clothing_type=clothing_type,
            eyebrow_type=eyebrow_type,
            eye_type=eye_type,
            facial_hair_type=facial_hair_type,
            glasses_type=glasses_type,
            hair_color_type=hair_color_type,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            margin_bottom=H // 10,
            margin_left=W // 20,
            margin_right=W // 20,
            margin_top=H // 10,
            mouth_type=mouth_type,
            shirt_logo_type=shirt_logo_type,
            size=(256, 256),
            skin_color_type=skin_color_type,
            top_of_head_type=top_of_head_type,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_barchart(
        self,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "Slideshow":
        """
        Add a bar chart to the PDF document.

        The `add_barchart` method inserts a bar chart into the document,
        using the provided data values and labels.
        This is useful for visualizing categorical data and comparing different values across categories.

        :param xs:      A list of numerical values representing the heights of the bars in the chart.
        :param ys:      A list of labels corresponding to each bar in the chart.
        :param y_label: A descriptive label for the y-axis of the bar chart.
        :return:        Self, allowing for method chaining
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_barchart method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(ys, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W - 2 * (W // 10), H - 2 * (H // 10)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_barchart_and_text(
        self,
        text: str,
        title: str,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "Slideshow":
        """
        Add a slide with a bar chart, accompanying text, and a title to the PDF document.

        The `add_barchart_and_text` method creates a slide that includes a bar chart, descriptive text, and a title.
        The bar chart is generated from the provided data values and labels,
        while the text can be used to explain or provide context for the chart.

        :param text:    The descriptive text to be displayed alongside the bar chart.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :param xs:      A list of numerical values representing the heights of the bars in the chart.
        :param ys:      A list of labels corresponding to each bar in the chart.
        :param y_label: A descriptive label for the y-axis of the bar chart.
        :return:        Self, allowing for method chaining
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_barchart_and_text method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.bar(ys, xs)
        if y_label is not None:
            ax.set_ylabel(y_label)

        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W // 2 - 2 * (W // 20), H - 2 * (H // 10)),
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_big_number(self, big_number: str) -> "Slideshow":
        """
        Add a slide containing a prominently displayed big number.

        This method creates a new slide with a single large number centered on it.
        This is useful for emphasizing a key statistic or figure that needs to capture
        the audience's attention.

        :param big_number:  The number to be displayed on the slide.
        :return:            Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        max_paragraph: typing.Optional[Paragraph] = None
        for font_size in range(128, 12, -1):
            tmp_paragraph = Paragraph(
                text=big_number,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                font_color=Slideshow.__VERY_DARK_GRAY,
                padding_left=W // 10,
                padding_right=W // 10,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            w, h = tmp_paragraph.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_paragraph = tmp_paragraph
                break
        assert max_paragraph is not None
        max_paragraph.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_big_number_and_text(
        self, big_number: str, text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with a large number, accompanying text, and a title to the PDF document.

        The `add_big_number_and_text` method creates a slide that prominently displays a large number,
        which is typically used to highlight key metrics or statistics.
        The slide also includes a block of descriptive text and a title to provide context or explanation for the number.

        :param big_number:  A string representing the large number to be prominently displayed on the slide.
        :param text:        The descriptive text to be displayed below or alongside the big number.
        :param title:       The title text to be prominently displayed at the top of the slide.
        :return:            Self, allowing for method chaining.
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()

        max_paragraph: typing.Optional[Paragraph] = None
        for font_size in range(64, 12, -1):
            tmp_paragraph = Paragraph(
                text=big_number,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                font_color=Slideshow.__VERY_DARK_GRAY,
                padding_left=W // 20,
                padding_right=W // 20,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            w, h = tmp_paragraph.get_size(available_space=(W // 2, H))
            if w <= W and h <= H:
                max_paragraph = tmp_paragraph
                break
        assert max_paragraph is not None
        max_paragraph.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_blank(self) -> "Slideshow":
        """
        Add a purposefully blank slide to the slideshow.

        This method creates a slide that intentionally contains no content. It
        can be used to signify a transition or a pause in the presentation,
        allowing the audience to focus on the previous content or prepare for
        what comes next.

        :return: Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        Paragraph(
            "This slide intentionally left blank.",
            padding_top=10,
            padding_bottom=10,
            padding_right=10,
            padding_left=10,
            font_color=Slideshow.__DARK_GRAY,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.BOTTOM,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_code_snippet(self, code: str) -> "Slideshow":
        """
        Add a slide with a code snippet to the PDF document.

        The `add_code_snippet` method creates a slide that displays a snippet of code.
        This is useful for presentations that include programming examples,
        syntax highlighting, or technical demonstrations.
        The code is presented in a readable, formatted style on the slide.

        :param code:    The code string to be displayed in the code snippet.
        :return:        Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_code_snippet: typing.Optional[CodeSnippet] = None
        for font_size in range(32, 10, -1):
            tmp_code_snippet = CodeSnippet(
                code=code,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=H // 10,
                padding_bottom=H // 10,
                padding_right=W // 10,
                padding_left=W // 10,
            )
            w, h = tmp_code_snippet.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_code_snippet = tmp_code_snippet
                break
        assert max_code_snippet is not None
        max_code_snippet.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_code_snippet_and_text(
        self, code: str, text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with a code snippet, accompanying text, and a title to the PDF document.

        The `add_code_snippet_and_text` method creates a slide that features
        a snippet of code along with descriptive text and a title.
        This is useful for presenting programming examples or technical content in a clear and organized manner,
        allowing the audience to understand the context of the code being shown.

        :param code:    The code string to be displayed in the code snippet.
        :param text:    The descriptive text to be displayed alongside or below the code snippet.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :return:        Self, allowing for method chaining.
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_code_snippet: typing.Optional[CodeSnippet] = None
        for font_size in range(32, 10, -1):
            tmp_code_snippet = CodeSnippet(
                code=code,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                padding_top=H // 10,
                padding_bottom=H // 10,
                padding_right=W // 20,
                padding_left=W // 20,
            )
            w, h = tmp_code_snippet.get_size(available_space=(W // 2, H))
            if w <= (W // 2) and h <= H:
                max_code_snippet = tmp_code_snippet
                break
        assert max_code_snippet is not None
        max_code_snippet.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_image(self, url_or_path: typing.Union[str, pathlib.Path]) -> "Slideshow":
        """
        Add an image to the slideshow.

        This method allows users to include an image in the current slide.
        The image can be specified either by a URL or a local file path.
        Once added, the image will be included in the slideshow presentation.

        :param url_or_path: The URL or local file path of the image to be added.
        :return:            Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        Image(
            bytes_path_pil_image_or_url=url_or_path,
            size=(W, H),
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_image_and_text(
        self,
        path_or_url: typing.Union[pathlib.Path, str],
        text: str,
        title: str,
    ) -> "Slideshow":
        """
        Add a slide that includes an image along with a title and descriptive text.

        This method creates a new slide featuring the specified image, which can be
        provided as a file path or a URL. The slide will also display a title and
        accompanying text, allowing for the presentation of visual content alongside
        relevant information.

        :param path_or_url: The file path or URL of the image to be displayed on the slide.
        :param text:        The descriptive text to accompany the image.
        :param title:       The title associated with the slide.
        :return:            Self, allowing for method chaining.
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        Image(
            bytes_path_pil_image_or_url=path_or_url,
            size=(W // 2 - 2 * (W // 20), H - 2 * (H // 10)),
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_line_chart(
        self,
        labels: typing.List[str],
        xs: typing.List[typing.List[float]],
        ys: typing.List[typing.List[float]],
        x_label: typing.Optional[str] = None,
        y_label: typing.Optional[str] = None,
    ) -> "Slideshow":
        """
        Add a line chart to the PDF document.

        The `add_linechart` method inserts a line chart into the document using the provided data series and labels.
        Multiple data series can be included, each with its own label.
        Optional axis labels can also be provided for further clarity.

        :param xs:          A list of lists where each sublist contains x-values (e.g., time or categories) for the corresponding data series.
        :param ys:          A list of lists where each sublist contains y-values (e.g., data points) for the corresponding data series.
        :param labels:      A list of strings representing the labels for each data series.
        :param x_label:     Optional. A label for the x-axis of the line chart.
        :param y_label:     Optional. A label for the y-axis of the line chart.
        :return:            Self, allowing for method chaining
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_line_chart method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add
        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W - 2 * (W // 10), H - 2 * (H // 10)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
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
    ) -> "Slideshow":
        """
        Add a slide with a line chart, accompanying text, and a title to the PDF document.

        The `add_line_chart_and_text` method creates a slide that includes a line chart with multiple data series,
        a block of descriptive text, and a title.
        The chart is generated using the provided x-values, y-values, and series labels,
        while optional axis labels can be specified to clarify the chart's axes.

        :param text:    The descriptive text to be displayed alongside the line chart.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :param xs:      A list of lists where each sublist contains x-values for the corresponding data series.
        :param ys:      A list of lists where each sublist contains y-values for the corresponding data series.
        :param labels:  A list of strings representing the labels for each data series.
        :param x_label: Optional. A label for the x-axis of the line chart.
        :param y_label: Optional. A label for the y-axis of the line chart.
        :return:        Self, allowing for method chaining
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_line_chart_and_text method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots(layout="constrained")
        ax.set(xlabel=x_label or "", ylabel=y_label or "", title="")
        for x, y, label in zip(xs, ys, labels):
            ax.plot(x, y, label=label)
        fig.legend(loc="outside lower center")

        # add
        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W // 2 - 2 * (W // 20), H - 2 * (H // 10)),
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_europe(
        self, marked_countries: typing.List[str] = []
    ) -> "Slideshow":
        """
        Add a slide with a map of Europe to the PDF document, with optional highlighted countries.

        The `add_map_of_europe` method creates a slide featuring a map of Europe.
        Optionally, specific countries can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_countries:    A list of country names (strings) to be highlighted on the map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        map: MapOfEurope = MapOfEurope(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_countries:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, H)).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_europe_and_text(
        self, text: str, title: str, marked_countries: typing.List[str] = []
    ) -> "Slideshow":
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
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        map = MapOfEurope(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W // 2, H))
        for c in marked_countries:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_contiguous_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "Slideshow":
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
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        map = MapOfTheContiguousUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_states:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, H)).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_contiguous_united_states_and_text(
        self, text: str, title: str, marked_states: typing.List[str] = []
    ) -> "Slideshow":
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
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        map = MapOfTheContiguousUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W // 2, H))
        for c in marked_states:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_united_states(
        self, marked_states: typing.List[str] = []
    ) -> "Slideshow":
        """
        Add a slide with a map of the United States to the PDF document, with optional highlighted states.

        The `add_map_of_the_united_states` method creates a slide featuring a map of the United States.
        Optionally, specific states can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_states:   A list of state names (strings) to be highlighted on the map.
                                Default is an empty list (no states highlighted).
        :return:                Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        map: MapOfTheUnitedStatesOfAmerica = MapOfTheUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_states:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, H)).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_united_states_and_text(
        self, text: str, title: str, marked_states: typing.List[str] = []
    ) -> "Slideshow":
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
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        map = MapOfTheUnitedStatesOfAmerica(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W // 2, H))
        for c in marked_states:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_world(
        self, marked_countries: typing.List[str] = []
    ) -> "Slideshow":
        """
        Add a slide with a world map to the PDF document, with optional highlighted countries.

        The `add_map_of_the_world` method creates a slide featuring a world map.
        Optionally, specific countries can be highlighted to emphasize geographic data or focus on certain regions.
        This slide does not include additional text or titles.

        :param marked_countries:    A list of country names (strings) to be highlighted on the world map.
                                    Default is an empty list (no countries highlighted).
        :return:                    Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        map: MapOfTheWorld = MapOfTheWorld(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 10,
            padding_left=W // 10,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        for c in marked_countries:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.scale_to_fit(size=(W, H)).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_map_of_the_world_and_text(
        self, text: str, title: str, marked_countries: typing.List[str] = []
    ) -> "Slideshow":
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
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        map = MapOfTheWorld(
            stroke_color=X11Color.WHITE,
            fill_color=Slideshow.__LIGHT_GRAY,
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
            line_width=0.1,  # type: ignore[arg-type]
        )
        map.scale_to_fit(size=(W // 2, H))
        for c in marked_countries:
            map.set_fill_color(fill_color=Slideshow.__YELLOW_MUNSELL, name=c)
        map.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_ordered_list(self, list_data: typing.List[str]) -> "Slideshow":
        """
        Add a slide containing an ordered list based on the provided list data.

        This method creates a new slide that presents a sequence of items in a
        structured ordered list format. The list is generated from the provided
        list of strings, where each string represents an item in the list.
        This format helps to clearly convey a ranked or sequential order of information.

        :param list_data:   A list of strings containing the items to be displayed
                            in the ordered list.
        :return:            Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_list: typing.Optional[OrderedList] = None
        for font_size in range(64, 12, -1):
            tmp_list = OrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                padding_left=W // 10,
                padding_right=W // 10,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            for li in list_data:
                tmp_list.append_layout_element(
                    Paragraph(
                        text=li,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
            w, h = tmp_list.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_list = tmp_list
                break
        assert max_list is not None
        max_list.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_ordered_list_and_text(
        self, list_data: typing.List[str], text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with an ordered list, accompanying text, and a title to the PDF document.

        The `add_ordered_list_and_text` method creates a slide that includes an ordered list (numbered list)
        based on the provided list of items.
        It also features descriptive text and a title at the top of the slide.
        This method is ideal for presenting a sequence of steps or ranked items along with explanatory text.

        :param list_data:   A list of strings representing the items in the ordered (numbered) list.
        :param text:        The descriptive text to be displayed alongside or below the ordered list.
        :param title:       The title text to be prominently displayed at the top of the slide.
        :return:            Self, allowing for method chaining
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()

        max_list: typing.Optional[OrderedList] = None
        for font_size in range(64, 12, -1):
            tmp_list = OrderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                padding_left=W // 20,
                padding_right=W // 20,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            for li in list_data:
                tmp_list.append_layout_element(
                    Paragraph(
                        text=li,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
            w, h = tmp_list.get_size(available_space=(W // 2, H))
            if w <= W and h <= H:
                max_list = tmp_list
                break
        assert max_list is not None
        max_list.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_pie_chart(
        self,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "Slideshow":
        """
        Add a pie chart to the PDF document.

        The `add_pie_chart` method allows users to easily incorporate a pie chart into the PDF.
        Users provide the data values and corresponding labels, and the method takes care of
        generating the chart in the appropriate format and layout.

        :param xs:      A list of numerical values representing the segments of the pie chart.
        :param ys:      A list of labels corresponding to each segment in the pie chart.
        :param y_label: A descriptive label for the pie chart, which will be displayed prominently.
        :return:        Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_pie_chart method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(xs, labels=ys)
        if y_label is not None:
            ax.set_ylabel(y_label)

        # add
        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W - 2 * (W // 10), H - 2 * (H // 10)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_pie_chart_and_text(
        self,
        text: str,
        title: str,
        xs: typing.List[float],
        ys: typing.List[str],
        y_label: typing.Optional[str] = None,
    ) -> "Slideshow":
        """
        Add a slide with a pie chart, accompanying text, and a title to the PDF document.

        The `add_pie_chart_and_text` method creates a slide featuring a pie chart along with a block of descriptive text.
        The pie chart is generated from the provided data values and labels,
        and the text can be used to explain or elaborate on the chart.

        :param text:    The descriptive text to be displayed alongside the pie chart.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :param xs:      A list of numerical values representing the segments of the pie chart.
        :param ys:      A list of labels corresponding to each segment in the pie chart.
        :param y_label: A descriptive label for the pie chart, which will be displayed on the slide.
        :return:        Self, allowing for method chaining.
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        # create chart
        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the add_pie_chart_and_text method in the Slideshow class. "
                "You can install it with 'pip install matplotlib'."
            )

        fig, ax = matplotlib.pyplot.subplots()
        ax.pie(xs, labels=ys)
        if y_label is not None:
            ax.set_ylabel(y_label)

        Chart(
            matplotlib_plt=matplotlib.pyplot,
            size=(W // 2 - 2 * (W // 20), H - 2 * (H // 10)),
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_qr_code(self, url: str) -> "Slideshow":
        """
        Add a slide containing a QR code linked to a specified URL.

        This method generates a QR code that encodes the provided URL and places it
        on a new slide. This allows the audience to easily scan the QR code with their
        devices to access the linked content.

        :param url: The URL to be encoded in the QR code.
        :return:    Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()

        QRCode(
            qr_code_data=url,
            qr_code_type=QRCode.QRCodeType.REGULAR,
            size=(H - 2 * (H // 10), H - 2 * (H // 10)),
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        ).paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_qr_code_and_text(self, text: str, title: str, url: str) -> "Slideshow":
        """
        Add a slide containing a QR code alongside descriptive text and a title.

        This method creates a new slide that features a QR code generated from the
        provided URL, along with the specified title and text. This is useful for
        presentations where you want to direct the audience to a web resource or
        provide additional information while maintaining an engaging visual layout.

        :param text:    A string containing the descriptive text to be displayed on the slide.
        :param title:   A string representing the title to be displayed on the slide.
        :param url:     A string representing the URL that the QR code will link to.
        :return:        Self, allowing for method chaining.
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()
        QRCode(
            qr_code_data=url,
            qr_code_type=QRCode.QRCodeType.REGULAR,
            size=(W // 2 - 2 * (W // 20), H - 2 * (H // 10)),
            padding_top=H // 10,
            padding_bottom=H // 10,
            padding_right=W // 20,
            padding_left=W // 20,
        ).paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_quote(self, author: str, quote: str) -> "Slideshow":
        """
        Add a slide containing a quote attributed to a specified author.

        This method creates a new slide that features the provided quote prominently,
        along with the name of the author. This is useful for highlighting impactful
        statements or insights within the presentation.

        :param author:  The name of the author of the quote.
        :param quote:   The quote to be displayed on the slide.
        :return:        Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=H // 10,
                    padding_bottom=H // 10,
                    padding_left=W // 10,
                    padding_right=W // 10,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Paragraph(
                        text=quote,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=author,
                        text_alignment=LayoutElement.TextAlignment.RIGHT,
                        font=Standard14Fonts.get("Helvetica-Bold"),
                        font_size=(font_size - 2),
                        font_color=Slideshow.__YELLOW_MUNSELL,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=self.__page.get_size())
            if w <= W and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_quote_and_text(
        self, author: str, quote: str, text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with a quote, the author's name, accompanying text, and a title to the PDF document.

        The `add_quote_and_text` method creates a slide that features a prominently displayed quote, the author's name,
        and additional descriptive text.
        The title is displayed at the top, while the text serves to elaborate on or contextualize the quote.

        :param author:  The name of the author of the quote, displayed below the quote.
        :param text:    The descriptive text to be displayed alongside or below the quote.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :param quote:   The quote to be displayed prominently on the slide.
        :return:        Self, allowing for method chaining
        """
        self.__slide_with_text(title=title, text=text)
        assert self.__page is not None
        W, H = self.__page.get_size()

        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=H // 10,
                    padding_bottom=H // 10,
                    padding_right=W // 20,
                    padding_left=W // 20,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Paragraph(
                        text=quote,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=author,
                        text_alignment=LayoutElement.TextAlignment.RIGHT,
                        font_size=(font_size - 2),
                        font=Standard14Fonts.get("Helvetica-Bold"),
                        font_color=Slideshow.__YELLOW_MUNSELL,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=(W // 2, H))
            if w <= W and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_section_title(self, subtitle: str, title: str) -> "Slideshow":
        """
        Add a section title and subtitle to the PDF document.

        The `add_section_title` method inserts a title and an optional subtitle
        to mark the beginning of a new section in the document.
        This is useful for structuring content by clearly defining sections within the slideshow.

        :param subtitle:    The subtitle text to be displayed below the section title. Can be left empty for no subtitle.
        :param title:       The main section title to be prominently displayed.
        :return:            Self, allowing for method chaining.
        """
        self.__slide_with_text(text=subtitle, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()
        import random

        Image(
            bytes_path_pil_image_or_url=random.choice(Slideshow.__SECTION_TITLE_IMAGES),
            size=(W // 2, H),
        ).paint(available_space=(0, 0, W // 2, H), page=self.__page)
        Shape(
            coordinates=[
                (W // 2 - W // 40 + 0.0, 0.0),
                (W // 2 - W // 40, H),
                (W // 2, H),
                (W // 2, 0),
                (W // 2 - W // 40, 0),
            ],
            stroke_color=Slideshow.__YELLOW_MUNSELL,
            fill_color=Slideshow.__YELLOW_MUNSELL,
        ).paint(available_space=(W // 2 - W // 40, 0, W // 40, H), page=self.__page)
        return self

    def append_single_column_of_text(
        self,
        text: str,
        title: str,
    ) -> "Slideshow":
        """
        Add a slide with a single column of text and a title to the PDF document.

        The `add_single_column_of_text` method creates a slide that features a title
        at the top and a single column of text. This is useful for presenting blocks of text,
        such as descriptions, explanations, or bullet points, in a clear and concise manner.

        :param text:    The body of text to be displayed in a single column on the slide.
        :param title:   The title text to be prominently displayed at the top of the slide.
        :return:        Self, allowing for method chaining.
        """
        self.__slide_with_text(text="", title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_paragraph: typing.Optional[Paragraph] = None
        for font_size in range(32, 12, -1):
            tmp_paragraph = Paragraph(
                text=text,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                font_size=font_size,
                font_color=Slideshow.__DARK_GRAY,
                padding_top=H // 10,
                padding_bottom=H // 10,
                padding_right=W // 20,
                padding_left=W // 20,
            )
            w, h = tmp_paragraph.get_size(available_space=(W // 2, H))
            if w <= (W // 2) and h <= H:
                max_paragraph = tmp_paragraph
                break
        assert max_paragraph is not None
        max_paragraph.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_table(
        self, tabular_data: typing.List[typing.List[typing.Any]]
    ) -> "Slideshow":
        """
        Add a slide containing a table based on the provided tabular data.

        This method creates a new slide that presents data in a structured table format.
        The table is generated from the given list of lists, where each inner list
        represents a row of data. This allows for clear organization and presentation
        of various types of information.

        :param tabular_data:    A list of lists containing the data for the table,
                                where each inner list corresponds to a row.
        :return:                Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = TableUtil.from_2d_data(
                tabular_data=tabular_data,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                padding_left=W // 10,
                padding_right=W // 10,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            w, h = tmp_table.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_table_and_text(
        self, tabular_data: typing.List[typing.List[str]], text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with a table, accompanying text, and a title to the PDF document.

        The `add_table_and_text` method creates a slide that displays a table of data along with
        a block of descriptive text and a title.
        The table is constructed from the provided 2D list of strings,
        where each sublist represents a row in the table.
        This method is ideal for presenting structured data along with explanatory text.

        :param tabular_data:    A 2D list of strings representing the table's content. Each sublist corresponds to a row of the table.
        :param text:            The descriptive text to be displayed alongside or below the table.
        :param title:           The title text to be prominently displayed at the top of the slide.
        :return:                Self, allowing for method chaining
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = TableUtil.from_2d_data(
                tabular_data=tabular_data,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                font_size=font_size,
                padding_left=W // 20,
                padding_right=W // 20,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            w, h = tmp_table.get_size(available_space=(W // 2, H))
            if w <= W // 2 and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_title(self, subtitle: str, title: str) -> "Slideshow":
        """
        Add a title and subtitle to the PDF document.

        The `add_title` method allows the user to insert a title and
        a subtitle at a predefined position in the document.
        This is typically used for the main slide or opening page in a slideshow-style PDF.

        :param subtitle:    The subtitle text to be displayed below the title. Can be left empty for no subtitle.
        :param title:       The main title text to be prominently displayed.
        :return:            Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        s = W // 40
        Shape(
            coordinates=[(0.0, 0.0), (0, H), (s, H), (s, s), (W, s), (W, 0), (0, 0)],
            stroke_color=Slideshow.__YELLOW_MUNSELL,
            fill_color=Slideshow.__YELLOW_MUNSELL,
        ).paint(available_space=(0, 0, W, H), page=self.__page)
        max_table: typing.Optional[Table] = None
        for font_size in range(32, 12, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=1,
                    number_of_rows=2,
                    padding_top=H // 10,
                    padding_bottom=H // 10,
                    padding_left=W // 10,
                    padding_right=W // 10,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Paragraph(
                        text=title,
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                        font_size=font_size,
                        font=Standard14Fonts.get("Helvetica-Bold"),
                        font_color=Slideshow.__VERY_DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=subtitle,
                        text_alignment=LayoutElement.TextAlignment.CENTERED,
                        font_size=(font_size - 2),
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_two_columns_of_text(
        self,
        text_left: str,
        text_right: str,
        title: str,
    ) -> "Slideshow":
        """
        Add a slide with two columns of text and a title to the PDF document.

        The `add_two_columns_of_text` method creates a slide that displays text in two columns,
        allowing for a side-by-side comparison or presentation of related content.
        A title is displayed at the top of the slide, while the left and right columns contain the provided text.

        :param title:       The title text to be prominently displayed at the top of the slide.
        :param text_right:  The text to be displayed in the right column.
        :param text_left:   The text to be displayed in the left column.
        :return:            Self, allowing for method chaining
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_table: typing.Optional[Table] = None
        for font_size in range(64, 12, -1):
            tmp_table = (
                FixedColumnWidthTable(
                    number_of_columns=2,
                    number_of_rows=2,
                    padding_top=H // 10,
                    padding_bottom=H // 10,
                    padding_left=W // 10,
                    padding_right=W // 10,
                    horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                    vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                )
                .append_layout_element(
                    Table.TableCell(
                        Paragraph(
                            text=title,
                            text_alignment=LayoutElement.TextAlignment.LEFT,
                            padding_bottom=H // 10,
                            font_size=font_size,
                            font=Standard14Fonts.get("Helvetica-Bold"),
                            font_color=Slideshow.__VERY_DARK_GRAY,
                        ),
                        row_span=1,
                        column_span=2,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=text_left,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        padding_right=W // 20,
                        font_size=(font_size - 2),
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
                .append_layout_element(
                    Paragraph(
                        text=text_right,
                        text_alignment=LayoutElement.TextAlignment.JUSTIFIED,
                        padding_left=W // 20,
                        font_size=(font_size - 2),
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
                .no_borders()
            )
            w, h = tmp_table.get_size(available_space=self.__page.get_size())
            if w <= W and h <= H:
                max_table = tmp_table
                break
        assert max_table is not None
        max_table.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_unordered_list(self, list_data: typing.List[str]) -> "Slideshow":
        """
        Add a slide containing an unordered list based on the provided list data.

        This method creates a new slide that presents a collection of items in a
        structured unordered list format. The list is generated from the provided
        list of strings, where each string represents an item in the list.
        This format is useful for displaying information without implying a specific
        order or ranking.

        :param list_data:   A list of strings containing the items to be displayed
                            in the unordered list.
        :return:            Self, allowing for method chaining.
        """
        self.__empty_slide()
        assert self.__page is not None
        W, H = self.__page.get_size()
        max_list: typing.Optional[UnorderedList] = None
        for font_size in range(64, 12, -1):
            tmp_list = UnorderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                padding_left=W // 10,
                padding_right=W // 10,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            for li in list_data:
                tmp_list.append_layout_element(
                    Paragraph(
                        text=li,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
            w, h = tmp_list.get_size(available_space=(W, H))
            if w <= W and h <= H:
                max_list = tmp_list
                break
        assert max_list is not None
        max_list.paint(
            available_space=(
                0,
                0,
                W,
                H,
            ),
            page=self.__page,
        )
        return self

    def append_unordered_list_and_text(
        self, list_data: typing.List[str], text: str, title: str
    ) -> "Slideshow":
        """
        Add a slide with an unordered list, accompanying text, and a title to the PDF document.

        The `add_unordered_list_and_text` method creates a slide that includes an unordered list
        generated from the provided list of items.
        It also features descriptive text and a title displayed at the top of the slide.
        This method is useful for presenting bullet points along with explanatory text.

        :param list_data:   A list of strings representing the items in the unordered list.
        :param text:        The descriptive text to be displayed alongside or below the unordered list.
        :param title:       The title text to be prominently displayed at the top of the slide.
        :return:            Self, allowing for method chaining
        """
        self.__slide_with_text(text=text, title=title)
        assert self.__page is not None
        W, H = self.__page.get_size()

        max_list: typing.Optional[UnorderedList] = None
        for font_size in range(64, 12, -1):
            tmp_list = UnorderedList(
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
                padding_left=W // 20,
                padding_right=W // 20,
                padding_top=H // 10,
                padding_bottom=H // 10,
            )
            for li in list_data:
                tmp_list.append_layout_element(
                    Paragraph(
                        text=li,
                        font_size=font_size,
                        font_color=Slideshow.__DARK_GRAY,
                    )
                )
            w, h = tmp_list.get_size(available_space=(W // 2, H))
            if w <= W and h <= H:
                max_list = tmp_list
                break
        assert max_list is not None
        max_list.paint(
            available_space=(
                0,
                0,
                W // 2,
                H,
            ),
            page=self.__page,
        )
        return self

    def save(self, path: str) -> "Slideshow":
        """
        Save the slideshow to a specified file path.

        This method writes the current slideshow document to the given file path.
        The document will be saved in the PDF format. If the file already exists,
        it may be overwritten.

        :param path:    The file path where the slideshow will be saved.
        :return:        Self, allowing for method chaining.
        """
        PDF.write(what=self.__document, where_to=path)
        return self
