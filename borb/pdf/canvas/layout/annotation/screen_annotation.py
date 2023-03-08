#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A screen annotation (PDF 1.5) specifies a region of a page upon which media clips may be played. It also
serves as an object from which actions can be triggered. 12.6.4.13, “Rendition Actions” discusses the
relationship between screen annotations and rendition actions. Table 187 shows the annotation dictionary
entries specific to this type of annotation.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class ScreenAnnotation(Annotation):
    """
    A screen annotation (PDF 1.5) specifies a region of a page upon which media clips may be played. It also
    serves as an object from which actions can be triggered. 12.6.4.13, “Rendition Actions” discusses the
    relationship between screen annotations and rendition actions. Table 187 shows the annotation dictionary
    entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(ScreenAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
