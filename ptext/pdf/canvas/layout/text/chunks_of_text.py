import copy
import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.layout_element import Alignment
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.canvas.layout.text.paragraph import Paragraph
from ptext.pdf.page.page import Page


class ChunksOfText(Paragraph):
    def __init__(
        self,
        chunks_of_text: typing.List[ChunkOfText],
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,  # type: ignore [name-defined]
    ):

        # background color
        self.background_color: typing.Optional[Color] = background_color

        # borders
        self.border_color: Color = border_color
        self.border_width: Decimal = border_width
        self.border_top: bool = border_top
        self.border_right: bool = border_right
        self.border_bottom: bool = border_bottom
        self.border_left: bool = border_left

        # alignment
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

        # padding
        self.padding_top: Decimal = padding_top
        self.padding_right: Decimal = padding_right
        self.padding_bottom: Decimal = padding_bottom
        self.padding_left: Decimal = padding_left

        # leading
        self._leading: Decimal = Decimal(1.3)

        # store chunks
        assert len(chunks_of_text) > 0
        self._chunks_of_text: typing.List[ChunkOfText] = chunks_of_text

    def _split_chunks_to_lines(
        self, page: Page, bounding_box: Rectangle
    ) -> typing.List[typing.Tuple[typing.List[ChunkOfText], Decimal]]:
        lines: typing.List[typing.Tuple[typing.List[ChunkOfText], Decimal]] = []
        previous_line: typing.List[ChunkOfText] = []
        previous_line_width: Decimal = Decimal(0)
        for i in range(0, len(self._chunks_of_text)):
            c: ChunkOfText = self._chunks_of_text[i]
            w: Decimal = c._calculate_layout_box_without_padding(
                page, bounding_box
            ).get_width()
            if previous_line_width + w > bounding_box.get_width():
                lines.append((copy.deepcopy(previous_line), previous_line_width))
                previous_line.clear()
                previous_line.append(c)
                previous_line_width = w
            else:
                previous_line.append(c)
                previous_line_width += w
        if len(previous_line) > 0:
            lines.append((copy.deepcopy(previous_line), previous_line_width))
        return lines

    def _do_layout_without_padding(self, page: Page, bounding_box: Rectangle):

        # split text to lines
        lines: typing.List[
            typing.Tuple[typing.List[ChunkOfText], Decimal]
        ] = self._split_chunks_to_lines(page, bounding_box)

        assert self.horizontal_alignment in [
            Alignment.LEFT,
            Alignment.RIGHT,
            Alignment.CENTERED,
        ]

        #
        min_x: Decimal = Decimal(2048)
        min_y: Decimal = Decimal(2048)
        max_x: Decimal = Decimal(0)
        max_y: Decimal = Decimal(0)

        # determine y-coordinate for line
        line_y: Decimal = (
            bounding_box.get_y()
            + bounding_box.get_height()
            - max([x.get_bounding_box().get_height() for x in lines[0][0]])
        )

        for line_of_chunks, line_width in lines:

            # determine x-coordinate to start line
            prev_x: Decimal = bounding_box.get_x()
            if self.horizontal_alignment == Alignment.LEFT:
                prev_x = bounding_box.get_x()
            elif self.horizontal_alignment == Alignment.RIGHT:
                # fmt: off
                prev_x = bounding_box.get_x() + bounding_box.get_width() - line_width
                # fmt: on
            elif self.horizontal_alignment == Alignment.CENTERED:
                # fmt: off
                prev_x = bounding_box.get_x() + (bounding_box.get_width() - line_width) / Decimal(2)
                # fmt: on

            # layout line
            for chunk_of_text in line_of_chunks:
                r: Rectangle = chunk_of_text.layout(
                    page,
                    Rectangle(
                        prev_x,
                        line_y,
                        bounding_box.get_width(),
                        chunk_of_text.font_size,
                    ),
                )

                # update prev_x
                prev_x += chunk_of_text.get_bounding_box().get_width()

                # keep track of layout coordinates
                # to determine the final layout rectangle of this pseudo-paragraph
                min_x = min(r.x, min_x)
                min_y = min(r.y, min_y)
                max_x = max(r.x + r.width, max_x)
                max_y = max(r.y + r.height, max_y)

            # update line_y
            line_y -= (
                max([x.get_bounding_box().get_height() for x in line_of_chunks])
                * self._leading
            )

        layout_rect = Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
