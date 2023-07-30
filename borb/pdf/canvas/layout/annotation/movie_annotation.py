#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A movie annotation (PDF 1.2) contains animated graphics and sound to be presented on the computer screen
and through the speakers. When the annotation is activated, the movie shall be played. Table 186 shows the
annotation dictionary entries specific to this type of annotation. Movies are discussed in 13.4, “Movies.”
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class MovieAnnotation(Annotation):
    """
    A movie annotation (PDF 1.2) contains animated graphics and sound to be presented on the computer screen
    and through the speakers. When the annotation is activated, the movie shall be played. Table 186 shows the
    annotation dictionary entries specific to this type of annotation. Movies are discussed in 13.4, “Movies.”
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(MovieAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
