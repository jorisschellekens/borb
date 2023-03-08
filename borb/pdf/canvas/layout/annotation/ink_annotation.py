#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more disjoint paths. When
opened, it shall display a pop-up window containing the text of the associated note. Table 182 shows the
annotation dictionary entries specific to this type of annotation.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class InkAnnotation(Annotation):
    """
    An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more disjoint paths. When
    opened, it shall display a pop-up window containing the text of the associated note. Table 182 shows the
    annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(InkAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
