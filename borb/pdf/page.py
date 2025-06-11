#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `Page` class inherits from `dict` and represents a page in a PDF document.

This class stores various elements and properties associated with the page, such as
text, images, and layout information. It provides a structured way to manage the
content and metadata of a page within the PDF.
"""
import typing

from borb.pdf.primitives import stream, name


class Page(dict):
    """
    The `Page` class inherits from `dict` and represents a page in a PDF document.

    This class stores various elements and properties associated with the page, such as
    text, images, and layout information. It provides a structured way to manage the
    content and metadata of a page within the PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, height_in_points: int = 842, width_in_points: int = 595):
        """
        Initialize a new PDF page object with specified dimensions.

        The `Page` class represents a single page in a PDF document, defined by its width and height in points.
        This constructor allows the creation of a page with customizable dimensions,
        typically used for setting up different page sizes such as A4 or letter.

        :param height_in_points:    The height of the page in points. Default is 842 points (A4 height).
        :param width_in_points:     The width of the page in points. Default is 595 points (A4 width).
        """
        super().__init__()
        self["Contents"] = stream()
        # self["CropBox"] = [0, 0, width_in_points, height_in_points]
        self["MediaBox"] = [0, 0, width_in_points, height_in_points]
        self["ProcSet"] = [name("PDF"), name("Text")]
        self["Resources"] = {}
        self["Rotate"] = 0
        self["Type"] = name("Page")
        self.__document: typing.Optional["Document"] = None  # type: ignore[name-defined]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_document(self) -> typing.Optional["Document"]:  # type: ignore[name-defined]
        """
        Retrieve the `Document` object to which this `Page` belongs.

        This method returns the `Document` that the current `Page` is part of. If the page
        has not yet been added to a document, it returns `None`. This can be useful when
        working with standalone `Page` objects or when you need to reference the parent
        `Document`.

        :return:    The `Document` object to which this `Page` belongs,
                    or `None` if the `Page` is not part of a `Document`.
        """
        return self.__document

    def get_size(self) -> typing.Tuple[int, int]:
        """
        Return the dimensions of the page in points.

        This method typically represents the width and height of the page. The size is determined
        based on the page's content or metadata and helps in understanding how the content fits
        within the page boundaries.

        :return: The size of the page as a tuple of (width, height) in points.
        """
        return int(self["MediaBox"][2]), int(self["MediaBox"][3])

    def rotate_left(self) -> "Page":
        """
        Rotate the entire page content by 90 degrees to the left (counterclockwise).

        This method effectively changes the orientation of the page, which is useful for
        adjusting the layout when the page has been scanned or created in the wrong orientation.

        :return: Self, with the updated rotation applied.
        """
        self["Rotate"] = (self.get("Rotate", 0) + 270) % 360
        if self["Rotate"] == 0:
            self.pop("Rotate")
        return self

    def rotate_right(self) -> "Page":
        """
        Rotate the entire page content by 90 degrees to the right (counterclockwise).

        This method effectively changes the orientation of the page, which is useful for
        adjusting the layout when the page has been scanned or created in the wrong orientation.

        :return: Self, with the updated rotation applied.
        """
        self["Rotate"] = (self.get("Rotate", 0) + 90) % 360
        if self["Rotate"] == 0:
            self.pop("Rotate")
        return self

    def uses_color_images(self) -> bool:
        """
        Determine if the PDF uses color images.

        The PDF operators used in content streams are grouped into categories of related
        operators called procedure sets (see Table 314). Each procedure set corresponds
        to a named resource that contains the implementations of the operators in that
        procedure set. The ProcSet entry in a content stream’s resource dictionary (see
        7.8.3, “Resource Dictionaries”) holds an array consisting of the names of the
        procedure sets used in that content stream.

        This method checks whether the PDF uses operators from the "ImageC" procedure set.

        :return: True if the page uses color images, False otherwise.
        """
        return "ImageC" in self.get("ProcSet", [])

    def uses_grayscale_images(self) -> bool:
        """
        Determine if the PDF uses grayscale images.

        The PDF operators used in content streams are grouped into categories of related
        operators called procedure sets (see Table 314). Each procedure set corresponds
        to a named resource that contains the implementations of the operators in that
        procedure set. The ProcSet entry in a content stream’s resource dictionary (see
        7.8.3, “Resource Dictionaries”) holds an array consisting of the names of the
        procedure sets used in that content stream.

        This method checks whether the PDF uses operators from the "ImageB" procedure set.

        :return: True if the page uses grayscale images, False otherwise.
        """
        return "ImageB" in self.get("ProcSet", [])

    def uses_indexed_images(self) -> bool:
        """
        Determine if the PDF uses indexed images.

        The PDF operators used in content streams are grouped into categories of related
        operators called procedure sets (see Table 314). Each procedure set corresponds
        to a named resource that contains the implementations of the operators in that
        procedure set. The ProcSet entry in a content stream’s resource dictionary (see
        7.8.3, “Resource Dictionaries”) holds an array consisting of the names of the
        procedure sets used in that content stream.

        This method checks whether the PDF uses operators from the "ImageI" procedure set.

        :return: True if the page uses indexed images, False otherwise.
        """
        return "ImageI" in self.get("ProcSet", [])

    def uses_painting_and_graphics_state(self) -> bool:
        """
        Check if the PDF uses operators from the painting and graphics state procedure set.

        PDF operators used in content streams are grouped into categories called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource containing
        the implementations of the operators in that procedure set. The ProcSet entry in a
        content stream’s resource dictionary (see 7.8.3, “Resource Dictionaries”) holds
        an array of the names of the procedure sets used in that content stream.

        This method determines whether the PDF utilizes operators from the "PDF" procedure set.

        :return: True if the page uses operators from the "PDF" procedure set, False otherwise.
        """
        return "PDF" in self.get("ProcSet", [])

    def uses_text(self) -> bool:
        """
        Check if the PDF uses text operators.

        PDF operators used in content streams are grouped into categories called procedure
        sets (see Table 314). Each procedure set corresponds to a named resource that
        contains the implementations of the operators in that procedure set. The ProcSet
        entry in a content stream’s resource dictionary (see 7.8.3, “Resource Dictionaries”)
        holds an array of the names of the procedure sets used in that content stream.

        This method determines whether the PDF utilizes operators from the "Text"
        procedure set.

        :return: True if the page uses operators from the "Text" procedure set, False otherwise.
        """
        return "Text" in self.get("ProcSet", [])
