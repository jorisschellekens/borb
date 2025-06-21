#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate visual elements like diagrams and lists for data representation.

The `SmartArt` class provides static methods to create various visual components such as picture lists, tag clouds,
and process diagrams. These elements can be used to display data in a structured and visually engaging format in
PDFs or other layouts. It supports both horizontal and vertical layouts, offering flexible options for representing
sequences, steps, or categorized information. This class allows you to combine text and images to create organized
and aesthetically pleasing visuals in your documents.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.smart_art.bending_process import BendingProcess
from borb.pdf.layout_element.smart_art.block_list import BasicBlockList
from borb.pdf.layout_element.smart_art.circular_process import CircularProcess
from borb.pdf.layout_element.smart_art.horizontal_ascending_list import (
    HorizontalAscendingList,
)
from borb.pdf.layout_element.smart_art.horizontal_bullet_list import (
    HorizontalBulletList,
)
from borb.pdf.layout_element.smart_art.horizontal_descending_list import (
    HorizontalDescendingList,
)
from borb.pdf.layout_element.smart_art.horizontal_equation import HorizontalEquation
from borb.pdf.layout_element.smart_art.horizontal_picture_list import (
    HorizontalPictureList,
)
from borb.pdf.layout_element.smart_art.horizontal_pie_process import (
    HorizontalPieProcess,
)
from borb.pdf.layout_element.smart_art.horizontal_process import HorizontalProcess
from borb.pdf.layout_element.smart_art.inverted_pyramid import InvertedPyramid
from borb.pdf.layout_element.smart_art.opposing_ideas import OpposingIdeas
from borb.pdf.layout_element.smart_art.pyramid import Pyramid
from borb.pdf.layout_element.smart_art.tags import Tags
from borb.pdf.layout_element.smart_art.vertical_bullet_list import VerticalBulletList
from borb.pdf.layout_element.smart_art.vertical_equation import VerticalEquation
from borb.pdf.layout_element.smart_art.vertical_picture_list import VerticalPictureList
from borb.pdf.layout_element.smart_art.vertical_process import VerticalProcess


