#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A file attachment annotation (PDF 1.3) contains a reference to a file, which typically shall be embedded in the
PDF file (see 7.11.4, “Embedded File Streams”).
"""
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class FileAttachmentAnnotation(Annotation):
    """
    A file attachment annotation (PDF 1.3) contains a reference to a file, which typically shall be embedded in the
    PDF file (see 7.11.4, “Embedded File Streams”).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(FileAttachmentAnnotation, self).__init__()
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
