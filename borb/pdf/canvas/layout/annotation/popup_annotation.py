#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A pop-up annotation (PDF 1.3) displays text in a pop-up window for entry and editing. It shall not appear alone
but is associated with a markup annotation, its parent annotation, and shall be used for editing the parent’s text.
It shall have no appearance stream or associated actions of its own and shall be identified by the Popup entry
in the parent’s annotation dictionary (see Table 174). Table 183 shows the annotation dictionary entries specific
to this type of annotation.
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class PopupAnnotation(Annotation):
    """
    A pop-up annotation (PDF 1.3) displays text in a pop-up window for entry and editing. It shall not appear alone
    but is associated with a markup annotation, its parent annotation, and shall be used for editing the parent’s text.
    It shall have no appearance stream or associated actions of its own and shall be identified by the Popup entry
    in the parent’s annotation dictionary (see Table 174). Table 183 shows the annotation dictionary entries specific
    to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(PopupAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
