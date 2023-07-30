#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A caret annotation (PDF 1.5) is a visual symbol that indicates the presence of text edits. Table 180 lists the
entries specific to caret annotations.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class CaretAnnotation(Annotation):
    """
    A caret annotation (PDF 1.5) is a visual symbol that indicates the presence of text edits. Table 180 lists the
    entries specific to caret annotations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(CaretAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
