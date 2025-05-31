#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a redaction annotation (PDF 1.7) that identifies content intended for removal from the document.

Redaction annotations facilitate a two-step process for managing sensitive content:

1. **Content Identification**:
   Users apply redaction annotations to specify the pieces or regions of content that should be removed.
   Until the next step is performed, users can see, move, and redefine these annotations.

2. **Content Removal**:
   Users instruct the viewer application to apply the redaction annotations. After this action, the content
   in the specified areas is removed, and a marking appears to indicate that the area has been redacted.
   Additionally, the redaction annotations themselves are removed from the PDF document.

Redaction annotations provide a mechanism for the content identification step, allowing content to be
marked for redaction in a non-destructive manner. This enables a review process to evaluate potential
redactions before the specified content is permanently removed.
"""


class RedactAnnotation:
    """
    Represents a redaction annotation (PDF 1.7) that identifies content intended for removal from the document.

    Redaction annotations facilitate a two-step process for managing sensitive content:

    1. **Content Identification**:
       Users apply redaction annotations to specify the pieces or regions of content that should be removed.
       Until the next step is performed, users can see, move, and redefine these annotations.

    2. **Content Removal**:
       Users instruct the viewer application to apply the redaction annotations. After this action, the content
       in the specified areas is removed, and a marking appears to indicate that the area has been redacted.
       Additionally, the redaction annotations themselves are removed from the PDF document.

    Redaction annotations provide a mechanism for the content identification step, allowing content to be
    marked for redaction in a non-destructive manner. This enables a review process to evaluate potential
    redactions before the specified content is permanently removed.
    """

    #
    # CONSTRUCTOR
    #
    # TODO
    pass

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
