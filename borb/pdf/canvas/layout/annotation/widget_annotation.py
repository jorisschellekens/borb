#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactive forms (see 12.7, “Interactive Forms”) use widget annotations (PDF 1.2) to represent the appearance
of fields and to manage user interactions. As a convenience, when a field has only a single associated widget
annotation, the contents of the field dictionary (12.7.3, “Field Dictionaries”) and the annotation dictionary may
be merged into a single dictionary containing entries that pertain to both a field and an annotation.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class WidgetAnnotation(Annotation):
    """
    Interactive forms (see 12.7, “Interactive Forms”) use widget annotations (PDF 1.2) to represent the appearance
    of fields and to manage user interactions. As a convenience, when a field has only a single associated widget
    annotation, the contents of the field dictionary (12.7.3, “Field Dictionaries”) and the annotation dictionary may
    be merged into a single dictionary containing entries that pertain to both a field and an annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(WidgetAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
