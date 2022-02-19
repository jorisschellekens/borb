#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
“Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
entries specific to this type of annotation.
This method adds a link annotation with an action that opens a remote URI.
"""
from borb.io.read.types import Name, String, Dictionary
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class RemoteGoToAnnotation(Annotation):
    """
    A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
    “Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
    entries specific to this type of annotation.
    This method adds a link annotation with an action that opens a remote URI.
    """

    def __init__(self, bounding_box: Rectangle, uri: str):
        super(RemoteGoToAnnotation, self).__init__(bounding_box)

        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        self[Name("Subtype")] = Name("Link")

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        self[Name("A")] = Dictionary()
        self["A"][Name("Type")] = Name("Action")
        self["A"][Name("S")] = Name("URI")
        self["A"][Name("URI")] = String(uri)
