#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a paragraph composed of heterogeneous pieces of text.

The `HeterogeneousParagraph` class is used to create a paragraph that
contains various chunks of text with different styles, such as different
fonts, sizes, colors, etc. The user can pass `Chunk` objects to form the
paragraph, where each `Chunk` can have its own styling properties.
"""
import functools
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.page import Page


class HeterogeneousParagraph(LayoutElement):
    """
    Represents a paragraph composed of heterogeneous pieces of text.

    The `HeterogeneousParagraph` class is used to create a paragraph that
    contains various chunks of text with different styles, such as different
    fonts, sizes, colors, etc. The user can pass `Chunk` objects to form the
    paragraph, where each `Chunk` can have its own styling properties.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        chunks: typing.List[Chunk],
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        fixed_leading: typing.Optional[int] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        multiplied_leading: typing.Optional[float] = 1.2,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        preserve_whitespaces: bool = False,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a HeterogeneousParagraph object composed of multiple Chunk objects.

        The `HeterogeneousParagraph` class allows the creation of a paragraph
        that consists of various `Chunk` objects, each potentially having different
        properties such as color, font, and background color. This facilitates the
        inclusion of richly formatted text within a single paragraph element.

        :param chunks:                  A list of `Chunk` objects representing individual pieces of text
                                        that may have varying styles and attributes.
        :param background_color:        Optional background color for the paragraph. Defaults to None.
        :param fixed_leading:           Optional fixed leading (line spacing) for the paragraph. If provided, it will override multiplied leading.
        :param multiplied_leading:      The factor by which to multiply the font size to calculate line spacing. Default is 1.2.
        :param text_alignment:          The alignment of the text within the paragraph. Defaults to left alignment.
        :param border_color:            Optional color for the border of the paragraph. Defaults to None.
        :param border_dash_pattern:     List defining the dash pattern for the border. Defaults to an empty list.
        :param border_dash_phase:       Phase offset for the dash pattern. Defaults to 0.
        :param border_width_bottom:     Width of the bottom border. Defaults to 0.
        :param border_width_left:       Width of the left border. Defaults to 0.
        :param border_width_right:      Width of the right border. Defaults to 0.
        :param border_width_top:        Width of the top border. Defaults to 0.
        :param horizontal_alignment:    Alignment of the paragraph within its containing element. Defaults to left alignment.
        :param margin_bottom:           Bottom margin around the paragraph. Defaults to 0.
        :param margin_left:             Left margin around the paragraph. Defaults to 0.
        :param margin_right:            Right margin around the paragraph. Defaults to 0.
        :param margin_top:              Top margin around the paragraph. Defaults to 0.
        :param padding_bottom:          Padding inside the bottom of the paragraph. Defaults to 0.
        :param padding_left:            Padding inside the left of the paragraph. Defaults to 0.
        :param padding_right:           Padding inside the right of the paragraph. Defaults to 0.
        :param padding_top:             Padding inside the top of the paragraph. Defaults to 0.
        :param vertical_alignment:      Alignment of the paragraph within its containing element vertically. Defaults to top alignment.
        """
        super().__init__(
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self.__fixed_leading: typing.Optional[float] = fixed_leading
        self.__multiplied_leading: typing.Optional[float] = multiplied_leading
        self.__preserve_whitespaces: bool = preserve_whitespaces
        self.__text_alignment: LayoutElement.TextAlignment = text_alignment
        self.__split_chunk_to_original_chunk: typing.Dict[Chunk, Chunk] = {}
        self.__chunks: typing.List[Chunk] = []
        for i, ch in enumerate(chunks):
            words: typing.List[str] = HeterogeneousParagraph.__split_str(
                ch.get_text(), preserve_whitespaces=self.__preserve_whitespaces
            )

            # IF there are no words
            # THEN skip
            if len(words) == 0:
                continue

            # IF the chunk is NOT the last chunk
            #   AND ends with whitespace
            #   AND we don't need to preserve the original whitespace
            # THEN force the chunk to end with a whitespace
            if (
                i != len(chunks) - 1
                and ch.get_text().endswith(" ")
                and (not preserve_whitespaces)
            ):
                words[-1] += " "

            # IF the chunk is NOT the first chunk
            #   AND starts with whitespace
            #   AND the previous chunk does not end with a whitespace
            #   AND we don't need to preserve the original whitespaces
            # THEN force the chunk to start with a whitespace
            if (
                i != 0
                and ch.get_text().startswith(" ")
                and (not chunks[i - 1].get_text().endswith(" "))
                and (not preserve_whitespaces)
            ):
                words[0] = " " + words[0]

            for w in words:
                # IF the chunk is empty
                # THEN continue
                if w == "":
                    continue
                # append a separate chunk for the word
                self.__chunks += [
                    Chunk(
                        w,
                        background_color=ch.get_background_color(),
                        border_color=ch.get_border_color(),
                        border_dash_pattern=ch.get_border_dash_pattern(),
                        border_dash_phase=ch.get_border_dash_phase(),
                        border_width_top=ch.get_border_width_top(),
                        border_width_right=ch.get_border_width_right(),
                        border_width_bottom=ch.get_border_width_bottom(),
                        border_width_left=ch.get_border_width_left(),
                        font=ch.get_font(),
                        font_color=ch.get_font_color(),
                        font_size=ch.get_font_size(),
                        horizontal_alignment=ch.get_horizontal_alignment(),
                        margin_bottom=ch.get_margin_bottom(),
                        margin_left=ch.get_margin_left(),
                        margin_right=ch.get_margin_right(),
                        margin_top=ch.get_margin_top(),
                        padding_bottom=ch.get_padding_bottom(),
                        padding_left=ch.get_padding_left(),
                        padding_right=ch.get_padding_right(),
                        padding_top=ch.get_padding_top(),
                        vertical_alignment=ch.get_vertical_alignment(),
                        character_spacing=ch.get_character_spacing(),
                    )
                ]
                self.__split_chunk_to_original_chunk[self.__chunks[-1]] = ch

    #
    # PRIVATE
    #

    @functools.cache
    def __get_lines(
        self,
        available_space: typing.Tuple[int, int],
        preserve_whitespaces: bool = False,
    ) -> typing.List[typing.List[Chunk]]:

        current_line_width: int = 0
        lines: typing.List[typing.List[Chunk]] = [[]]
        for c in self.__chunks:
            w, h = c.get_size(available_space=available_space)

            # IF the chunk fits on the line
            # THEN append the chunk to the line
            # THEN update the current_line_width
            if current_line_width + w <= available_space[0]:
                current_line_width += w
                lines[-1] += [c]
                continue

            # start a new line
            lines += [[c]]
            current_line_width = w

        # remove leading/trailing spaces
        if not preserve_whitespaces:
            for i in range(0, len(lines)):
                # remove leading space
                while len(lines[i]) > 0 and lines[i][0].get_text().isspace():
                    lines[i].pop(0)
                # remove trailing space
                while len(lines[i]) > 0 and lines[i][-1].get_text().isspace():
                    lines[i].pop(-1)

        # return
        return lines

    @staticmethod
    def __split_str(s: str, preserve_whitespaces: bool = False) -> typing.List[str]:
        import re

        xs: typing.List[str] = []
        if preserve_whitespaces:
            for x in re.split(r"(\s+)", re.sub(r"\s", " ", s)):
                xs.append(x)
        else:
            for x in re.split(r"\s+", s):
                xs.append(x)
                xs.append(" ")
            xs = xs[:-1]
            while len(xs) > 0 and (xs[0] == " " or xs[0] == ""):
                xs = xs[1:]
            while len(xs) > 0 and (xs[-1] == " " or xs[-1] == ""):
                xs = xs[:-1]
        return xs

    #
    # PUBLIC
    #

    @functools.cache
    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        # figure out how to lay out the Chunk(s)
        lines: typing.List[typing.List[Chunk]] = self.__get_lines(
            available_space=(
                available_space[0] - self.get_padding_left() - self.get_padding_right(),
                available_space[1] - self.get_padding_top() - self.get_padding_bottom(),
            ),
            preserve_whitespaces=self.__preserve_whitespaces,
        )

        # measure width, height
        # fmt: off
        w = max([sum([l.get_size(available_space=available_space)[0] for l in line]) for line in lines])
        hs = [max([l.get_size(available_space=available_space)[1] for l in line] + [0]) for line in lines]
        # fmt: on

        # IF the text is justified
        # THEN the full width needs to be consumed
        if self.__text_alignment == LayoutElement.TextAlignment.JUSTIFIED:
            w = available_space[0] - self.get_padding_left() - self.get_padding_right()

        # leading
        hs = [
            int(
                math.ceil(
                    h * (self.__multiplied_leading or 1.0)
                    + (self.__fixed_leading or 0.0)
                )
            )
            for h in hs
        ]

        # total height
        h: int = int(sum(hs))

        # return
        return (
            w + self.get_padding_left() + self.get_padding_right(),
            h + self.get_padding_bottom() + self.get_padding_top(),
        )

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # BDC
        # fmt: off
        HeterogeneousParagraph._begin_marked_content_with_dictionary(page=page, structure_element_type='P')  # type: ignore[attr-defined]
        # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # start drawing chunks
        lines: typing.List[typing.List[Chunk]] = self.__get_lines(
            available_space=(
                available_space[2] - self.get_padding_left() - self.get_padding_right(),
                available_space[3] - self.get_padding_top() - self.get_padding_bottom(),
            )
        )

        # paint lines
        line_y: int = background_y + h - self.get_padding_top()
        for line_nr, line in enumerate(lines):

            # determine line_height
            # fmt: off
            line_height: int = max([l.get_size(available_space=(2**64, 2**64))[1] for l in line] + [0])
            line_height = int(line_height * (self.__multiplied_leading or 1) + (self.__fixed_leading or 0))
            # fmt: on

            # determine line_width
            # fmt: off
            line_width: int = sum([l.get_size(available_space=(2**64, 2**64))[0] for l in line])
            # fmt: on

            # determine line_x, line_y
            extra_space_per_chunk: float = 0
            line_x: int = background_x + self.get_padding_left()
            avail_w: int = w - self.get_padding_right() - self.get_padding_left()
            if self.__text_alignment == LayoutElement.TextAlignment.RIGHT:
                line_x += avail_w - line_width
            if self.__text_alignment == LayoutElement.TextAlignment.CENTERED:
                line_x += (avail_w - line_width) // 2
            if self.__text_alignment == LayoutElement.TextAlignment.JUSTIFIED and (
                line_nr != len(lines) - 1
            ):
                if len(line) > 1:
                    # fmt: off
                    extra_space_per_chunk = (avail_w - line_width) / (len(line) - 1)
                    extra_space_per_chunk = math.floor(extra_space_per_chunk * 10**8) / 10**8
                    # fmt: on
                else:
                    extra_space_per_chunk = 0
            line_y -= line_height

            # paint
            for chunk in line:
                cw, ch = chunk.get_size(available_space=(2**64, 2**64))
                chunk.paint(available_space=(line_x, line_y, cw, ch), page=page)

                # IF we are applying LayoutElement.TextAlignment.JUSTIFIED
                # THEN we move line_x along by extra_space_per_chunk
                if self.__text_alignment == LayoutElement.TextAlignment.JUSTIFIED:
                    # we are purposefully ignoring the fact that we are mixing types
                    # because otherwise we have to shift line_x by an integer amount
                    # which is not trivial
                    line_x += extra_space_per_chunk  # type: ignore[assignment]

                # move line_x
                line_x += cw

        # EMC
        HeterogeneousParagraph._end_marked_content(page=page)  # type: ignore[attr-defined]

        # update bounding boxes of (original) Chunk objects
        min_max_x_y: typing.Dict[Chunk, typing.Tuple[int, int, int, int]] = {}
        for k0, v0 in self.__split_chunk_to_original_chunk.items():
            previous_paint_box: typing.Optional[typing.Tuple[int, int, int, int]] = (
                k0.get_previous_paint_box()
            )
            if previous_paint_box is None:
                continue
            assert previous_paint_box is not None
            if v0 not in min_max_x_y:
                min_max_x_y[v0] = (
                    previous_paint_box[0],
                    previous_paint_box[1],
                    previous_paint_box[0] + previous_paint_box[2],
                    previous_paint_box[1] + previous_paint_box[3],
                )
            else:
                min_max_x_y[v0] = (
                    min(min_max_x_y[v0][0], previous_paint_box[0]),
                    min(min_max_x_y[v0][1], previous_paint_box[1]),
                    max(
                        min_max_x_y[v0][2],
                        previous_paint_box[0] + previous_paint_box[2],
                    ),
                    max(
                        min_max_x_y[v0][3],
                        previous_paint_box[1] + previous_paint_box[3],
                    ),
                )
        for k1, v1 in min_max_x_y.items():
            k1._LayoutElement__previous_paint_box = (
                v1[0],
                v1[1],
                v1[2] - v1[0],
                v1[3] - v1[1],
            )
