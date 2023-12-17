#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class attempts to optimize a Type0Font by performing subsetting.
Subsetting is performed using fontTools.subset, after which the dictionaries are updated in the
Type0Font, the page content is also changed, updating the TJ instructions to refer to the new GIDs.
"""
import io
import random
import typing
import zlib

from fontTools.subset import Subsetter as fSubsetter  # type: ignore[import]
from fontTools.ttLib import TTFont  # type: ignore[import]

# fmt: off
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Name
from borb.io.write.font.character_set_listener import CharacterSetListener
from borb.io.write.font.copy_command_operator import CopyCommandOperator
from borb.io.write.font.subset_show_text_with_glyph_positioning import SubSetShowTextWithGlyphPositioning
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.font.composite_font.font_type_0 import Type0Font
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.page.page import Page


# fmt: on


class Subsetter:
    """
    This class attempts to optimize a Type0Font by performing subsetting.
    Subsetting is performed using fontTools.subset, after which the dictionaries are updated in the
    Type0Font, the page content is also changed, updating the TJ instructions to refer to the new GIDs.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _extract_text_per_font(page: "Page") -> typing.Dict[Font, typing.Set[str]]:
        csp = CanvasStreamProcessor(page, Canvas(), [])
        l: CharacterSetListener = CharacterSetListener()
        csp.read(io.BytesIO(page["Contents"]["DecodedBytes"]), [l])
        return l.get_character_set_per_font()

    @staticmethod
    def _modify_page_content_stream(
        page: Page, old_fonts: typing.List[Font], new_fonts: typing.List[Font]
    ):
        # build CanvasStreamProcessor
        csp = CanvasStreamProcessor(page, Canvas(), [])

        # new content stream
        new_content_stream: bytearray = bytearray()

        # modify operators
        for k, v in csp._canvas_operators.items():
            csp._canvas_operators[k] = CopyCommandOperator(v, new_content_stream)

        # rewrite the operands for Tf
        csp._canvas_operators["TJ"] = SubSetShowTextWithGlyphPositioning(
            old_fonts, new_fonts, new_content_stream
        )

        # process page
        csp.read(io.BytesIO(page["Contents"]["DecodedBytes"]))

        # modify Contents
        page["Contents"][Name("DecodedBytes")] = new_content_stream
        page["Contents"][Name("Bytes")] = zlib.compress(new_content_stream, 9)
        page["Contents"][Name("Filter")] = Name("FlateDecode")
        page["Contents"][Name("Length")] = bDecimal(len(new_content_stream))

        # return
        return page

    #
    # PUBLIC
    #

    @staticmethod
    def apply(page: Page) -> Page:
        """
        This function applies Font subsetting to the input Page and returns the Page afterwards
        :param page:    the Page on which to apply Font subsetting
        :return:        the Page with Font subsetting
        """
        if "Resources" not in page:
            return page
        if not isinstance(page["Resources"], dict):
            return page
        if "Font" not in page["Resources"]:
            return page

        # determine which fonts to apply subsetting to
        fonts_to_be_subset: typing.List[Font] = [
            x for x in page["Resources"]["Font"].values() if isinstance(x, Type0Font)
        ]
        if len(fonts_to_be_subset) == 0:
            return page

        # determine character set for each Type0Font
        characters_per_font: typing.Dict[
            Font, typing.Set[str]
        ] = Subsetter._extract_text_per_font(page)

        # update which fonts to apply subsetting to
        fonts_to_be_subset = [
            x for x in fonts_to_be_subset if len(characters_per_font[x]) < 256
        ]
        if len(fonts_to_be_subset) == 0:
            return page

        subset_fonts: typing.List[Font] = []
        for old_font in fonts_to_be_subset:
            # get DecodedBytes
            font_file_bytes_001 = old_font["DescendantFonts"][0]["FontDescriptor"][
                "FontFile2"
            ]["DecodedBytes"]
            ttfont: TTFont = TTFont(io.BytesIO(font_file_bytes_001))

            # perform subsetting
            subsetter = fSubsetter()
            subsetter.populate(text="".join([x for x in characters_per_font[old_font]]))
            subsetter.options.glyph_names = True
            subsetter.options.recalc_bounds = True
            subsetter.options.recalc_average_width = True
            subsetter.subset(ttfont)

            # determine (modified) DecodedBytes
            with io.BytesIO() as font_file_bytes_002:
                ttfont.save(font_file_bytes_002)
                font_file_bytes_002 = font_file_bytes_002.getvalue()

            # build TrueTypeFont
            # fmt: off
            new_font: Font = TrueTypeFont.true_type_font_from_file(font_file_bytes_002)
            basefont_prefix: str = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(0, 6)])
            new_font[Name("BaseFont")] = Name(basefont_prefix + "+" + str(new_font[Name("BaseFont")]))
            new_font["FontDescriptor"][Name("FontName")] = new_font[Name("BaseFont")]
            new_font[Name("ToUnicode")] = TrueTypeFont._build_custom_cmap_for_type_0_font(ttfont)
            new_font.pop(Name("Encoding"))

            # fmt: on
            subset_fonts.append(new_font)

        # change Page / Contents
        Subsetter._modify_page_content_stream(page, fonts_to_be_subset, subset_fonts)

        # change Page / Resources / Font
        for old_font_name, old_font in page["Resources"]["Font"].items():
            if old_font not in fonts_to_be_subset:
                continue
            new_font = subset_fonts[fonts_to_be_subset.index(old_font)]
            page["Resources"]["Font"][old_font_name] = new_font

        # return
        return page
