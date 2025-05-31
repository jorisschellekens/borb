#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a Type1 font and its properties in a PDF document.

The `Type1Font` class encapsulates the characteristics of a Type1 font, a widely used
PostScript font format in PDF documents. Type1 fonts are known for their high-quality
rendering and are commonly used in professional printing. This class provides access to
font-specific properties such as glyph mappings, metrics, and other attributes necessary
for rendering Type1 fonts accurately in PDF documents. As a subclass of `SimpleFont`,
it inherits basic font functionality while adding specific properties and behaviors
related to Type1 fonts.
"""

from borb.pdf.font.simple_font.simple_font import SimpleFont
from borb.pdf.primitives import name


class Type1Font(SimpleFont):
    """
    Represents a Type1 font and its properties in a PDF document.

    The `Type1Font` class encapsulates the characteristics of a Type1 font, a widely used
    PostScript font format in PDF documents. Type1 fonts are known for their high-quality
    rendering and are commonly used in professional printing. This class provides access to
    font-specific properties such as glyph mappings, metrics, and other attributes necessary
    for rendering Type1 fonts accurately in PDF documents. As a subclass of `SimpleFont`,
    it inherits basic font functionality while adding specific properties and behaviors
    related to Type1 fonts.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a Type1Font instance.

        This constructor initializes a new instance of the `Type1Font` class, which is a
        subclass of the `Font` class. It sets the font's `Subtype` to "Type1" and its
        `Type` to "Font", which are standard key-value pairs used to define the font's
        type and category in the PDF specification. These values help identify the font
        as a Type1 font, a widely used font format in PDF documents.
        """
        super().__init__()
        self[name("Subtype")] = name("Type1")
        self[name("Type")] = name("Font")

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
