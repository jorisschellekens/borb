import typing
from decimal import Decimal

from ptext.pdf.canvas.layout.layout_element import Alignment

try:
    import black

    able_to_import_black = True
except ImportError:
    able_to_import_black = False

from ptext.pdf.canvas.color.color import Color, X11Color, RGBColor
from ptext.pdf.canvas.font.font import Font
from ptext.pdf.canvas.layout.paragraph import Paragraph, LayoutElement


class CodeBlock(Paragraph):
    def __init__(
        self,
        text: str,
        font: typing.Union[Font, str] = "Courier",
        font_size: Decimal = Decimal(12),
        font_color: Color = RGBColor(Decimal(36), Decimal(41), Decimal(46)),
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(5),
        padding_right: Decimal = Decimal(5),
        padding_bottom: Decimal = Decimal(5),
        padding_left: Decimal = Decimal(5),
        background_color: typing.Optional[Color] = RGBColor(
            Decimal(246), Decimal(248), Decimal(250)
        ),
        parent: typing.Optional[LayoutElement] = None,
    ):
        # format string using black
        if able_to_import_black:
            text = black.format_str(text, mode=black.Mode())

        # call super
        super().__init__(
            text=text,
            font=font,
            font_size=font_size,
            font_color=font_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            background_color=background_color,
            respect_newlines_in_text=True,
            respect_spaces_in_text=True,
            parent=parent,
        )
