#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for retrieving TrueType fonts using the Google Font API.

This class provides functionality to download and manage TrueType fonts by
specifying their names. It facilitates interaction with the Google Font API
to access font resources.
"""
import pathlib
import typing

from borb.pdf.font.font import Font


class GoogleTrueTypeFont:
    """
    A class for retrieving TrueType fonts using the Google Font API.

    This class provides functionality to download and manage TrueType fonts by
    specifying their names. It facilitates interaction with the Google Font API
    to access font resources.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __download_google_font_to_temp_file(font_name: str) -> pathlib.Path:

        # get UNSPLASH_API_KEY
        # fmt: off
        import os
        google_fonts_api_key: typing.Optional[str] = os.environ.get("GOOGLE_FONTS_API_KEY")
        assert google_fonts_api_key is not None, "GOOGLE_FONTS_API_KEY not found in os.environ"
        # fmt: on

        # download overview
        import json

        try:
            import requests  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "Please install the 'requests' library to use the GoogleTrueTypeFont class. "
                "You can install it with 'pip install requests'."
            )

        try:

            # list all items
            items: typing.List[typing.Dict] = json.loads(
                requests.get(
                    f"https://www.googleapis.com/webfonts/v1/webfonts?key={google_fonts_api_key}"
                ).content
            ).get("items", [])

            # find matching font_info_dictionary
            # fmt: off
            font_info_dictionary: typing.Dict[str, typing.Any] = next(iter([x for x in items if x.get("family", None) == font_name]), {})
            if font_info_dictionary == {}:
                font_names: typing.List[str] = [x['family'] for x in items if isinstance(x, dict) and 'family' in x]
                font_names = [x for x in font_names if x is not None]
                font_names = sorted(font_names, key=lambda x:GoogleTrueTypeFont.__levenshtein(x.upper(), font_name.upper()))
                best_matching_font_name: str = font_names[0]
                assert font_info_dictionary is not None, f"Unable to find font {font_name}, did you mean \'{best_matching_font_name}\'?"
            # fmt: on

            # get URL
            # fmt: off
            true_type_font_file_url: typing.Optional[str] = font_info_dictionary.get("files", {}).get("regular", None)
            assert true_type_font_file_url is not None, f"Unable to find URL for font {font_name}"
            # fmt: on

            # download to temporary file
            # fmt: off
            import tempfile
            temp_font_file: pathlib.Path = pathlib.Path(tempfile.NamedTemporaryFile(suffix=".ttf").name)
            with open(temp_font_file, "wb") as fh:
                fh.write(requests.get(true_type_font_file_url).content)
            # fmt: on

            # return
            return temp_font_file
        except Exception as ex:
            assert False, f"Unable to process font {font_name}"

    @staticmethod
    def __levenshtein(s0: str, s1: str) -> int:
        # Create a matrix to hold distances
        len_s0 = len(s0)
        len_s1 = len(s1)

        # Initialize a matrix with zeros
        dp = [[0 for _ in range(len_s1 + 1)] for _ in range(len_s0 + 1)]

        # Fill the first row and column
        for i in range(len_s0 + 1):
            dp[i][0] = i
        for j in range(len_s1 + 1):
            dp[0][j] = j

        # Fill the matrix
        for i in range(1, len_s0 + 1):
            for j in range(1, len_s1 + 1):
                if s0[i - 1] == s1[j - 1]:
                    cost = 0
                else:
                    cost = 1

                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Deletion
                    dp[i][j - 1] + 1,  # Insertion
                    dp[i - 1][j - 1] + cost,  # Substitution
                )

        # The distance is in the bottom-right cell
        return dp[len_s0][len_s1]

    #
    # PUBLIC
    #

    @staticmethod
    def from_google_font_api(name: str) -> typing.Optional[Font]:
        """
        Retrieve a TrueType font by its name using the Google Font API.

        :param name:    The name of the font to retrieve.
        :return:        An instance of the Font class representing the requested TrueType font,
                        or None if the font could not be found or downloaded.
        """
        from borb.pdf.font.simple_font.true_type.true_type_font import TrueTypeFont

        return TrueTypeFont.from_file(
            where_from=GoogleTrueTypeFont.__download_google_font_to_temp_file(name)
        )
