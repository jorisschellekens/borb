#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
3D annotations (PDF 1.6) are the means by which 3D artwork shall be represented in a PDF document.
Table 298 shows the entries specific to a 3D annotation dictionary. Table 164 describes the entries common to
all annotation dictionaries.

In addition to these entries, a 3D annotation shall provide an appearance stream in its AP entry (see Table 164)
that has a normal appearance (the N entry in Table 168). This appearance may be used by applications that do
not support 3D annotations and by all applications for the initial display of the annotation.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class ThreeDAnnotation(Annotation):
    """
    3D annotations (PDF 1.6) are the means by which 3D artwork shall be represented in a PDF document.
    Table 298 shows the entries specific to a 3D annotation dictionary. Table 164 describes the entries common to
    all annotation dictionaries.

    In addition to these entries, a 3D annotation shall provide an appearance stream in its AP entry (see Table 164)
    that has a normal appearance (the N entry in Table 168). This appearance may be used by applications that do
    not support 3D annotations and by all applications for the initial display of the annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(ThreeDAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
