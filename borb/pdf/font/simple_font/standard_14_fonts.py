#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents the standard 14 fonts used in PDF documents.

This utility class handles the standard 14 fonts, which include commonly used fonts
such as Helvetica, Times, and Courier. It provides methods to retrieve these fonts
by their names.
"""
import typing

from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.courier.courier import Courier
from borb.pdf.font.simple_font.courier.courier_bold import CourierBold
from borb.pdf.font.simple_font.courier.courier_bold_italic import CourierBoldItalic
from borb.pdf.font.simple_font.courier.courier_italic import CourierItalic
from borb.pdf.font.simple_font.helvetica.helvetica import Helvetica
from borb.pdf.font.simple_font.helvetica.helvetica_bold import HelveticaBold
from borb.pdf.font.simple_font.helvetica.helvetica_bold_italic import (
    HelveticaBoldItalic,
)
from borb.pdf.font.simple_font.helvetica.helvetica_italic import HelveticaItalic
from borb.pdf.font.simple_font.symbol.symbol import Symbol
from borb.pdf.font.simple_font.times.times import Times
from borb.pdf.font.simple_font.times.times_bold import TimesBold
from borb.pdf.font.simple_font.times.times_bold_italic import TimesBoldItalic
from borb.pdf.font.simple_font.times.times_italic import TimesItalic
from borb.pdf.font.simple_font.zapfdingbats.zapfdingbats import ZapfDingbats


class Standard14Fonts:
    """
    Represents the standard 14 fonts used in PDF documents.

    This utility class handles the standard 14 fonts, which include commonly used fonts
    such as Helvetica, Times, and Courier. It provides methods to retrieve these fonts
    by their names.
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
    def get(name: str) -> typing.Optional[Font]:
        """
        Retrieve a font by its name from the standard 14 PDF fonts.

        This method searches for the specified font name among the standard 14 PDF fonts
        and returns the corresponding Font object if found.

        :param name:    The name of the font to retrieve.
        :return:        The matching Font object if found; otherwise, None.
        """
        s0: str = name.upper()

        # COURIER
        if "COURIER" in s0:
            if ("BOLD" in s0) and ("ITALIC" in s0):
                return CourierBoldItalic()
            if ("BOLD" in s0) and ("OBLIQUE" in s0):
                return CourierBoldItalic()
            if "BOLD" in s0:
                return CourierBold()
            if "ITALIC" in s0:
                return CourierItalic()
            if "OBLIQUE" in s0:
                return CourierItalic()
            return Courier()

        # HELVETICA
        if "HELVETICA" in s0:
            if ("BOLD" in s0) and ("ITALIC" in s0):
                return HelveticaBoldItalic()
            if ("BOLD" in s0) and ("OBLIQUE" in s0):
                return HelveticaBoldItalic()
            if "BOLD" in s0:
                return HelveticaBold()
            if "ITALIC" in s0:
                return HelveticaItalic()
            if "OBLIQUE" in s0:
                return HelveticaItalic()
            return Helvetica()

        # TIMES
        if "TIMES" in s0:
            if ("BOLD" in s0) and ("ITALIC" in s0):
                return TimesBoldItalic()
            if ("BOLD" in s0) and ("OBLIQUE" in s0):
                return TimesBoldItalic()
            if "BOLD" in s0:
                return TimesBold()
            if "ITALIC" in s0:
                return TimesItalic()
            if "OBLIQUE" in s0:
                return TimesItalic()
            return Times()

        # SYMBOL
        if "SYMBOL" in s0:
            return Symbol()

        # ZAPFDINGBATS
        if "ZAPFDINGBATS" in s0:
            return ZapfDingbats()

        # default
        return None
