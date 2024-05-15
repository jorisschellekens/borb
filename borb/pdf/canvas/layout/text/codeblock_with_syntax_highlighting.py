#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In computer programming, a block or code block is a lexical structure of source code which is grouped together.
Blocks consist of one or more declarations and statements. A programming language that permits the creation of blocks,
including blocks nested within other blocks, is called a block-structured programming language.
Blocks are fundamental to structured programming, where control structures are formed from blocks.

The function of blocks in programming is to enable groups of statements to be treated as if they were one statement,
and to narrow the lexical scope of objects such as variables,
procedures and functions declared in a block so that they do not conflict with those having the same name used elsewhere.
In a block-structured programming language, the objects named in outer blocks are visible inside inner blocks,
unless they are masked by an object declared with the same name.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.emoji.emoji import Emoji
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import LineBreakChunk


class CodeBlockWithSyntaxHighlighting(HeterogeneousParagraph):
    """
    In computer programming, a block or code block is a lexical structure of source code which is grouped together.
    Blocks consist of one or more declarations and statements. A programming language that permits the creation of blocks,
    including blocks nested within other blocks, is called a block-structured programming language.
    Blocks are fundamental to structured programming, where control structures are formed from blocks.

    The function of blocks in programming is to enable groups of statements to be treated as if they were one statement,
    and to narrow the lexical scope of objects such as variables,
    procedures and functions declared in a block so that they do not conflict with those having the same name used elsewhere.
    In a block-structured programming language, the objects named in outer blocks are visible inside inner blocks,
    unless they are masked by an object declared with the same name.
    """

    LIGHT_THEME: typing.Dict[str, Color] = {
        "Token.Comment.Single": HexColor("8c8c8c"),
        "Token.Keyword": HexColor("0033b3"),
        "Token.Keyword.Constant": HexColor("0033b3"),
        "Token.Keyword.Namespace": HexColor("0033b3"),
        "Token.Literal.Number.Integer": HexColor("0033b3"),
        "Token.Literal.String": HexColor("067d17"),
        "Token.Literal.String.Doc": HexColor("8c8c8c"),
        "Token.Name.Builtin": HexColor("0033b3"),
        "Token.Name.Builtin.Pseudo": HexColor("a360b2"),
        "Token.Name.Function": HexColor("00627a"),
    }

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        font: typing.Union["Font", str] = "Courier",
        font_color: Color = HexColor("#000000"),
        font_size: Decimal = Decimal(12),
        horizontal_alignment: Alignment = Alignment.LEFT,
        padding_bottom: Decimal = Decimal(5),
        padding_left: Decimal = Decimal(5),
        padding_right: Decimal = Decimal(5),
        padding_top: Decimal = Decimal(5),
        vertical_alignment: Alignment = Alignment.TOP,
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        background_color: typing.Optional[Color] = HexColor("f6f8fa"),
    ):

        # format string using black
        try:
            import black  # type: ignore[import]

            text = black.format_str(text, mode=black.Mode())
        except:
            pass

        # call super.__init__
        super(CodeBlockWithSyntaxHighlighting, self).__init__(
            chunks_of_text=self._get_colored_chunks_of_text(
                text=text,
                default_font=font,
                default_font_color=font_color,
                font_size=font_size,
            ),
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            respect_newlines_in_text=True,
            vertical_alignment=vertical_alignment,
        )
        self._font: Font = StandardType1Font(font) if isinstance(font, str) else font
        self._font_color = font_color
        self._font_size = font_size

    #
    # PRIVATE
    #
    def _get_colored_chunks_of_text(
        self,
        default_font: typing.Union["Font", str],
        default_font_color: Color,
        font_size: Decimal,
        text: str,
    ) -> typing.List[typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]]:

        # convert to typing.List[ChunkOfText]
        chunks: typing.List[
            typing.Union[ChunkOfText, LineOfText, Emoji, Image, str]
        ] = []

        # go over entire text
        tokens_and_colors: typing.List[
            typing.Tuple[str, Color]
        ] = self._get_non_default_colored_tokens(text)
        tokens_and_colors_index: int = 0
        while len(text):

            # find first matching token
            next_token: str = tokens_and_colors[tokens_and_colors_index][0]
            next_color: Color = tokens_and_colors[tokens_and_colors_index][1]

            # prefix
            pos: int = text.find(next_token)
            prefix = text[:pos]
            if len(prefix):
                chunks.extend(
                    CodeBlockWithSyntaxHighlighting._split_token_on_newlines(
                        token_text=prefix,
                        font=default_font,
                        font_color=default_font_color,
                        font_size=font_size,
                    )
                )

            # token
            chunks.extend(
                CodeBlockWithSyntaxHighlighting._split_token_on_newlines(
                    token_text=next_token,
                    font=default_font,
                    font_color=next_color,
                    font_size=font_size,
                )
            )

            # update text
            text = text[pos + len(next_token) :]

            # update next_token
            tokens_and_colors_index += 1

            # (potential) clean up
            if tokens_and_colors_index == len(tokens_and_colors) and len(text):
                chunks.extend(
                    CodeBlockWithSyntaxHighlighting._split_token_on_newlines(
                        token_text=text,
                        font=default_font,
                        font_color=default_font_color,
                        font_size=font_size,
                    )
                )
                text = ""
                break

        # return
        return chunks

    def _get_non_default_colored_tokens(
        self, text: str
    ) -> typing.List[typing.Tuple[str, Color]]:
        """
        This function returns the tokens it found in the input, and their corresponding Color
        :return:    tokens and Colors (as typing.List[typing.Tuple[str, Color]])
        """

        number_of_tokens: int = 0
        number_of_default_tokens: int = 0
        tokens_and_colors: typing.List[typing.Tuple[str, Color]] = []

        from pygments import lexers  # type: ignore[import]

        for ttype, value in lexers.get_lexer_by_name("python").get_tokens(text):
            number_of_tokens += 1
            token_color: typing.Optional[Color] = self._get_token_color_by_type(ttype)
            if token_color is not None:
                tokens_and_colors += [(value, token_color)]
            else:
                number_of_default_tokens += 1
        return tokens_and_colors

    @staticmethod
    def _get_token_color_by_type(token_type: "_TokenType") -> typing.Optional[Color]:  # type: ignore[name-defined]
        if token_type is None:
            return None
        color_and_style: typing.Optional[
            Color
        ] = CodeBlockWithSyntaxHighlighting.LIGHT_THEME.get(str(token_type))
        while color_and_style is None and token_type.parent is not None:
            token_type = token_type.parent
            color_and_style = CodeBlockWithSyntaxHighlighting.LIGHT_THEME.get(
                str(token_type)
            )
        return color_and_style

    @staticmethod
    def _split_token_on_newlines(
        token_text: str,
        font: typing.Union[Font, str],
        font_color: Color,
        font_size: Decimal,
    ) -> typing.List[ChunkOfText]:
        if "\n" not in token_text:
            return [
                ChunkOfText(
                    token_text, font=font, font_color=font_color, font_size=font_size
                )
            ]
        cs: typing.List[ChunkOfText] = []
        for line in token_text.split("\n"):
            cs += [
                ChunkOfText(line, font=font, font_color=font_color, font_size=font_size)
            ]
            cs += [LineBreakChunk()]
            cs[-1]._font_size = font_size
        cs.pop(-1)
        return cs

    #
    # PUBLIC
    #
