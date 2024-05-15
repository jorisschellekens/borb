#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A SmartArt graphic is a visual representation of your information and ideas.
You create one by choosing a layout that fits your message.
Some layouts (such as organization charts and Venn diagrams) portray specific kinds of information,
while others simply enhance the appearance of a bulleted list.
"""

import math
import random
import types
import typing
from decimal import Decimal

# fmt: off
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.layout.emoji.emoji import Emoji
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.inline_flow import InlineFlow
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.page.page import Page


# fmt: on


class SmartArt:
    """
    A SmartArt graphic is a visual representation of your information and ideas.
    You create one by choosing a layout that fits your message.
    Some layouts (such as organization charts and Venn diagrams) portray specific kinds of information,
    while others simply enhance the appearance of a bulleted list.
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
    def alternating_picture_list(
        pictures: typing.List[str],
        texts: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
    ) -> LayoutElement:
        """
        Use to show a series of pictures from top to bottom. Text appears alternately on the right or left of the picture.
        :param texts:               the typing.List[str] to be used as
        :param pictures             the typing.List[str] to be used as image URLs
        :param font_size:           the font_size to be used
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(texts) > 0
        assert len(pictures) > 0
        assert len(texts) == len(pictures)
        assert font_size > 0

        N: int = len(texts)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=3, number_of_rows=N
        )

        # add content
        for i in range(0, N):
            if i % 2 == 0:
                table.add(
                    TableCell(
                        Paragraph(
                            texts[i],
                            font_color=font_color,
                            font_size=font_size,
                            background_color=background_color,
                        ),
                        column_span=2,
                        border_left=False,
                        border_top=(True if i != 0 else False),
                        border_bottom=(True if i != N - 1 else False),
                        background_color=background_color,
                        border_color=HexColor("FFFFFF"),
                        border_width=font_size / 2,
                    )
                )
                table.add(
                    TableCell(
                        Image(pictures[i], width=Decimal(64), height=Decimal(64)),
                        border_right=False,
                        border_top=(True if i != 0 else False),
                        border_bottom=(True if i != N - 1 else False),
                        border_color=HexColor("FFFFFF"),
                        background_color=background_color,
                        border_width=font_size / 2,
                    )
                )
            else:
                table.add(
                    TableCell(
                        Image(pictures[i], width=Decimal(64), height=Decimal(64)),
                        border_left=False,
                        border_bottom=(True if i != N - 1 else False),
                        background_color=background_color,
                        border_color=HexColor("FFFFFF"),
                        border_width=font_size / 2,
                    )
                )
                table.add(
                    TableCell(
                        Paragraph(
                            texts[i],
                            font_color=font_color,
                            font_size=font_size,
                            background_color=background_color,
                        ),
                        border_right=False,
                        border_bottom=(True if i != N - 1 else False),
                        column_span=2,
                        background_color=background_color,
                        border_color=HexColor("FFFFFF"),
                        border_width=font_size / 2,
                    )
                )

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)

        # return
        return table

    @staticmethod
    def ascending_block_list(
        text_level_1: typing.List[str],
        text_level_2: typing.List[typing.List[str]],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show groups of related ideas or lists of information.
        The text shapes increase in height sequentially, and the Level 1 text displays vertically.
        :param text_level_1:        the typing.List[str] to be used as level 1 text
        :param text_level_2         the typing.List[typing.List[str]] to be used as level 2 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text_level_1) > 0
        assert len(text_level_2) > 0
        assert all([len(x) > 0 for x in text_level_2])
        assert len(text_level_1) == len(text_level_2)
        assert font_size > 0
        N: int = len(text_level_1)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=N, number_of_rows=2 + (N - 1)
        )
        for i in range(0, N - 1):
            for j in range(0, N):
                if N - j - 1 > i:
                    table.add(
                        TableCell(
                            Paragraph(" "),
                            border_top=False,
                            border_right=False,
                            border_bottom=False,
                            border_left=False,
                        )
                    )
                else:
                    table.add(
                        TableCell(
                            Paragraph(" "),
                            background_color=background_color,
                            border_width=font_size / 2,
                            border_color=HexColor("ffffff"),
                            border_right=True if j != N - 1 else False,
                            border_left=True if j != 0 else False,
                            border_top=False,
                            border_bottom=False,
                        )
                    )

        for i in range(0, N):
            table.add(
                TableCell(
                    Paragraph(
                        text_level_1[i],
                        font_size=font_size + Decimal(2),
                        font="Helvetica-Bold",
                        font_color=font_color,
                        background_color=background_color,
                    ),
                    background_color=background_color,
                    border_width=font_size / 2,
                    border_color=HexColor("ffffff"),
                    border_right=True if i != N - 1 else False,
                    border_left=True if i != 0 else False,
                    border_top=False,
                    border_bottom=False,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )
        for i in range(0, N):
            ul: UnorderedList = UnorderedList()
            for li in text_level_2[i]:
                ul.add(Paragraph(li, font_size=font_size, font_color=font_color))
            table.add(
                TableCell(
                    ul,
                    background_color=background_color,
                    border_width=font_size / 2,
                    border_color=HexColor("ffffff"),
                    border_right=True if i != N - 1 else False,
                    border_left=True if i != 0 else False,
                    border_top=False,
                    border_bottom=False,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )
        return table

    @staticmethod
    def basic_bending_process(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show a long or non-linear sequence or steps in a task, process, or workflow.
        Works best with Level 1 text only. Maximizes both horizontal and vertical display space for shapes.
        :param text:                the typing.List[str] to be used as level 1 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text) > 0
        assert font_size > 0
        ncols: int = math.ceil(math.sqrt(len(text)))
        nrows: int = math.ceil(len(text) / ncols)

        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=ncols * 2 - 1, number_of_rows=nrows * 2 - 1
        )

        filling_left_to_right: bool = True
        elements_to_add: typing.List[str] = text
        while len(elements_to_add) > 0:
            next_row: typing.List[typing.Optional[str]] = elements_to_add[0:ncols]  # type: ignore [assignment]
            elements_to_add = elements_to_add[ncols:]
            while len(next_row) != ncols:
                next_row.append(None)
            if not filling_left_to_right:
                next_row.reverse()

            # add <data> + <arrow>
            for i, e in enumerate(next_row):
                if e is None:
                    table.add(Paragraph(" "))
                else:
                    table.add(
                        TableCell(
                            Paragraph(
                                e,
                                font_size=font_size,
                                font_color=font_color,
                                background_color=background_color,
                            ),
                            background_color=background_color,
                        )
                    )

                #
                # ADD ARROW BETWEEN BLOCKS
                #
                add_arrow: bool = False
                add_empty_paragraph_instead_of_arrow: bool = True
                if filling_left_to_right:
                    if (i != len(next_row) - 1) and next_row[i + 1] is not None:
                        add_arrow = True
                if not filling_left_to_right and next_row[i] is not None:
                    add_arrow = True
                if i == len(next_row) - 1:
                    add_arrow = False
                    add_empty_paragraph_instead_of_arrow = False
                if not add_arrow:
                    if add_empty_paragraph_instead_of_arrow:
                        table.add(Paragraph(" "))
                else:
                    # add arrow (depending on the fill direction of this line)
                    if filling_left_to_right:
                        table.add(
                            ConnectedShape(
                                LineArtFactory.arrow_right(
                                    Rectangle(
                                        Decimal(0),
                                        Decimal(0),
                                        Decimal(32),
                                        Decimal(32),
                                    )
                                ),
                                stroke_color=foreground_color,
                                fill_color=foreground_color,
                            )
                        )
                    else:
                        table.add(
                            ConnectedShape(
                                LineArtFactory.arrow_left(
                                    Rectangle(
                                        Decimal(0),
                                        Decimal(0),
                                        Decimal(32),
                                        Decimal(32),
                                    )
                                ),
                                stroke_color=foreground_color,
                                fill_color=foreground_color,
                            )
                        )

            # add <empty> + <arrow down>
            if len(elements_to_add) > 0:
                # add arrow down
                if filling_left_to_right:
                    for _ in range(0, ncols * 2 - 2):
                        table.add(Paragraph(" "))
                    table.add(
                        ConnectedShape(
                            LineArtFactory.arrow_down(
                                Rectangle(
                                    Decimal(0), Decimal(0), Decimal(32), Decimal(32)
                                )
                            ),
                            stroke_color=foreground_color,
                            fill_color=foreground_color,
                        )
                    )
                else:
                    table.add(
                        ConnectedShape(
                            LineArtFactory.arrow_down(
                                Rectangle(
                                    Decimal(0), Decimal(0), Decimal(32), Decimal(32)
                                )
                            ),
                            stroke_color=foreground_color,
                            fill_color=foreground_color,
                        )
                    )
                    for _ in range(0, ncols * 2 - 2):
                        table.add(Paragraph(" "))

            # reverse line direction
            filling_left_to_right = not filling_left_to_right

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)
        table.no_borders()

        # return
        return table

    @staticmethod
    def closed_chevron_process(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show a progression, a timeline, or sequential steps in a task, process, or workflow, or to emphasize movement or direction.
        Can be used to emphasize information in the starting shape. Works best with Level 1 text only.
        :param text:
        :param font_size:
        :param foreground_color:
        :param background_color:
        :param font_color:
        :return:
        """
        assert font_size > 0
        N = len(text)
        table = FlexibleColumnWidthTable(number_of_columns=N * 2 + 1, number_of_rows=2)

        #
        # 1st row
        #

        # add triangle shape
        Z: Decimal = Decimal(0)
        H: Decimal = Decimal(50)
        table.add(
            TableCell(
                ConnectedShape(
                    [(Z, H), (H, H), (H, Z)],
                    fill_color=foreground_color,
                    stroke_color=foreground_color,
                )
            )
        )

        c0: Color = foreground_color
        c1: Color = background_color
        for i, li in enumerate(text):
            if i % 2 == 0:
                c0 = foreground_color
                c1 = background_color
            else:
                c0 = background_color
                c1 = foreground_color

            # add text
            table.add(
                TableCell(
                    Paragraph(li, font_size=font_size, font_color=font_color),
                    background_color=c0,
                    row_span=2,
                    padding_left=font_size,
                    padding_right=font_size,
                    padding_top=font_size,
                    padding_bottom=font_size,
                )
            )
            if i != N - 1:
                table.add(
                    TableCell(
                        ConnectedShape(
                            [(Z, Z), (Z, H), (H, Z)], fill_color=c0, stroke_color=c0
                        ),
                        background_color=c1,
                    )
                )
            else:
                table.add(
                    TableCell(
                        ConnectedShape(
                            [(Z, Z), (Z, H), (H, Z)], fill_color=c0, stroke_color=c0
                        )
                    )
                )

        #
        # 2nd row
        #

        # add triangle shape
        table.add(
            TableCell(
                ConnectedShape(
                    [(Z, Z), (H, H), (H, Z)],
                    fill_color=foreground_color,
                    stroke_color=foreground_color,
                )
            )
        )

        for i in range(0, N):
            if i % 2 == 0:
                c0 = foreground_color
                c1 = background_color
            else:
                c0 = background_color
                c1 = foreground_color

            # add triangle shape
            if i != N - 1:
                table.add(
                    TableCell(
                        ConnectedShape(
                            [(Z, Z), (Z, H), (H, H)], fill_color=c0, stroke_color=c0
                        ),
                        background_color=c1,
                    )
                )
            else:
                table.add(
                    TableCell(
                        ConnectedShape(
                            [(Z, Z), (Z, H), (H, H)], fill_color=c0, stroke_color=c0
                        )
                    )
                )
        table.no_borders()

        # return
        return table

    @staticmethod
    def descending_block_list(
        text_level_1: typing.List[str],
        text_level_2: typing.List[typing.List[str]],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
    ) -> LayoutElement:
        """
        Use to show groups of related ideas or lists of information.
        The text shapes decrease in height sequentially, and the Level 1 text displays vertically.
        :param text_level_1:        the typing.List[str] to be used as level 1 text
        :param text_level_2         the typing.List[typing.List[str]] to be used as level 2 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text_level_1) > 0
        assert len(text_level_2) > 0
        assert all([len(x) > 0 for x in text_level_2])
        assert len(text_level_1) == len(text_level_2)
        assert font_size > 0
        N: int = len(text_level_1)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=N, number_of_rows=2 + (N - 1)
        )
        for i in range(0, N - 1):
            for j in range(0, N):
                if j > i:
                    table.add(
                        TableCell(
                            Paragraph(" "),
                            border_top=False,
                            border_right=False,
                            border_bottom=False,
                            border_left=False,
                        )
                    )
                else:
                    table.add(
                        TableCell(
                            Paragraph(" "),
                            background_color=background_color,
                            border_width=font_size / 2,
                            border_color=HexColor("ffffff"),
                            border_right=True if j != N - 1 else False,
                            border_left=True if j != 0 else False,
                            border_top=False,
                            border_bottom=False,
                        )
                    )

        for i in range(0, N):
            table.add(
                TableCell(
                    Paragraph(
                        text_level_1[i],
                        font_size=font_size + Decimal(2),
                        font="Helvetica-Bold",
                        font_color=font_color,
                        background_color=background_color,
                    ),
                    background_color=background_color,
                    border_width=font_size / 2,
                    border_color=HexColor("ffffff"),
                    border_right=True if i != N - 1 else False,
                    border_left=True if i != 0 else False,
                    border_top=False,
                    border_bottom=False,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )
        for i in range(0, N):
            ul: UnorderedList = UnorderedList()
            for li in text_level_2[i]:
                ul.add(Paragraph(li, font_size=font_size, font_color=font_color))
            table.add(
                TableCell(
                    ul,
                    background_color=background_color,
                    border_width=font_size / 2,
                    border_color=HexColor("ffffff"),
                    border_right=True if i != N - 1 else False,
                    border_left=True if i != 0 else False,
                    border_top=False,
                    border_bottom=False,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )
        return table

    @staticmethod
    def horizontal_bullet_list(
        text_level_1: typing.List[str],
        text_level_2: typing.List[typing.List[str]],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        A horizontal bullet list is used to show non-sequential information or grouped data, yet it will not affect the outcome of the other data.
        The first block on the left is related to the second block as well as the third block but the process of the
        second block is not dependent on how the process on the first block is implemented.
        Apart from this, each block of information has the same emphasis, and it does not connote any direction.
        :param text_level_1:        the typing.List[str] to be used as level 1 text
        :param text_level_2         the typing.List[typing.List[str]] to be used as level 2 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text_level_1) > 0
        assert len(text_level_2) > 0
        assert all([len(x) > 0 for x in text_level_2])
        assert len(text_level_1) == len(text_level_2)
        assert font_size > 0
        N: int = len(text_level_1)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=N, number_of_rows=2
        )

        # add headers
        for i in range(0, N):
            table.add(
                TableCell(
                    Paragraph(
                        text_level_1[i],
                        font_size=font_size + Decimal(2),
                        font="Helvetica-Bold",
                        background_color=background_color,
                        font_color=font_color,
                    ),
                    border_top=False,
                    border_bottom=False,
                    border_left=(True if i != 0 else False),
                    border_right=(True if i != N - 1 else False),
                    border_width=font_size / 2,
                    background_color=background_color,
                    border_color=HexColor("FFFFFF"),
                )
            )

        # add body
        for i in range(0, N):
            ul: UnorderedList = UnorderedList()
            for li in text_level_2[i]:
                ul.add(
                    Paragraph(
                        li,
                        font_size=font_size,
                        background_color=foreground_color,
                        font_color=font_color,
                    )
                )
            table.add(
                TableCell(
                    ul,
                    border_top=False,
                    border_bottom=False,
                    border_left=(True if i != 0 else False),
                    border_right=(True if i != N - 1 else False),
                    border_width=font_size / 2,
                    background_color=foreground_color,
                    border_color=HexColor("FFFFFF"),
                )
            )
        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)

        # return
        return table

    @staticmethod
    def horizontal_process(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show a progression or sequential steps in a task, process, or workflow.
        :param text:                the typing.List[str] to be used as level 1 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text) > 0
        assert font_size > 0
        N: int = len(text)
        n: int = N * 2 - 1
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=n, number_of_rows=1
        )
        for i, e in enumerate(text):
            table.add(
                TableCell(
                    Paragraph(
                        e,
                        font_size=font_size,
                        font_color=font_color,
                        background_color=background_color,
                    ),
                    background_color=background_color,
                )
            )
            if i != len(text) - 1:
                table.add(
                    ConnectedShape(
                        LineArtFactory.arrow_right(
                            Rectangle(
                                Decimal(0),
                                Decimal(0),
                                Decimal(32),
                                Decimal(32),
                            )
                        ),
                        stroke_color=foreground_color,
                        fill_color=foreground_color,
                    )
                )

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)
        table.no_borders()

        # return
        return table

    @staticmethod
    def matrix(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        A matrix is a rectangular array of elements, arranged in rows and columns, and can be used to show the placement of concepts along two axes.
        For example, you can use a matrix to illustrate the four possible combinations of two concepts or ingredients.
        :param text:                the typing.List[str] to be used in the 4 boxes
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text) == 4
        assert font_size > 0
        modified_table: LayoutElement = (
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .add(
                TableCell(
                    Paragraph(
                        text[0],
                        font_size=font_size,
                        text_alignment=Alignment.CENTERED,
                        horizontal_alignment=Alignment.CENTERED,
                        font_color=font_color,
                    ),
                    border_width=font_size / 2,
                    border_top=False,
                    border_right=True,
                    border_bottom=True,
                    border_left=False,
                    border_color=background_color,
                )
            )
            .add(
                TableCell(
                    Paragraph(
                        text[1],
                        font_size=font_size,
                        text_alignment=Alignment.CENTERED,
                        horizontal_alignment=Alignment.CENTERED,
                        font_color=font_color,
                    ),
                    border_width=font_size / 2,
                    border_top=False,
                    border_right=False,
                    border_bottom=True,
                    border_left=True,
                    border_color=background_color,
                )
            )
            .add(
                TableCell(
                    Paragraph(
                        text[2],
                        font_size=font_size,
                        text_alignment=Alignment.CENTERED,
                        horizontal_alignment=Alignment.CENTERED,
                        font_color=font_color,
                    ),
                    border_width=font_size / 2,
                    border_top=True,
                    border_right=True,
                    border_bottom=False,
                    border_left=False,
                    border_color=background_color,
                )
            )
            .add(
                TableCell(
                    Paragraph(
                        text[3],
                        font_size=font_size,
                        text_alignment=Alignment.CENTERED,
                        horizontal_alignment=Alignment.CENTERED,
                        font_color=font_color,
                    ),
                    border_width=font_size / 2,
                    border_top=True,
                    border_right=False,
                    border_bottom=False,
                    border_left=True,
                    border_color=background_color,
                )
            )
            .set_padding_on_all_cells(font_size, font_size, font_size, font_size)
            .set_background_color_on_all_cells(foreground_color)
        )

        # get the paint method
        prev_paint = modified_table.paint

        # build a modified paint method
        def _modified_paint_method(obj, page: Page, available_space: Rectangle):
            lbox: Rectangle = obj.get_layout_box(available_space)
            lbox = lbox.grow(font_size)
            ConnectedShape(
                LineArtFactory.diamond(lbox),
                stroke_color=background_color,
                fill_color=background_color,
            ).paint(page, lbox)
            prev_paint(page, available_space)

        # assign
        modified_table.paint = types.MethodType(_modified_paint_method, modified_table)  # type: ignore [assignment]

        # return
        output_element: LayoutElement = InlineFlow().add(modified_table)
        output_element._margin_top = font_size
        output_element._margin_right = font_size
        output_element._margin_bottom = font_size
        output_element._margin_left = font_size
        return output_element

    @staticmethod
    def opposing_ideas(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show two opposing or contrasting ideas. Has two Level 1 items.
        Works well with large amounts of text.
        :param text:                the typing.List[str] to be used as level 1 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text) > 0
        assert font_size > 0
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=4, number_of_rows=1
        )

        # row 1
        table.add(
            ConnectedShape(
                LineArtFactory.arrow_up(
                    Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
                ),
                stroke_color=background_color,
                fill_color=background_color,
                vertical_alignment=Alignment.MIDDLE,
            )
        )
        table.add(
            TableCell(
                Paragraph(
                    text[0],
                    font_size=font_size,
                    font_color=font_color,
                    background_color=background_color,
                ),
                border_radius_bottom_left=Decimal(20),
                background_color=background_color,
            )
        )
        table.add(
            TableCell(
                Paragraph(
                    text[1],
                    font_size=font_size,
                    font_color=font_color,
                    background_color=foreground_color,
                ),
                border_radius_top_right=Decimal(20),
                background_color=foreground_color,
            )
        )
        table.add(
            ConnectedShape(
                LineArtFactory.arrow_down(
                    Rectangle(Decimal(0), Decimal(0), Decimal(32), Decimal(32))
                ),
                stroke_color=foreground_color,
                fill_color=foreground_color,
                vertical_alignment=Alignment.MIDDLE,
            )
        )

        # set global properties
        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)
        table.no_borders()

        # return
        return table

    @staticmethod
    def picture_list(
        pictures: typing.List[str],
        texts: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
    ) -> LayoutElement:
        """
        Use to show a series of pictures from top to bottom. Text appears on the right of the picture.
        :param texts:               the typing.List[str] to be used as
        :param pictures             the typing.List[str] to be used as image URLs
        :param font_size:           the font_size to be used
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(texts) > 0
        assert len(pictures) > 0
        assert len(texts) == len(pictures)
        assert font_size > 0

        N: int = len(texts)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=3, number_of_rows=N
        )

        # add content
        for i in range(0, N):
            table.add(
                TableCell(
                    Image(pictures[i], width=Decimal(64), height=Decimal(64)),
                    border_right=True,
                    border_left=False,
                    border_top=(True if i != 0 else False),
                    border_bottom=(True if i != N - 1 else False),
                    border_color=HexColor("FFFFFF"),
                    background_color=background_color,
                    border_width=font_size / 2,
                )
            )
            table.add(
                TableCell(
                    Paragraph(
                        texts[i],
                        font_color=font_color,
                        font_size=font_size,
                        background_color=background_color,
                    ),
                    column_span=2,
                    border_right=False,
                    border_left=True,
                    border_top=(True if i != 0 else False),
                    border_bottom=(True if i != N - 1 else False),
                    background_color=background_color,
                    border_color=HexColor("FFFFFF"),
                    border_width=font_size / 2,
                )
            )

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)

        # return
        return table

    @staticmethod
    def table_hierarcy(
        text: typing.Any,
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show groups of information built from top to bottom, and the hierarchies within each group.
        This layout does not contain connecting lines.
        :param text:                the typing.List[str] to be used as level 1 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """

        def _cols(e) -> int:
            if isinstance(e, str) or e[1] is None:
                return 1
            return sum([_cols(x) for x in e[1]])

        def _rows(e) -> int:
            if isinstance(e, str) or e[1] is None:
                return 1
            return 1 + max([_rows(x) for x in e[1]])

        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=_cols(text), number_of_rows=_rows(text)
        )
        row: typing.List[typing.Any] = [text]
        number_of_rows: int = _rows(text)
        j: int = 0
        while len(row) > 0:
            next_row: typing.List[typing.Any] = []
            for i, e in enumerate(row):
                c: Color = background_color
                if random.randint(0, 100) > 30:
                    c = foreground_color
                key: typing.Optional[str] = None
                children: typing.List[typing.Any] = []
                if isinstance(e, str):
                    key = e
                if isinstance(e, tuple):
                    key = e[0]
                    children.extend(e[1])
                table.add(
                    TableCell(
                        Paragraph(
                            key or "",
                            text_alignment=Alignment.CENTERED,
                            horizontal_alignment=Alignment.CENTERED,
                            font_size=font_size,
                            font_color=font_color,
                            background_color=c,
                        ),
                        border_left=True if i != 0 else False,
                        border_right=(True if i != len(row) - 1 else False),
                        border_top=False if j == 0 else True,
                        border_bottom=False if j == number_of_rows - 1 else True,
                        border_width=font_size / 2,
                        border_color=HexColor("ffffff"),
                        column_span=_cols(e),
                        background_color=c,
                    )
                )
                next_row.extend(children)
            row = next_row
            j += 1

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)

        # table
        return table

    @staticmethod
    def tags(
        s: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """

        :param s:                   the typing.List[str] to be converted to tags
        :param foreground_color:    the foreground_color (unused)
        :param background_color:    the background_color of the tags
        :param font_color:          the font_color of the tags
        :param font_size:           the font_size of the tags
        :return:
        """

        # get unique list of tags
        uniq: typing.List[str] = []
        for x in s:
            if x.upper() not in [y.upper() for y in uniq]:
                uniq.append(x)
        uniq.sort()

        # build typing.List[ChunkOfText]
        chunks: typing.List[
            typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]
        ] = []
        for t in uniq:
            chunks.append(
                ChunkOfText(
                    t,
                    font_size=font_size,
                    font_color=font_color,
                    background_color=background_color,
                    border_color=background_color,
                    border_top=True,
                    border_right=True,
                    border_bottom=True,
                    border_left=True,
                    border_radius_top_right=Decimal(5),
                    border_radius_bottom_right=Decimal(5),
                    border_radius_bottom_left=Decimal(5),
                    border_radius_top_left=Decimal(5),
                    padding_top=Decimal(2),
                    padding_right=Decimal(2),
                    padding_bottom=Decimal(0),
                    padding_left=Decimal(2),
                )
            )
            chunks.append(ChunkOfText(" ", font_size=font_size))
        chunks = chunks[:-1]

        # return
        return HeterogeneousParagraph(chunks)

    @staticmethod
    def vertical_bullet_list(
        text_level_1: typing.List[str],
        text_level_2: typing.List[typing.List[str]],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        A vertical bullet list is used to show non-sequential information or grouped data, yet it will not affect the outcome of the other data.
        The first block on the top is related to the second block as well as the third block but the process of the
        second block is not dependent on how the process on the first block is implemented.
        Apart from this, each block of information has the same emphasis, and it does not connote any direction.
        :param text_level_1:        the typing.List[str] to be used as level 1 text
        :param text_level_2         the typing.List[typing.List[str]] to be used as level 2 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text_level_1) > 0
        assert len(text_level_2) > 0
        assert all([len(x) > 0 for x in text_level_2])
        assert len(text_level_1) == len(text_level_2)
        assert font_size > 0
        N: int = len(text_level_1)
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_columns=1, number_of_rows=N * 2
        )
        for i in range(0, N):
            table.add(
                TableCell(
                    Paragraph(
                        text_level_1[i],
                        font_size=font_size + Decimal(2),
                        font="Helvetica-Bold",
                        font_color=font_color,
                        background_color=background_color,
                    ),
                    background_color=background_color,
                    border_radius_top_right=Decimal(20),
                    border_radius_bottom_right=Decimal(20),
                    border_radius_bottom_left=Decimal(20),
                    border_radius_top_left=Decimal(20),
                    border_color=background_color,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )
            ul: UnorderedList = UnorderedList()
            for li in text_level_2[i]:
                ul.add(Paragraph(li, font_size=font_size))
            table.add(
                TableCell(
                    ul,
                    border_top=False,
                    border_right=False,
                    border_bottom=False,
                    border_left=False,
                    padding_top=font_size,
                    padding_right=font_size,
                    padding_bottom=font_size,
                    padding_left=font_size,
                )
            )

        # return
        return table

    @staticmethod
    def vertical_process(
        text: typing.List[str],
        background_color: Color = HexColor("#8BBD8B"),
        font_color: Color = HexColor("#FFFFFF"),
        font_size: Decimal = Decimal(12),
        foreground_color: Color = HexColor("#6CAE75"),
    ) -> LayoutElement:
        """
        Use to show a progression or sequential steps in a task, process, or workflow.
        :param text:                the typing.List[str] to be used as level 1 text
        :param font_size:           the font_size to be used
        :param foreground_color:    the Color to be used in the foreground
        :param background_color:    the color to be used in the background
        :param font_color:          the Color to be used for text
        :return:                    a LayoutElement
        """
        assert len(text) > 0
        assert font_size > 0
        N: int = len(text)
        n: int = N * 2 - 1
        table: FlexibleColumnWidthTable = FlexibleColumnWidthTable(
            number_of_rows=n, number_of_columns=1
        )
        for i, e in enumerate(text):
            table.add(
                TableCell(
                    Paragraph(
                        e,
                        font_size=font_size,
                        font_color=font_color,
                        background_color=background_color,
                    ),
                    background_color=background_color,
                )
            )
            if i != len(text) - 1:
                table.add(
                    ConnectedShape(
                        LineArtFactory.arrow_down(
                            Rectangle(
                                Decimal(0),
                                Decimal(0),
                                Decimal(32),
                                Decimal(32),
                            )
                        ),
                        stroke_color=foreground_color,
                        fill_color=foreground_color,
                    )
                )

        table.set_padding_on_all_cells(font_size, font_size, font_size, font_size)
        table.no_borders()

        # return
        return table
