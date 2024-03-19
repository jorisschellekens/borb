#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This Enum provides a convenient way of getting all common paper page sizes
"""
import enum
from decimal import Decimal


class PageSize(enum.Enum):
    """
    This Enum provides a convenient way of getting all common paper page sizes
    """

    A0_LANDSCAPE = (Decimal(3370), Decimal(2384))
    A0_PORTRAIT = (Decimal(2384), Decimal(3370))

    A1_LANDSCAPE = (Decimal(2384), Decimal(1684))
    A1_PORTRAIT = (Decimal(1684), Decimal(2384))

    A2_LANDSCAPE = (Decimal(1684), Decimal(1190))
    A2_PORTRAIT = (Decimal(1190), Decimal(1684))

    A3_LANDSCAPE = (Decimal(1190), Decimal(842))
    A3_PORTRAIT = (Decimal(842), Decimal(1190))

    A4_LANDSCAPE = (Decimal(842), Decimal(595))
    A4_PORTRAIT = (Decimal(595), Decimal(842))

    A5_LANDSCAPE = (Decimal(595), Decimal(420))
    A5_PORTRAIT = (Decimal(420), Decimal(595))

    A6_LANDSCAPE = (Decimal(420), Decimal(298))
    A6_PORTRAIT = (Decimal(298), Decimal(420))

    A7_LANDSCAPE = (Decimal(298), Decimal(210))
    A7_PORTRAIT = (Decimal(210), Decimal(298))

    A8_LANDSCAPE = (Decimal(210), Decimal(148))
    A8_PORTRAIT = (Decimal(148), Decimal(210))

    A9_LANDSCAPE = (Decimal(547), Decimal(105))
    A9_PORTRAIT = (Decimal(105), Decimal(547))

    A10_LANDSCAPE = (Decimal(105), Decimal(74))
    A10_PORTRAIT = (Decimal(74), Decimal(105))

    B0_LANDSCAPE = (Decimal(4008), Decimal(2834))
    B0_PORTRAIT = (Decimal(2834), Decimal(4008))

    B1_LANDSCAPE = (Decimal(2834), Decimal(2004))
    B1_PORTRAIT = (Decimal(2004), Decimal(2834))

    B2_LANDSCAPE = (Decimal(2004), Decimal(1417))
    B2_PORTRAIT = (Decimal(1417), Decimal(2004))

    B3_LANDSCAPE = (Decimal(1417), Decimal(1000))
    B3_PORTRAIT = (Decimal(1000), Decimal(1417))

    B4_LANDSCAPE = (Decimal(1000), Decimal(708))
    B4_PORTRAIT = (Decimal(708), Decimal(1000))

    B5_LANDSCAPE = (Decimal(708), Decimal(498))
    B5_PORTRAIT = (Decimal(498), Decimal(708))

    B6_LANDSCAPE = (Decimal(498), Decimal(354))
    B6_PORTRAIT = (Decimal(354), Decimal(498))

    B7_LANDSCAPE = (Decimal(354), Decimal(249))
    B7_PORTRAIT = (Decimal(249), Decimal(354))

    B8_LANDSCAPE = (Decimal(249), Decimal(175))
    B8_PORTRAIT = (Decimal(175), Decimal(249))

    B9_LANDSCAPE = (Decimal(175), Decimal(124))
    B9_PORTRAIT = (Decimal(124), Decimal(175))

    B10_LANDSCAPE = (Decimal(124), Decimal(88))
    B10_PORTRAIT = (Decimal(88), Decimal(124))

    EXECUTIVE_LANDSCAPE = (Decimal(756), Decimal(522))
    EXECUTIVE_PORTRAIT = (Decimal(522), Decimal(756))

    LEDGER_LANDSCAPE = (Decimal(792), Decimal(1224))
    LEDGER_PORTRAIT = (Decimal(1224), Decimal(792))

    LEGAL_LANDSCAPE = (Decimal(1008), Decimal(612))
    LEGAL_PORTRAIT = (Decimal(612), Decimal(1008))

    LETTER_LANDSCAPE = (Decimal(792), Decimal(612))
    LETTER_PORTRAIT = (Decimal(612), Decimal(792))

    TABLOID_LANDSCAPE = (Decimal(792), Decimal(1224))
    TABLOID_PORTRAIT = (Decimal(792), Decimal(1224))