class SmartArt:
    """
    Generate visual elements like diagrams and lists for data representation.

    The `SmartArt` class provides static methods to create various visual components such as picture lists, tag clouds,
    and process diagrams. These elements can be used to display data in a structured and visually engaging format in
    PDFs or other layouts. It supports both horizontal and vertical layouts, offering flexible options for representing
    sequences, steps, or categorized information. This class allows you to combine text and images to create organized
    and aesthetically pleasing visuals in your documents.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def bending_process(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a bending process layout with items displayed along a curved path.

        This static method creates a visual layout of a process, arranging each
        item (level 1) along a flowing, curved line to convey a sense of progression
        or continuity. Each item appears as a labeled point along the curve,
        and arrows or lines between items indicate the order of the steps.

        :param level_1_items:       A list of strings representing the primary items or steps in the process.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for item labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed bending process layout, ready for rendering in a graphical interface.
        """
        return BendingProcess.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def block_list(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a Basic Block List layout element with specified attributes.

        This static method creates a visually appealing block list structure
        suitable for use in smart art representations. It allows customization
        of the background color, font color, and font size for the level 1 items.

        :params: level_1_items: A list of strings representing the items to be displayed as the first level in the block list.
        :params: background_color: The background color of the block list. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the level 1 items. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the level 1 items. Defaults to 12.

        :returns:   An instance representing the constructed block list layout element,
                    which can be used for further rendering or manipulation.
        """
        return BasicBlockList.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def circular_process(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a circular process layout with items arranged radially around a center.

        This static method creates a visual layout of a process, placing each
        item (level 1) evenly spaced around a circle to represent cyclical flow
        or repeating sequences. Arrows connect items in a clockwise direction,
        emphasizing the ongoing, looped nature of the process.

        :param level_1_items:       A list of strings representing the primary items or steps in the process.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for item labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed circular process layout, ready for rendering in a graphical interface.
        """
        return CircularProcess.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def horizontal_ascending_list(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a horizontal ascending list layout with items displayed in a progressively elevated order.

        This static method creates a visual layout for displaying items
        horizontally, with each item slightly higher than the previous one
        to indicate upward progression. Customization options for background
        color, font color, and font size allow the layout to be adapted to
        specific visual requirements, making it suitable for representing
        ordered steps, rankings, or achievements.

        :param level_1_items: A list of strings representing the items to be displayed in ascending order.
        :param background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color: The font color for the item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size: The font size for the item labels. Defaults to 12.
        :return: A LayoutElement representing the constructed horizontal ascending list layout, ready for rendering in a graphical interface.
        """
        return HorizontalAscendingList.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def horizontal_bullet_list(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
    ) -> LayoutElement:
        """
        Construct a horizontal bullet list layout element with specified attributes for multiple levels of items.

        This static method creates a structured horizontal bullet list where
        the first level contains primary items and the second level contains
        sub-items for each primary item. It allows for customization of
        background colors, font colors, and font sizes for both levels.

        :params: level_1_items: A list of strings representing the primary items in the bullet list.
        :params: level_2_items: A list of lists, where each sub-list contains strings representing the sub-items corresponding to the primary items.
        :params: background_color: The background color of the bullet list. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the primary items. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the primary items. Defaults to 16.
        :params: level_2_font_color: The font color for the sub-items. Defaults to X11Color.WHITE.
        :params: level_2_font_size: The font size for the sub-items. Defaults to 14.

        :returns: A LayoutElement representing the constructed horizontal bullet list layout, suitable for rendering in a graphical interface.
        """
        return HorizontalBulletList.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
        )

    @staticmethod
    def horizontal_descending_list(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a horizontal descending list layout with items displayed in a progressively elevated order.

        This static method creates a visual layout for displaying items
        horizontally, with each item slightly higher than the previous one
        to indicate upward progression. Customization options for background
        color, font color, and font size allow the layout to be adapted to
        specific visual requirements, making it suitable for representing
        ordered steps, rankings, or achievements.

        :param level_1_items: A list of strings representing the items to be displayed in descending order.
        :param background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color: The font color for the item labels. Defaults to X11Color.WHITE.
        :param level_1_font_size: The font size for the item labels. Defaults to 12.
        :return: A LayoutElement representing the constructed horizontal descending list layout, ready for rendering in a graphical interface.
        """
        return HorizontalDescendingList.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def horizontal_equation(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a horizontal equation layout displaying a fixed format equation: "A + B + C ... = D".

        This method arranges items horizontally in a predetermined equation
        structure, where each item in `level_1_items` is displayed sequentially
        as terms (A, B, C, etc.) on the left side of a "+" operation, culminating
        in an "=" operation leading to the final result. The "+" and "=" operators
        are fixed and cannot be modified. Customization options for background
        color, font color, and font size allow the equation's appearance to be
        tailored as needed.

        :param level_1_items:       A list of strings representing the items to be  included in the equation, where each item will represent a term of the equation.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for the equation terms. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for the equation terms. Defaults to 12.
        :return:                    A LayoutElement representing the horizontal equation layout, ready for rendering with a fixed structure showing "A + B + C ... = D".
        """
        return HorizontalEquation.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def horizontal_picture_list(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        pictures: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
        picture_size: typing.Tuple[int, int] = (128, 128),
    ) -> LayoutElement:
        """
        Construct a horizontal list layout element containing paired items with hierarchical text levels and images.

        This method arranges `level_1_items` in a horizontal row, where each main item is paired with a list of sub-items
        (`level_2_items`) and an associated image. Each item can be customized with specific colors, font sizes,
        and image dimensions to create a visually cohesive horizontal list.

        :param level_1_items: Primary text items to be displayed at the top level in the horizontal list.
        :param level_2_items: A list of lists, where each sublist contains secondary text items related to each corresponding item in `level_1_items`. Each sublist aligns with the structure of `level_1_items`.
        :param pictures: Paths to images that accompany each primary item. The length should match `level_1_items` for consistent pairing.
        :param background_color: Background color of the layout. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: Font color for `level_1_items`. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: Font size for `level_1_items`. Defaults to 16.
        :param level_2_font_color: Font color for `level_2_items`. Defaults to `X11Color.WHITE`.
        :param level_2_font_size: Font size for `level_2_items`. Defaults to 14.
        :param picture_size: Dimensions of each picture in pixels, as (width, height). Defaults to (128, 128).

        :return: A layout element representing the horizontally aligned list with hierarchical text and image elements.
        """
        return HorizontalPictureList.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            pictures=pictures,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
            picture_size=picture_size,
        )

    @staticmethod
    def horizontal_pie_process(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
    ) -> LayoutElement:
        """
        Construct a horizontal process layout with steps, each accompanied by a pie chart indicating progress.

        This static method builds a visual representation of a multistep
        process. Each step (level 1 item) is displayed alongside a corresponding
        set of details (level 2 items) and a pie chart that illustrates the
        progress for that step. The method allows customization of background
        color, font colors, and font sizes for both levels, providing a clear
        and aesthetically pleasing layout.

        :params: level_1_items:         A list of strings representing the main steps in the process.
        :params: level_2_items:         A list of lists, where each sub-list contains strings providing additional details or sub-steps related to each main step.
        :params: background_color:      The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color:    The font color for the main step items. Defaults to X11Color.WHITE.
        :params: level_1_font_size:     The font size for the main step items. Defaults to 16.
        :params: level_2_font_color:    The font color for the sub-step items. Defaults to X11Color.WHITE.
        :params: level_2_font_size:     The font size for the sub-step items. Defaults to 14.
        :returns:                       A LayoutElement representing the constructed horizontal process layout, suitable for rendering in a graphical interface.
        """
        return HorizontalPieProcess.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
        )

    @staticmethod
    def horizontal_process(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a horizontal process layout with items represented as blocks connected by arrows.

        This static method creates a visual representation of a series of items
        in a process, where each item (level 1) is displayed as a block.
        The blocks are connected by arrows to illustrate the flow of the process.
        Users can customize the background color, font color, and font size
        for the block labels, allowing for a tailored appearance.

        :params: level_1_items: A list of strings representing the items in the process.
        :params: background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the block labels. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the block labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed horizontal process layout, suitable for rendering.
        """
        return HorizontalProcess.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def inverted_pyramid(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Build an inverted pyramid layout as a `LayoutElement` with the given items and appearance settings.

        This method creates a hierarchical inverted pyramid structure where each item is displayed
        in a centered row. The rows progressively narrow toward the base, forming the shape of an upside-down pyramid.
        The visual appearance can be customized with parameters such as background color, font color, and font size.

        :param level_1_items: A list of strings representing the items to include in the inverted pyramid. Each string corresponds to a row, starting from the widest row at the top.
        :param background_color: The background color for the pyramid rows. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: The font color for the text in the pyramid. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: The font size for the text in the pyramid. Defaults to `12`.

        :return: A `LayoutElement` representing the inverted pyramid structure, ready to be added to a PDF.
        """
        return InvertedPyramid.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def opposing_ideas(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
    ) -> LayoutElement:
        """
        Construct an "opposing ideas" layout, visually contrasting two sets of ideas with directional arrows emphasizing the distinction.

        This static method arranges items in two levels to visually represent
        opposing concepts or ideas. Each item in `level_1_items` corresponds to
        an item in `level_2_items`, with an arrow pointing down towards the
        first level and an arrow pointing up towards the second, emphasizing
        the contrast between the two. Customization options for colors and
        font sizes allow for adapting the layout to different visual themes.

        :param level_1_items: A list of strings representing the first set of items or ideas (Level 1).
        :param level_2_items: A list of lists, where each sub-list contains strings for the corresponding items in the second set (Level 2).
        :param background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color: The font color for Level 1 items. Defaults to X11Color.WHITE.
        :param level_1_font_size: The font size for Level 1 items. Defaults to 16.
        :param level_2_font_color: The font color for Level 2 items. Defaults to X11Color.WHITE.
        :param level_2_font_size: The font size for Level 2 items. Defaults to 14.
        :return: A LayoutElement representing the constructed "opposing ideas" layout, suitable for rendering in a graphical interface.
        """
        return OpposingIdeas.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
        )

    @staticmethod
    def pyramid(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Build a pyramid layout as a `LayoutElement` with the given items and appearance settings.

        This method creates a hierarchical pyramid structure where each item is displayed
        in a centered row. The rows are progressively wider toward the base, forming the
        shape of a pyramid. The visual appearance can be customized with parameters
        such as background color, font color, and font size.

        :param level_1_items: A list of strings representing the items to include in the pyramid. Each string corresponds to a row, starting from the top.
        :param background_color: The background color for the pyramid rows. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: The font color for the text in the pyramid. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: The font size for the text in the pyramid. Defaults to `12`.

        :return: A `LayoutElement` representing the pyramid structure, ready to be added to a PDF.
        """
        return Pyramid.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def tags(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Build a layout element representing the collection of tags.

        This method constructs a visual representation of the tags as a paragraph, with each tag styled
        using the specified background color, font color, and font size. Tags are separated by underscores.

        :param level_1_items: A list of strings representing the tags to display.
        :param background_color: The background color for the tags. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color: The font color for the tags. Defaults to `X11Color.WHITE`.
        :param level_1_font_size: The font size for the tags. Defaults to 12.
        :return: A `LayoutElement` representing the formatted tags.
        """
        return Tags.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def vertical_bullet_list(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
    ) -> LayoutElement:
        """
        Construct a vertical bullet list layout element with specified attributes for multiple levels of items.

        This static method creates a structured horizontal bullet list where
        the first level contains primary items and the second level contains
        sub-items for each primary item. It allows for customization of
        background colors, font colors, and font sizes for both levels.

        :params: level_1_items: A list of strings representing the primary items in the bullet list.
        :params: level_2_items: A list of lists, where each sub-list contains strings representing the sub-items corresponding to the primary items.
        :params: background_color: The background color of the bullet list. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the primary items. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the primary items. Defaults to 16.
        :params: level_2_font_color: The font color for the sub-items. Defaults to X11Color.WHITE.
        :params: level_2_font_size: The font size for the sub-items. Defaults to 14.

        :returns: A LayoutElement representing the constructed vertical bullet list layout, suitable for rendering in a graphical interface.
        """
        return VerticalBulletList.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
        )

    @staticmethod
    def vertical_equation(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a vertical equation layout displaying a fixed format equation: "A + B + C ... = D".

        This method arranges items horizontally in a predetermined equation
        structure, where each item in `level_1_items` is displayed sequentially
        as terms (A, B, C, etc.) on the left side of a "+" operation, culminating
        in an "=" operation leading to the final result. The "+" and "=" operators
        are fixed and cannot be modified. Customization options for background
        color, font color, and font size allow the equation's appearance to be
        tailored as needed.

        :param level_1_items:       A list of strings representing the items to be  included in the equation, where each item will represent a term of the equation.
        :param background_color:    The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :param level_1_font_color:  The font color for the equation terms. Defaults to X11Color.WHITE.
        :param level_1_font_size:   The font size for the equation terms. Defaults to 12.
        :return:                    A LayoutElement representing the horizontal equation layout, ready for rendering with a fixed structure showing "A + B + C ... = D".
        """
        return VerticalEquation.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )

    @staticmethod
    def vertical_picture_list(
        level_1_items: typing.List[str],
        level_2_items: typing.List[typing.List[str]],
        pictures: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size: int = 16,
        level_2_font_color: Color = X11Color.WHITE,
        level_2_font_size: int = 14,
        picture_size: typing.Tuple[int, int] = (128, 128),
    ) -> LayoutElement:
        """
        Construct a vertical list layout element containing paired items with hierarchical text levels and images.

        This method builds a visual element that organizes `level_1_items` in a primary list format, where each main item
        is accompanied by a list of sub-items (`level_2_items`) and an associated image. It supports customization of
        text and background colors, font sizes, and image sizing for tailored styling.

        :param level_1_items:       Primary text items to be displayed at the top level in the vertical list.
        :param level_2_items:       A list of lists, where each sublist contains secondary text items related to each corresponding `level_1_item`. Each sublist aligns with the hierarchy of the primary items.
        :param pictures:            Paths to images that will accompany each primary item. The length should match `level_1_items` for consistent pairing.
        :param background_color:    Background color of the layout. Defaults to `X11Color.PRUSSIAN_BLUE`.
        :param level_1_font_color:  Font color for `level_1_items`. Defaults to `X11Color.WHITE`.
        :param level_1_font_size:   Font size for `level_1_items`. Defaults to 16.
        :param level_2_font_color:  Font color for `level_2_items`. Defaults to `X11Color.WHITE`.
        :param level_2_font_size:   Font size for `level_2_items`. Defaults to 14.
        :param picture_size:        Width and height for each picture in pixels. Defaults to (128, 128).

        :return: A layout element object representing the vertically aligned list with hierarchical text and image elements.
        """
        return VerticalPictureList.build(
            level_1_items=level_1_items,
            level_2_items=level_2_items,
            pictures=pictures,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
            level_2_font_color=level_2_font_color,
            level_2_font_size=level_2_font_size,
            picture_size=picture_size,
        )

    @staticmethod
    def vertical_process(
        level_1_items: typing.List[str],
        background_color: Color = X11Color.PRUSSIAN_BLUE,
        level_1_font_color: Color = X11Color.WHITE,
        level_1_font_size=12,
    ) -> LayoutElement:
        """
        Construct a vertical process layout with items represented as blocks connected by arrows.

        This static method creates a visual representation of a series of items
        in a process, where each item (level 1) is displayed as a block.
        The blocks are connected by arrows to illustrate the flow of the process.
        Users can customize the background color, font color, and font size
        for the block labels, allowing for a tailored appearance.

        :params: level_1_items: A list of strings representing the items in the process.
        :params: background_color: The background color for the layout. Defaults to X11Color.PRUSSIAN_BLUE.
        :params: level_1_font_color: The font color for the block labels. Defaults to X11Color.WHITE.
        :params: level_1_font_size: The font size for the block labels. Defaults to 12.
        :returns: A LayoutElement representing the constructed vertical process layout, suitable for rendering.
        """
        return VerticalProcess.build(
            level_1_items=level_1_items,
            background_color=background_color,
            level_1_font_color=level_1_font_color,
            level_1_font_size=level_1_font_size,
        )
