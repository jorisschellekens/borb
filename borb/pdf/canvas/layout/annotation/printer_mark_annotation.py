#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A printer’s mark annotation (PDF 1.4) represents a graphic symbol, such as a registration target, colour bar, or
cut mark, that may be added to a page to assist production personnel in identifying components of a multiple-
plate job and maintaining consistent output during production. See 14.11.3, “Printer’s Marks,” for further
discussion.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class PrinterMarkAnnotation(Annotation):
    """
    A printer’s mark annotation (PDF 1.4) represents a graphic symbol, such as a registration target, colour bar, or
    cut mark, that may be added to a page to assist production personnel in identifying components of a multiple-
    plate job and maintaining consistent output during production. See 14.11.3, “Printer’s Marks,” for further
    discussion.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(PrinterMarkAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
