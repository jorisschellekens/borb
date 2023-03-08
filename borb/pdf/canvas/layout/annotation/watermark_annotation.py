#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A watermark annotation (PDF 1.6) shall be used to represent graphics that shall be printed at a fixed size and
position on a page, regardless of the dimensions of the printed page. The FixedPrint entry of a watermark
annotation dictionary (see Table 190) shall be a dictionary that contains values for specifying the size and
position of the annotation (see Table 191).
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class WatermarkAnnotation(Annotation):
    """
    A watermark annotation (PDF 1.6) shall be used to represent graphics that shall be printed at a fixed size and
    position on a page, regardless of the dimensions of the printed page. The FixedPrint entry of a watermark
    annotation dictionary (see Table 190) shall be a dictionary that contains values for specifying the size and
    position of the annotation (see Table 191).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(WatermarkAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
