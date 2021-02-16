#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This Enum provides a convenient way of getting all common paper page sizes
"""
import enum


class PageSize(enum.Enum):
    """
    This Enum provides a convenient way of getting all common paper page sizes
    """

    A0_PORTRAIT = (2384, 3370)
    A0_LANDSCAPE = (3370, 2384)

    A1_PORTRAIT = (1684, 2384)
    A1_LANDSCAPE = (2384, 1684)

    A2_PORTRAIT = (1190, 1684)
    A2_LANDSCAPE = (1684, 1190)

    A3_PORTRAIT = (842, 1190)
    A3_LANDSCAPE = (842, 1190)

    A4_PORTRAIT = (595, 842)
    A4_LANDSCAPE = (842, 595)

    A5_PORTRAIT = (420, 595)
    A5_LANDSCAPE = (595, 420)

    A6_PORTRAIT = (298, 420)
    A6_LANDSCAPE = (420, 298)

    A7_PORTRAIT = (210, 298)
    A7_LANDSCAPE = (298, 210)

    A8_PORTRAIT = (148, 210)
    A8_LANDSCAPE = (210, 148)

    A9_PORTRAIT = (105, 547)
    A9_LANDSCAPE = (547, 105)

    A10_PORTRAIT = (74, 105)
    A10_LANDSCAPE = (105, 74)

    B0_PORTRAIT = (2834, 4008)
    B0_LANDSCAPE = (4008, 2834)

    B1_PORTRAIT = (2004, 2834)
    B1_LANDSCAPE = (2834, 2004)

    B2_PORTRAIT = (1417, 2004)
    B2_LANDSCAPE = (2004, 1417)

    B3_PORTRAIT = (1000, 1417)
    B3_LANDSCAPE = (1417, 1000)

    B4_PORTRAIT = (708, 1000)
    B4_LANDSCAPE = (1000, 708)

    B5_PORTRAIT = (498, 708)
    B5_LANDSCAPE = (708, 498)

    B6_PORTRAIT = (354, 498)
    B6_LANDSCAPE = (498, 354)

    B7_PORTRAIT = (249, 354)
    B7_LANDSCAPE = (354, 249)

    B8_PORTRAIT = (175, 249)
    B8_LANDSCAPE = (249, 175)

    B9_PORTRAIT = (124, 175)
    B9_LANDSCAPE = (175, 124)

    B10_PORTRAIT = (88, 124)
    B10_LANDSCAPE = (124, 88)

    LETTER_PORTRAIT = (612, 792)
    LETTER_LANDSCAPE = (792, 612)

    LEGAL_PORTRAIT = (612, 1008)
    LEGAL_LANDSCAPE = (1008, 612)

    TABLOID_PORTRAIT = (792, 1224)
    TABLOID_LANDSCAPE = (792, 1224)

    LEDGER_PORTRAIT = (1224, 792)
    LEDGER_LANDSCAPE = (792, 1224)

    EXECUTIVE_PORTRAIT = (522, 756)
    EXECUTIVE_LANDSCAPE = (756, 522)
