#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The TrueType font format was developed by Apple Computer, Inc., and has been adopted as a standard font
format for the Microsoft Windows operating system. Specifications for the TrueType font file format are
available in Apple’s TrueType Reference Manual and Microsoft’s TrueType 1.0 Font Files Technical
Specification (see Bibliography).
"""
import json
import os
import tempfile
import typing
import pathlib

import requests

from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont


class GoogleTrueTypeFont(TrueTypeFont):
    """
    A TrueType font dictionary may contain the same entries as a Type 1 font dictionary (see Table 111), with these
    differences:
    •   The value of Subtype shall be TrueType.
    •   The value of Encoding is subject to limitations that are described in 9.6.6, "Character Encoding".
    •   The value of BaseFont is derived differently. The PostScript name for the value of BaseFont may be determined in one of two ways:
    •   If the TrueType font program's “name” table contains a PostScript name, it shall be used.
    •   In the absence of such an entry in the “name” table, a PostScript name shall be derived from the name by
        which the font is known in the host operating system. On a Windows system, the name shall be based on
        the lfFaceName field in a LOGFONT structure; in the Mac OS, it shall be based on the name of the FOND
        resource. If the name contains any SPACEs, the SPACEs shall be removed.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _download_google_font(font_name: str) -> pathlib.Path:

        # get GOOGLE_FONTS_API_KEY
        google_fonts_api_key: typing.Optional[str] = os.environ.get(
            "GOOGLE_FONTS_API_KEY"
        )
        assert (
            google_fonts_api_key is not None
        ), "GOOGLE_FONTS_API_KEY not found in os.environ"

        # download overview
        try:

            # list all items
            items: typing.List[typing.Dict] = json.loads(
                requests.get(
                    f"https://www.googleapis.com/webfonts/v1/webfonts?key={google_fonts_api_key}"
                ).content
            ).get("items", [])

            # find matching font_info_dictionary
            font_info_dictionary: typing.Dict[str, typing.Any] = next(
                iter([x for x in items if x.get("family", None) == font_name]), None
            )
            assert font_info_dictionary is not None, f"Unable to find font {font_name}"

            # get URL
            true_type_font_file_url: typing.Optional[str] = font_info_dictionary.get(
                "files", {}
            ).get("regular", None)
            assert (
                true_type_font_file_url is not None
            ), f"Unable to find URL for font {font_name}"

            # download to temporary file
            temp_font_file: pathlib.Path = pathlib.Path(
                tempfile.NamedTemporaryFile(suffix=".ttf").name
            )
            with open(temp_font_file, "wb") as fh:
                fh.write(requests.get(true_type_font_file_url).content)

            # return
            return temp_font_file
        except:
            assert False, f"Unable to process font {font_name}"

    #
    # PUBLIC
    #

    @staticmethod
    def true_type_font_from_google(
        font_name: str,
    ) -> typing.Union["TrueTypeFont", "Type0Font"]:
        """
        This function returns the PDF TrueTypeFont object for a given font name.
        It does so by looking up the font using the Google Fonts API,
        downloading the font to a temporary file,
        and subsequently loading that temporary file using TrueTypeFont.true_type_font_from_file
        :param font_name:   the font name
        :return:            a TrueTypeFont or Type0Font
        """
        return TrueTypeFont.true_type_font_from_file(
            GoogleTrueTypeFont._download_google_font(font_name)
        )
